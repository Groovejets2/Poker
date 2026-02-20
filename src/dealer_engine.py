"""
Dealer Engine for OpenClaw Poker Platform

Manages game flow, betting, pot management, and rules enforcement.
Supports both 5-card draw and Texas Hold'em variants.

Author: Angus Young
Date: 2026-02-21
Version: 1.0
"""

from enum import Enum
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import copy

from src.card import Card


class GameType(Enum):
    """Supported poker game variants."""
    TEXAS_HOLDEM = "texas_holdem"
    FIVE_CARD_DRAW = "five_card_draw"


class GamePhase(Enum):
    """Game state phases."""
    WAITING_FOR_PLAYERS = "waiting_for_players"
    GAME_STARTED = "game_started"
    BLINDS_POSTED = "blinds_posted"
    PRE_FLOP = "pre_flop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    POT_DISTRIBUTION = "pot_distribution"
    HAND_COMPLETE = "hand_complete"


class PlayerStatus(Enum):
    """Status of a player within the current hand."""
    ACTIVE = "active"
    FOLDED = "folded"
    ALL_IN = "all_in"
    WAITING_FOR_ACTION = "waiting_for_action"
    ACTED = "acted"
    OUT_OF_HAND = "out_of_hand"


class ActionType(Enum):
    """Valid player actions."""
    CHECK = "check"
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    ALL_IN = "all_in"


@dataclass
class PlayerAction:
    """Represents a player's action decision."""
    action: ActionType
    amount: int


@dataclass
class Player:
    """Represents a player at the table."""
    player_id: str
    position: str  # "dealer", "small_blind", "big_blind", or seat number
    initial_stack: int
    current_stack: int
    hole_cards: List[Card] = field(default_factory=list)
    status: PlayerStatus = PlayerStatus.ACTIVE
    current_bet_in_round: int = 0
    total_bet_in_hand: int = 0
    
    @property
    def is_active(self) -> bool:
        """Check if player is still in the hand."""
        return self.status in [PlayerStatus.ACTIVE, PlayerStatus.ALL_IN, PlayerStatus.WAITING_FOR_ACTION, PlayerStatus.ACTED]
    
    @property
    def can_act(self) -> bool:
        """Check if player can take an action."""
        return self.status in [PlayerStatus.ACTIVE, PlayerStatus.WAITING_FOR_ACTION]


@dataclass
class Pot:
    """Represents a pot (main or side)."""
    amount: int
    contributors: List[str]  # player_ids who contributed


