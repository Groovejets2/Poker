"""
Game runner and invariant checker for OpenClaw Poker clinical testing.

Orchestrates full hands between bots, enforces all invariants from
TEST-PLAN.md after every hand, and supports multi-hand sessions and
survivor (persistent-stack) tests.
"""

import sys
import os
import random
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from poker_engine import (
    PlayerState,
    Card,
    ActionType,
    GamePhase,
    PlayerStatus,
    RoundStatus,
    InvalidActionError,
    NotPlayersTurnError,
)
from poker_engine.dealer_engine import DealerEngine, GameType
from bots.base_bot import BaseBot

from .statistics import SessionStatistics, HandResult
from .logger import SimulationLogger

# Default game configuration
STARTING_STACK = 1_000
SMALL_BLIND = 10
BIG_BLIND = 20

# Safety limit to prevent infinite loops in a single hand
MAX_HAND_ITERATIONS = 500


# =============================================================================
# DECK UTILITIES
# =============================================================================

def _create_shuffled_deck() -> List[Card]:
    """Create and shuffle a standard 52-card deck."""
    suits = [Card.HEARTS, Card.DIAMONDS, Card.CLUBS, Card.SPADES]
    deck = [Card(suit, rank) for suit in suits for rank in Card.RANKS]
    random.shuffle(deck)
    return deck


# =============================================================================
# INVARIANT CHECKING
# =============================================================================

def _check_invariants(
    chips_before: Dict[str, int],
    chips_after: Dict[str, int],
    dealt_cards: List[Card],
) -> List[str]:
    """
    Validate all invariants from TEST-PLAN.md Section 7 after a hand.

    Checks:
    - Pot conservation (total chips unchanged)
    - No negative stacks
    - Deck integrity (no duplicate cards dealt)

    Returns:
        List of violation descriptions. Empty list means all passed.
    """
    violations = []

    # 1. Pot conservation
    total_before = sum(chips_before.values())
    total_after = sum(chips_after.values())
    if total_before != total_after:
        violations.append(
            f"Pot conservation: before={total_before}, after={total_after}, "
            f"diff={total_after - total_before}"
        )

    # 2. No negative stacks
    for pid, stack in chips_after.items():
        if stack < 0:
            violations.append(f"Negative stack: {pid}={stack}")

    # 3. Deck integrity - no duplicate cards dealt
    seen: set = set()
    for card in dealt_cards:
        key = (card.suit, card.rank)
        if key in seen:
            violations.append(
                f"Duplicate card dealt: {card.rank} of {card.suit}"
            )
        seen.add(key)

    return violations


# =============================================================================
# GAME LOOP HELPERS
# =============================================================================

def _is_round_complete(engine: DealerEngine) -> bool:
    """
    Return True when all ACTIVE players have ACTED and matched the current bet.

    Two conditions must both hold for every PlayerStatus.ACTIVE player:
    1. Their RoundStatus is ACTED (not SITTING_OUT or WAITING_FOR_ACTION).
    2. Their current_bet equals the highest bet at the table, OR their stack
       is 0 (they went all-in for less than the max bet).

    Condition 2 handles an engine limitation: the ALL_IN action does not reset
    other players to WAITING_FOR_ACTION (only RAISE does).  Without this check,
    a player who previously ACTED at a lower bet level would not be re-prompted
    when a later ALL_IN exceeds their committed amount.
    """
    active = engine.game_state.get_active_players()
    max_bet = max((p.current_bet for p in active), default=0)

    for p in active:
        if p.status == PlayerStatus.ACTIVE:
            if p.round_status != RoundStatus.ACTED:
                return False
            # Player acted at a lower level than the current max bet and still
            # has chips to contribute - they must respond again.
            if p.current_bet < max_bet and p.stack > 0:
                return False
    return True


def _deal_community_cards(
    engine: DealerEngine,
    deck: List[Card],
    dealt_cards: List[Card],
    prev_phase: GamePhase,
    new_phase: GamePhase,
) -> None:
    """Deal the appropriate community cards when advancing between phases."""
    if new_phase == GamePhase.FLOP and prev_phase == GamePhase.PRE_FLOP:
        for _ in range(3):
            card = deck.pop()
            dealt_cards.append(card)
            engine.game_state.reveal_community_card(card)

    elif new_phase == GamePhase.TURN and prev_phase == GamePhase.FLOP:
        card = deck.pop()
        dealt_cards.append(card)
        engine.game_state.reveal_community_card(card)

    elif new_phase == GamePhase.RIVER and prev_phase == GamePhase.TURN:
        card = deck.pop()
        dealt_cards.append(card)
        engine.game_state.reveal_community_card(card)


# =============================================================================
# SINGLE HAND
# =============================================================================

