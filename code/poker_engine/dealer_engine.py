"""Dealer engine orchestrating all poker game components."""

from enum import Enum
from typing import Optional, List, Dict, Tuple
import logging

from poker_engine.game_state import GameState, GamePhase
from poker_engine.player_state import PlayerState, PlayerStatus, RoundStatus
from poker_engine.betting_validator import BettingValidator, ActionType
from poker_engine.pot_manager import PotManager
from poker_engine.winner_determiner import WinnerDeterminer
from poker_engine.hand_evaluator import HandEvaluator

logger = logging.getLogger(__name__)


class GameType(Enum):
    """Supported poker variants."""
    
    TEXAS_HOLDEM = "TEXAS_HOLDEM"
    """Texas Hold'em: community cards, 5-card best hand."""
    
    FIVE_CARD_DRAW = "FIVE_CARD_DRAW"
    """Five-card draw: no community cards, 5-card hand."""


class DealerEngine:
    """
    Orchestrates poker game flow and state management.
    
    Responsibilities:
    - Manage game phases and state transitions
    - Enforce turn order and action validation
    - Delegate to specialised components:
      * BettingValidator: action validation
      * PotManager: pot and side pot tracking
      * WinnerDeterminer: hand comparison and pot distribution
    
    Does NOT handle:
    - AI strategy (bot responsibility)
    - Card dealing (game coordinator responsibility)
    - Network communication (platform responsibility)
    
    Attributes:
        game_state (GameState): Current game state.
        betting_validator (BettingValidator): Action validator.
        pot_manager (PotManager): Pot and side pot manager.
        winner_determiner (WinnerDeterminer): Hand evaluator and distribution.
        game_type (GameType): Variant being played.
    """
    
    def __init__(
        self,
        game_type: GameType,
        players: List[PlayerState],
        small_blind_amount: int,
        big_blind_amount: int,
        game_id: str = "game_001"
    ):
        """
        Initialise the dealer engine.
        
        Args:
            game_type (GameType): Poker variant (TEXAS_HOLDEM or FIVE_CARD_DRAW).
            players (List[PlayerState]): 2-8 players seated at table.
            small_blind_amount (int): Small blind stake.
            big_blind_amount (int): Big blind stake.
            game_id (str): Unique game identifier.
        
        Raises:
            ValueError: If parameters invalid.
        """
        if not 2 <= len(players) <= 8:
            raise ValueError(f"Game must have 2-8 players, got {len(players)}")
        if big_blind_amount <= small_blind_amount:
            raise ValueError(
                f"Big blind {big_blind_amount} must exceed small blind {small_blind_amount}"
            )
        
        self.game_type = game_type
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
        
        # Initialise core components
        self.game_state = GameState(
            game_id=game_id,
            players=players,
            small_blind_amount=small_blind_amount,
            big_blind_amount=big_blind_amount
        )
        
        self.betting_validator = BettingValidator(
            self.game_state,
            min_raise_amount=big_blind_amount
        )
        
        self.pot_manager = PotManager(
            active_player_ids=[p.player_id for p in players]
        )
        
        hand_evaluator = HandEvaluator()
        self.winner_determiner = WinnerDeterminer(hand_evaluator)
        
        logger.info(
            f"Dealer engine initialised: game_id={game_id}, "
            f"players={len(players)}, blinds={small_blind_amount}/{big_blind_amount}"
        )
    
    # =========================================================================
    # HAND LIFECYCLE
    # =========================================================================
    
    def start_hand(self) -> None:
        """
        Initialise a new hand.
        
        Resets player states, posts blinds, and transitions to PRE_FLOP.
        
        Raises:
            ValueError: If fewer than 2 players with chips.
        """
        # Reset game state for new hand
        self.game_state.reset_for_new_hand()
        
        # Reinitialise pot manager
        active_ids = [p.player_id for p in self.game_state.get_active_players()]
        self.pot_manager = PotManager(active_ids)
        
        # Post blinds
        self._post_blinds()
        
        # Set first action player (UTG in Texas Hold'em)
        self.game_state.current_action_player = self._get_first_action_seat()
        self.game_state.advance_phase(GamePhase.PRE_FLOP)
        
        logger.info(
            f"Hand started: {self.game_state.game_id}, "
            f"active_players={len(active_ids)}, "
            f"button={self.game_state.dealer_button}"
        )
    
    def end_hand(self) -> None:
        """
        Complete current hand and prepare for next.
        
        Advances to HAND_COMPLETE phase.
        """
        self.game_state.advance_phase(GamePhase.HAND_COMPLETE)
        logger.info(f"Hand completed: {self.game_state.game_id}")
    
    # =========================================================================
    # ACTION REQUEST & PROCESSING
    # =========================================================================
    
    def request_action(self, player_id: str) -> Dict:
        """
        Request a player to act.
        
        Validates it's the player's turn and returns game state for decision.
        
        Args:
            player_id (str): Player making the request.
        
        Returns:
            Dict: Game state snapshot for bot decision making.
        
        Raises:
            ValueError: If not this player's turn.
        """
        player = self.game_state.get_player_by_id(player_id)
        if not player:
            raise ValueError(f"Player {player_id} not found")
        
        current_action_player = self.game_state.get_player_by_seat(
            self.game_state.current_action_player
        )
        
        if player.player_id != current_action_player.player_id:
            raise ValueError(
                f"Not {player_id}'s turn. Current: {current_action_player.player_id}"
            )
        
        return self._get_action_state_snapshot(player)
    
    def process_action(
        self,
        player_id: str,
        action: ActionType,
        amount: int = 0
    ) -> None:
        """
        Process a player's action.
        
        Validates action, updates state, and advances turn if needed.
        
        Args:
            player_id (str): Player taking action.
            action (ActionType): Action type (CHECK, FOLD, CALL, etc.).
            amount (int): Bet/raise amount (for BET, RAISE, ALL_IN).
        
        Raises:
            ValueError: If action invalid or not player's turn.
        """
        # Validate action
        try:
            self.betting_validator.validate_action(player_id, action, amount)
        except Exception as e:
            logger.error(f"Invalid action by {player_id}: {e}")
            raise
        
        player = self.game_state.get_player_by_id(player_id)
        
        # Execute action
        if action == ActionType.FOLD:
            player.fold()
            self.pot_manager.add_to_pot(player_id, 0)
            
        elif action == ActionType.CHECK:
            player.round_status = RoundStatus.ACTED
            self.pot_manager.add_to_pot(player_id, 0)
            
        elif action == ActionType.CALL:
            call_amount = self._calculate_call_amount(player)
            if call_amount > 0:
                player.post_bet(call_amount)
                self.pot_manager.add_to_pot(player_id, call_amount)
            player.round_status = RoundStatus.ACTED
            
        elif action == ActionType.BET:
            player.post_bet(amount)
            self.pot_manager.add_to_pot(player_id, amount)
            player.round_status = RoundStatus.ACTED
            self.game_state.current_action_player = self._get_next_action_seat()
            
        elif action == ActionType.RAISE:
            raise_total = self._calculate_raise_total(player, amount)
            player.post_bet(raise_total)
            self.pot_manager.add_to_pot(player_id, raise_total)
            player.round_status = RoundStatus.ACTED
            # Reset other players so they must act again after the raise
            for p in self.game_state.get_active_players():
                if p.player_id != player_id and not self._is_all_in(p) and not self._is_folded(p):
                    p.round_status = RoundStatus.WAITING_FOR_ACTION
            
        elif action == ActionType.ALL_IN:
            all_in_amount = player.stack
            if all_in_amount > 0:
                player.post_bet(all_in_amount)
                self.pot_manager.add_to_pot(player_id, all_in_amount)
            player.go_all_in()
            self.pot_manager.set_all_in(player_id, 0)
        
        # Advance turn
        self.game_state.current_action_player = self._get_next_action_seat()
        
        logger.debug(
            f"Action processed: {player_id}, action={action.value}, amount={amount}"
        )
    
    # =========================================================================
    # ROUND & PHASE MANAGEMENT
    # =========================================================================
    
    def advance_round(self) -> None:
        """
        Advance to the next betting round or showdown.
        
        Clears round bets and moves to next phase.
        
        Raises:
            ValueError: If all players haven't acted.
        """
        # Check if all active players have acted
        for player in self.game_state.get_active_players():
            if player.round_status == RoundStatus.WAITING_FOR_ACTION:
                raise ValueError("Not all players have acted")
        
        # Check if only one player remains (all others folded)
        remaining = [p for p in self.game_state.get_active_players()
                    if not self._is_folded(p)]
        
        if len(remaining) == 1:
            self.game_state.advance_phase(GamePhase.SHOWDOWN)
            return
        
        # Reset round state and move to next phase
        for player in self.game_state.get_active_players():
            player.clear_round_data()
        
        # Transition to next phase
        current = self.game_state.current_phase
        phase_map = {
            GamePhase.PRE_FLOP: GamePhase.FLOP,
            GamePhase.FLOP: GamePhase.TURN,
            GamePhase.TURN: GamePhase.RIVER,
            GamePhase.RIVER: GamePhase.SHOWDOWN,
        }
        
        next_phase = phase_map.get(current, GamePhase.SHOWDOWN)
        self.game_state.advance_phase(next_phase)
        
        # Set first action player for new round
        self.game_state.current_action_player = self._get_first_action_seat_post_flop()
        
        logger.debug(f"Advanced to phase: {next_phase.value}")
    
    # =========================================================================
    # SHOWDOWN & POT DISTRIBUTION
    # =========================================================================
    
    def determine_winners(self) -> Dict[str, int]:
        """
        Determine winners and calculate winnings per player.
        
        Handles side pots and split pots.
        
        Returns:
            Dict[str, int]: Winnings per player_id.
        """
        # Transition to showdown
        self.game_state.advance_phase(GamePhase.SHOWDOWN)
        
        # Calculate side pots
        self.pot_manager.calculate_side_pots()
        
        # Get remaining players (not folded)
        remaining = [p for p in self.game_state.get_active_players()
                    if not self._is_folded(p)]
        
        if len(remaining) == 1:
            # All others folded; winner takes pot
            winner_id = remaining[0].player_id
            total = self.pot_manager.get_pot_total()
            return {winner_id: total}
        
        # Multiple players: compare hands
        main_pot = self.pot_manager.get_main_pot()
        side_pots = self.pot_manager.get_side_pots()
        
        winnings = self.winner_determiner.determine_winners(
            remaining_players=remaining,
            main_pot=main_pot,
            side_pots=side_pots,
            community_cards=self.game_state.community_cards
        )
        
        logger.info(f"Winners determined: {winnings}")
        
        return winnings
    
    def distribute_pot(self, winnings: Dict[str, int]) -> None:
        """
        Distribute winnings to players.
        
        Args:
            winnings (Dict[str, int]): Amount each player won.
        """
        self.game_state.advance_phase(GamePhase.POT_DISTRIBUTION)
        
        for player_id, amount in winnings.items():
            player = self.game_state.get_player_by_id(player_id)
            if player:
                player.stack += amount
        
        logger.info(f"Pot distributed: {winnings}")
    
    # =========================================================================
    # STATE QUERIES
    # =========================================================================
    
    def get_game_state(self) -> Dict:
        """
        Get complete game state for external consumers.
        
        Returns:
            Dict: Game state snapshot.
        """
        return {
            "game_id": self.game_state.game_id,
            "phase": self.game_state.current_phase.value,
            "current_action_player": self.game_state.current_action_player,
            "main_pot": self.pot_manager.get_main_pot(),
            "side_pots": self.pot_manager.get_side_pots(),
            "total_pot": self.pot_manager.get_pot_total(),
            "community_cards": [str(c) for c in self.game_state.community_cards],
            "dealer_button": self.game_state.dealer_button,
            "players": [
                {
                    "player_id": p.player_id,
                    "seat": p.seat_number,
                    "stack": p.stack,
                    "current_bet": p.current_bet,
                    "status": p.status.value,
                    "hole_cards": [str(c) for c in p.hole_cards],
                }
                for p in self.game_state.players
            ]
        }
    
    def get_player_state(self, player_id: str) -> Dict:
        """
        Get state for a specific player.
        
        Args:
            player_id (str): Player's ID.
        
        Returns:
            Dict: Player state.
        
        Raises:
            ValueError: If player not found.
        """
        player = self.game_state.get_player_by_id(player_id)
        if not player:
            raise ValueError(f"Player {player_id} not found")
        
        return {
            "player_id": player.player_id,
            "seat": player.seat_number,
            "stack": player.stack,
            "current_bet": player.current_bet,
            "status": player.status.value,
            "is_active_in_hand": player.is_active_in_hand(),
            "hole_cards": [str(c) for c in player.hole_cards],
        }
    
    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================
    
    def _post_blinds(self) -> None:
        """Post small and big blinds."""
        sb_seat = (self.game_state.dealer_button + 1) % len(self.game_state.players)
        bb_seat = (self.game_state.dealer_button + 2) % len(self.game_state.players)
        
        sb_player = self.game_state.get_player_by_seat(sb_seat)
        bb_player = self.game_state.get_player_by_seat(bb_seat)
        
        # Post blinds (may be all-in for short stacks)
        sb_amount = min(self.small_blind_amount, sb_player.stack)
        bb_amount = min(self.big_blind_amount, bb_player.stack)
        
        sb_player.post_bet(sb_amount)
        bb_player.post_bet(bb_amount)
        
        self.pot_manager.add_to_pot(sb_player.player_id, sb_amount)
        self.pot_manager.add_to_pot(bb_player.player_id, bb_amount)
        
        if sb_player.stack == 0:
            sb_player.go_all_in()
        if bb_player.stack == 0:
            bb_player.go_all_in()
    
    def _get_first_action_seat(self) -> int:
        """
        Get first action seat for PRE_FLOP.
        
        In Texas Hold'em: UTG (3 seats left of dealer).
        In 5-card draw: Same as Hold'em initially.
        
        Returns:
            int: Seat number.
        """
        num_seats = len(self.game_state.players)
        return (self.game_state.dealer_button + 3) % num_seats
    
    def _get_first_action_seat_post_flop(self) -> int:
        """
        Get first action seat for FLOP, TURN, RIVER.
        
        Small blind acts first.
        
        Returns:
            int: Seat number.
        """
        num_seats = len(self.game_state.players)
        return (self.game_state.dealer_button + 1) % num_seats
    
    def _get_next_action_seat(self) -> Optional[int]:
        """
        Get next player who must act.
        
        Skips folded and all-in players.
        
        Returns:
            Optional[int]: Seat number, or None if round complete.
        """
        if self.game_state.current_action_player is None:
            return None
        
        current_seat = self.game_state.current_action_player
        num_seats = len(self.game_state.players)
        
        for offset in range(1, num_seats):
            next_seat = (current_seat + offset) % num_seats
            next_player = self.game_state.get_player_by_seat(next_seat)
            
            # Skip if not active in hand
            if not next_player.is_active_in_hand():
                continue
            
            # Skip if already all-in
            if self._is_all_in(next_player):
                continue
            
            # Skip if folded
            if self._is_folded(next_player):
                continue
            
            return next_seat
        
        # No more players can act
        return None
    
    def _calculate_call_amount(self, player: PlayerState) -> int:
        """Calculate amount player must call."""
        max_bet = max(
            (p.current_bet for p in self.game_state.get_active_players()),
            default=0
        )
        return max(0, max_bet - player.current_bet)
    
    def _calculate_raise_total(self, player: PlayerState, raise_amount: int) -> int:
        """Calculate total amount player must bet to raise."""
        call_amount = self._calculate_call_amount(player)
        return call_amount + raise_amount
    
    def _is_folded(self, player: PlayerState) -> bool:
        """Check if player has folded."""
        return player.status == PlayerStatus.FOLDED
    
    def _is_all_in(self, player: PlayerState) -> bool:
        """Check if player is all-in."""
        return player.status == PlayerStatus.ALL_IN
    
    def _get_action_state_snapshot(self, player: PlayerState) -> Dict:
        """
        Get game state snapshot for action request.
        
        Args:
            player (PlayerState): Player who will act.
        
        Returns:
            Dict: Relevant game information for action decision.
        """
        active_players = self.game_state.get_active_players()
        
        return {
            "player_id": player.player_id,
            "game_phase": self.game_state.current_phase.value,
            "your_cards": [str(c) for c in player.hole_cards],
            "your_stack": player.stack,
            "your_bet_this_round": player.current_bet,
            "community_cards": [str(c) for c in self.game_state.community_cards],
            "current_bet_to_call": self._calculate_call_amount(player),
            "pot_total": self.pot_manager.get_pot_total(),
            "active_players": [
                {
                    "player_id": p.player_id,
                    "seat": p.seat_number,
                    "stack": p.stack,
                    "current_bet": p.current_bet,
                }
                for p in active_players
            ],
        }