class DealerEngine:
    """
    Core dealer engine managing game flow and rules.
    
    Responsibilities:
    - Game state management
    - Betting validation and processing
    - Pot and side pot management
    - Turn order management
    - Winner determination
    """
    
    def __init__(self, game_type: GameType, players: List[Player], small_blind: int, big_blind: int):
        """
        Initialize the dealer engine.
        
        Args:
            game_type: TEXAS_HOLDEM or FIVE_CARD_DRAW
            players: List of Player objects
            small_blind: Small blind amount
            big_blind: Big blind amount
        """
        self.game_type = game_type
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind
        
        # Game state
        self.current_phase = GamePhase.WAITING_FOR_PLAYERS
        self.current_round_bets = 0  # highest bet in current round
        self.action_index = 0  # index of player whose turn it is
        self.dealer_position = 0  # index of dealer
        
        # Cards
        self.community_cards: List[Card] = []
        self.deck: List[Card] = []
        
        # Pots
        self.main_pot = Pot(amount=0, contributors=[])
        self.side_pots: List[Pot] = []
        
        # Hand tracking
        self.players_in_hand = set(p.player_id for p in players)
        self.hand_number = 0
    
    def start_game(self):
        """Initialize the game."""
        self.current_phase = GamePhase.GAME_STARTED
    
    def start_hand(self):
        """
        Start a new hand.
        
        - Reset player status
        - Post blinds
        - Deal hole cards
        """
        self.hand_number += 1
        self.players_in_hand = set(p.player_id for p in self.players if p.current_stack > 0)
        
        # Reset betting for new hand
        for player in self.players:
            player.status = PlayerStatus.ACTIVE if player.player_id in self.players_in_hand else PlayerStatus.OUT_OF_HAND
            player.hole_cards = []
            player.current_bet_in_round = 0
            player.total_bet_in_hand = 0
        
        # Post blinds and set phase
        self._post_blinds()
        
        self.current_phase = GamePhase.BLINDS_POSTED
        self.current_round_bets = self.big_blind
        
        # Set action to small blind (or first active player after)
        self.action_index = self._get_next_active_player(self.dealer_position)
    
    def _post_blinds(self):
        """Post small and big blinds."""
        # Find small blind position (left of dealer)
        sb_index = (self.dealer_position + 1) % len(self.players)
        
        # Find big blind position (left of small blind)
        bb_index = (self.dealer_position + 2) % len(self.players)
        
        # Post small blind
        sb_player = self.players[sb_index]
        if sb_player.player_id in self.players_in_hand:
            amount_to_post = min(self.small_blind, sb_player.current_stack)
            sb_player.current_stack -= amount_to_post
            sb_player.current_bet_in_round = amount_to_post
            sb_player.total_bet_in_hand += amount_to_post
            self.main_pot.amount += amount_to_post
            if sb_player.player_id not in self.main_pot.contributors:
                self.main_pot.contributors.append(sb_player.player_id)
        
        # Post big blind
        bb_player = self.players[bb_index]
        if bb_player.player_id in self.players_in_hand:
            amount_to_post = min(self.big_blind, bb_player.current_stack)
            bb_player.current_stack -= amount_to_post
            bb_player.current_bet_in_round = amount_to_post
            bb_player.total_bet_in_hand += amount_to_post
            self.main_pot.amount += amount_to_post
            if bb_player.player_id not in self.main_pot.contributors:
                self.main_pot.contributors.append(bb_player.player_id)
    
    def get_next_active_player(self) -> Optional[Player]:
        """Get the next player whose turn it is to act."""
        if self.action_index >= len(self.players):
            return None
        return self.players[self.action_index]
    
    def _get_next_active_player(self, start_index: int) -> int:
        """
        Find the index of the next active player starting from start_index.
        
        Args:
            start_index: Starting position
            
        Returns:
            Index of next active player
        """
        for i in range(len(self.players)):
            candidate_index = (start_index + i) % len(self.players)
            player = self.players[candidate_index]
            if player.player_id in self.players_in_hand and player.is_active:
                return candidate_index
        return start_index
    
    def process_action(self, player_id: str, action: ActionType, amount: int) -> Tuple[bool, str]:
        """
        Process a player's action.
        
        Args:
            player_id: ID of the player taking action
            action: Type of action (CALL, RAISE, FOLD, ALL_IN, CHECK)
            amount: Bet amount for RAISE or ALL_IN
            
        Returns:
            (success: bool, message: str)
        """
        # Find the player
        player = next((p for p in self.players if p.player_id == player_id), None)
        if not player:
            return False, f"Player {player_id} not found"
        
        # Validate action
        is_valid, error_msg = self._validate_action(player, action, amount)
        if not is_valid:
            return False, error_msg
        
        # Process action
        if action == ActionType.FOLD:
            player.status = PlayerStatus.FOLDED
        
        elif action == ActionType.CHECK:
            player.status = PlayerStatus.ACTED
        
        elif action == ActionType.CALL:
            amount_to_call = self.current_round_bets - player.current_bet_in_round
            actual_call = min(amount_to_call, player.current_stack)
            
            player.current_stack -= actual_call
            player.current_bet_in_round += actual_call
            player.total_bet_in_hand += actual_call
            self.main_pot.amount += actual_call
            if player.player_id not in self.main_pot.contributors:
                self.main_pot.contributors.append(player.player_id)
            
            if actual_call < amount_to_call:
                # Player went all-in while calling
                player.status = PlayerStatus.ALL_IN
            else:
                player.status = PlayerStatus.ACTED
        
        elif action == ActionType.RAISE:
            # Remove previous bet from this round, add the new bet
            self.main_pot.amount -= player.current_bet_in_round
            
            actual_raise = min(amount, player.current_stack)
            player.current_stack -= actual_raise
            player.current_bet_in_round = actual_raise
            player.total_bet_in_hand += actual_raise
            self.main_pot.amount += actual_raise
            
            if player.player_id not in self.main_pot.contributors:
                self.main_pot.contributors.append(player.player_id)
            
            self.current_round_bets = actual_raise
            player.status = PlayerStatus.ACTED
        
        elif action == ActionType.ALL_IN:
            # Bet remaining stack
            all_in_amount = player.current_stack
            
            self.main_pot.amount -= player.current_bet_in_round
            self.main_pot.amount += all_in_amount + player.current_bet_in_round
            
            player.current_stack = 0
            player.current_bet_in_round += all_in_amount
            player.total_bet_in_hand += all_in_amount
            
            if player.player_id not in self.main_pot.contributors:
                self.main_pot.contributors.append(player.player_id)
            
            self.current_round_bets = max(self.current_round_bets, player.current_bet_in_round)
            player.status = PlayerStatus.ALL_IN
        
        # Move to next player
        self._advance_action()
        
        return True, f"Action processed: {action.value}"
    
    def _validate_action(self, player: Player, action: ActionType, amount: int) -> Tuple[bool, str]:
        """
        Validate a player's proposed action.
        
        Returns:
            (is_valid: bool, error_message: str)
        """
        if not player.can_act:
            return False, f"Player {player.player_id} cannot act (status: {player.status.value})"
        
        if action == ActionType.FOLD:
            return True, ""
        
        elif action == ActionType.CHECK:
            if self.current_round_bets > player.current_bet_in_round:
                return False, "Cannot check; there is a bet to call"
            return True, ""
        
        elif action == ActionType.CALL:
            amount_to_call = self.current_round_bets - player.current_bet_in_round
            if amount_to_call < 0:
                return False, "Invalid call amount"
            if amount_to_call > 0 and amount_to_call > player.current_stack:
                # Allow all-in call
                return True, ""
            return True, ""
        
        elif action == ActionType.RAISE:
            if amount < self.current_round_bets * 2:
                return False, f"Raise must be at least double the current bet ({self.current_round_bets * 2})"
            if amount > player.current_stack + player.current_bet_in_round:
                return False, "Raise amount exceeds player's stack"
            return True, ""
        
        elif action == ActionType.ALL_IN:
            if amount > player.current_stack + player.current_bet_in_round:
                return False, "All-in amount exceeds player's stack"
            return True, ""
        
        return False, f"Unknown action: {action}"
    
    def _advance_action(self):
        """Move action to next active player."""
        self.action_index = self._get_next_active_player(self.action_index + 1)
        
        active_player = self.players[self.action_index]
        if active_player.can_act:
            active_player.status = PlayerStatus.WAITING_FOR_ACTION
    
    def is_betting_round_complete(self) -> bool:
        """
        Check if the current betting round is complete.
        
        A betting round is complete when:
        - All active players have acted
        - All active players have called the current bet amount
        - Only one player remains (others folded)
        """
        active_players = [p for p in self.players if p.is_active]
        acting_players = [p for p in active_players if p.status in [PlayerStatus.ACTIVE, PlayerStatus.WAITING_FOR_ACTION]]
        
        if len(acting_players) <= 1:
            return True
        
        # Check if all have called the current bet
        for player in acting_players:
            if player.current_bet_in_round < self.current_round_bets:
                return False
        
        return True
    
    def get_active_players(self) -> List[Player]:
        """Get list of players still in the hand."""
        return [p for p in self.players if p.player_id in self.players_in_hand and p.is_active]
    
    def get_folded_players(self) -> List[Player]:
        """Get list of players who have folded."""
        return [p for p in self.players if p.status == PlayerStatus.FOLDED]
    
    def get_game_state(self) -> Dict:
        """Return the current game state for external consumption."""
        return {
            "phase": self.current_phase.value,
            "hand_number": self.hand_number,
            "players": [
                {
                    "player_id": p.player_id,
                    "position": p.position,
                    "stack": p.current_stack,
                    "status": p.status.value,
                    "current_bet": p.current_bet_in_round,
                    "total_bet": p.total_bet_in_hand
                }
                for p in self.players
            ],
            "main_pot": self.main_pot.amount,
            "side_pots": [p.amount for p in self.side_pots],
            "community_cards": [{"suit": c.suit, "rank": c.rank} for c in self.community_cards],
            "current_round_bets": self.current_round_bets
        }