def play_single_hand(
    bots: list,
    hand_number: int,
    starting_stacks: Optional[Dict[str, int]] = None,
) -> Tuple[HandResult, Dict[str, int]]:
    """
    Play one complete Texas Hold'em hand between the given bots.

    Args:
        bots: List of BaseBot instances.
        hand_number: Hand sequence number for logging.
        starting_stacks: Optional dict of player_id -> stack.
                         Defaults to STARTING_STACK for all players.

    Returns:
        Tuple of (HandResult, final_stacks dict).
    """
    stacks = starting_stacks or {bot.name: STARTING_STACK for bot in bots}

    # Create PlayerState objects with appropriate starting stacks
    players = [
        PlayerState(bot.name, seat_number=i, starting_stack=stacks[bot.name])
        for i, bot in enumerate(bots)
    ]

    bot_map: Dict[str, BaseBot] = {bot.name: bot for bot in bots}
    chips_before = {p.player_id: p.stack for p in players}

    # Create a fresh engine for this hand
    engine = DealerEngine(
        game_type=GameType.TEXAS_HOLDEM,
        players=players,
        small_blind_amount=SMALL_BLIND,
        big_blind_amount=BIG_BLIND,
    )

    deck = _create_shuffled_deck()
    dealt_cards: List[Card] = []

    engine.start_hand()

    # Deal hole cards to all active players
    for player in engine.game_state.get_active_players():
        c1, c2 = deck.pop(), deck.pop()
        dealt_cards.extend([c1, c2])
        player.deal_hole_cards([c1, c2])

    went_to_showdown = False
    winnings: Dict[str, int] = {}

    # Main game loop
    for _ in range(MAX_HAND_ITERATIONS):
        phase = engine.game_state.current_phase

        # Hand is over
        if phase in (GamePhase.SHOWDOWN, GamePhase.HAND_COMPLETE):
            went_to_showdown = True
            break

        # Advance the round when all ACTIVE players have ACTED (or all-in/folded).
        # This must be checked BEFORE processing the next player, because
        # the engine's _get_next_action_seat() does not inspect RoundStatus and
        # will keep cycling back to already-acted players indefinitely.
        if _is_round_complete(engine):
            prev_phase = phase
            try:
                engine.advance_round()
            except ValueError:
                # Unexpected - treat as hand over
                break
            new_phase = engine.game_state.current_phase
            _deal_community_cards(engine, deck, dealt_cards, prev_phase, new_phase)
            continue

        # Round not complete - get the next player who must act
        current_seat = engine.game_state.current_action_player
        if current_seat is None:
            break

        current_player = engine.game_state.get_player_by_seat(current_seat)
        if current_player is None:
            break

        player_id = current_player.player_id
        bot = bot_map.get(player_id)
        if bot is None:
            break

        try:
            snapshot = engine.request_action(player_id)
            action, amount = bot.get_action(snapshot)
            engine.process_action(player_id, action, amount)
        except Exception as _action_err:
            # Expected: InvalidActionError or NotPlayersTurnError when a bot
            # returns an action that is currently illegal (e.g. BET when
            # someone has already bet).  Unexpected errors (AttributeError,
            # KeyError, etc.) are written to stderr so they surface during
            # development without aborting the simulation.
            if not isinstance(_action_err, (InvalidActionError, NotPlayersTurnError)):
                sys.stderr.write(
                    f"[game_runner] Unexpected error for {player_id} "
                    f"({type(_action_err).__name__}: {_action_err})\n"
                )
            # Fallback cascade: try CHECK first (safe when player has matched
            # the current bet), then FOLD.  Using CHECK before FOLD avoids
            # eliminating the last active player when BET/RAISE fails because
            # someone already bet — a FOLD there would leave zero active
            # players and cause a pot-conservation violation.
            for fallback_action, fallback_amount in [
                (ActionType.CHECK, 0),
                (ActionType.FOLD, 0),
            ]:
                try:
                    engine.process_action(player_id, fallback_action, fallback_amount)
                    break
                except Exception:
                    continue
            else:
                break

    # Determine winners and distribute pot
    try:
        winnings = engine.determine_winners()
        engine.distribute_pot(winnings)
    except Exception as _winner_err:
        # Write the root cause to stderr so it surfaces in development.
        # The pot-conservation invariant check will detect the resulting
        # chip discrepancy on the next call to _check_invariants().
        sys.stderr.write(
            f"[game_runner] Winner determination failed "
            f"({type(_winner_err).__name__}: {_winner_err})\n"
        )
        winnings = {}

    engine.end_hand()

    # Collect final stacks and check invariants
    chips_after = {p.player_id: p.stack for p in engine.game_state.players}
    violations = _check_invariants(chips_before, chips_after, dealt_cards)

    pot_total = sum(winnings.values())
    players_folded = sum(
        1 for p in engine.game_state.players
        if p.status == PlayerStatus.FOLDED
    )

    result = HandResult(
        hand_number=hand_number,
        winners=winnings,
        pot_total=pot_total,
        players_folded=players_folded,
        went_to_showdown=went_to_showdown,
        invariant_violations=violations,
    )

    return result, chips_after


# =============================================================================
# SESSION RUNNER
# =============================================================================

class GameRunner:
    """Runs multi-hand sessions and collects statistics."""

    def __init__(self, bots: list, logger: SimulationLogger) -> None:
        self.bots = bots
        self.logger = logger

    def run_session(
        self,
        num_hands: int,
        session_label: str,
        batch_size: int = 100,
    ) -> SessionStatistics:
        """
        Run a session of num_hands, each with fresh STARTING_STACK per player.

        Args:
            num_hands: Total hands to play.
            session_label: Short label for the report filename.
            batch_size: Log a batch summary every N hands.

        Returns:
            SessionStatistics for the session.
        """
        bot_names = [b.name for b in self.bots]
        stats = SessionStatistics(bot_names=bot_names)

        self.logger.log_section(
            f"{session_label} - {num_hands} hands, {len(self.bots)} bots"
        )
        self.logger.log(f"  Bots: {', '.join(bot_names)}")
        self.logger.log(
            f"  Stack per hand: {STARTING_STACK} chips  |  "
            f"Blinds: {SMALL_BLIND}/{BIG_BLIND}"
        )
        self.logger.log("")

        for hand_num in range(1, num_hands + 1):
            result, _ = play_single_hand(self.bots, hand_num)
            stats.record_hand(result)
            self.logger.log_hand(
                hand_num, result.winners, result.pot_total,
                result.invariant_violations,
            )
            if hand_num % batch_size == 0:
                self.logger.log_batch(
                    hand_num // batch_size, hand_num, stats.summary()
                )

        self.logger.log_summary(stats.summary())
        report_path = self.logger.write_report(stats.summary(), session_label)
        self.logger.log(f"\n  Report written: {report_path}")

        return stats


# =============================================================================
# SURVIVOR TEST (PERSISTENT STACKS)
# =============================================================================

def run_survivor_test(
    bots: list,
    logger: SimulationLogger,
    max_hands: int = 2000,
    session_label: str = "survivor",
) -> SessionStatistics:
    """
    Run until one player holds all chips or max_hands is reached.

    Each bot keeps their stack across hands. Bots eliminated (stack = 0)
    are removed from subsequent hands. The simulation ends when only one
    player remains.

    Args:
        bots: List of BaseBot instances.
        logger: SimulationLogger for output.
        max_hands: Hard limit to prevent infinite sessions.
        session_label: Label for the report filename.

    Returns:
        SessionStatistics for the full survivor session.
    """
    bot_names = [b.name for b in bots]
    stats = SessionStatistics(bot_names=bot_names)

    current_stacks = {bot.name: STARTING_STACK for bot in bots}
    active_bots = list(bots)

    logger.log_section(
        f"{session_label} - Survivor test ({len(bots)} bots, max {max_hands} hands)"
    )
    logger.log(f"  Bots: {', '.join(bot_names)}")
    logger.log(
        f"  Starting stack: {STARTING_STACK} chips  |  "
        f"Blinds: {SMALL_BLIND}/{BIG_BLIND}"
    )
    logger.log("")

    for hand_num in range(1, max_hands + 1):
        if len(active_bots) < 2:
            logger.log(f"\n  Game over at hand {hand_num - 1}. "
                       f"Survivor: {active_bots[0].name if active_bots else 'none'}")
            break

        # Only include bots with chips
        hand_bots = [b for b in active_bots if current_stacks.get(b.name, 0) >= BIG_BLIND]
        if len(hand_bots) < 2:
            logger.log(f"\n  Fewer than 2 bots can afford the blind. Ending.")
            break

        hand_stacks = {b.name: current_stacks[b.name] for b in hand_bots}
        result, final_stacks = play_single_hand(hand_bots, hand_num, hand_stacks)
        stats.record_hand(result)

        # Update persistent stacks
        for name, stack in final_stacks.items():
            current_stacks[name] = stack

        logger.log_hand(
            hand_num, result.winners, result.pot_total,
            result.invariant_violations,
        )

        # Eliminate bots with no chips
        eliminated = [b for b in active_bots if current_stacks.get(b.name, 0) == 0]
        for bot in eliminated:
            active_bots.remove(bot)
            logger.log(f"    [ELIMINATED] {bot.name} - stack = 0")

        if hand_num % 100 == 0:
            logger.log_batch(hand_num // 100, hand_num, stats.summary())
            standing = ', '.join(
                f"{b.name}={current_stacks[b.name]}"
                for b in active_bots
            )
            logger.log(f"    Standings: {standing}")

    logger.log_summary(stats.summary())
    report_path = logger.write_report(stats.summary(), session_label)
    logger.log(f"\n  Report written: {report_path}")

    return stats
