"""Validates poker actions and betting decisions."""

from enum import Enum
from typing import Optional
from poker_engine.game_state import GameState


class ActionType(Enum):
    """Valid poker actions a player can take."""
    
    CHECK = "CHECK"
    """Player passes without betting."""
    
    FOLD = "FOLD"
    """Player forfeits the hand and current bets."""
    
    CALL = "CALL"
    """Player matches the current bet amount."""
    
    BET = "BET"
    """Player initiates a new bet (only when no one has bet this round)."""
    
    RAISE = "RAISE"
    """Player increases the current bet amount."""
    
    ALL_IN = "ALL_IN"
    """Player bets all remaining chips."""


class InvalidActionError(Exception):
    """Raised when a player attempts an invalid action."""


class NotPlayersTurnError(Exception):
    """Raised when a player acts out of turn."""


class BettingValidator:
    """
    Validates poker betting actions and turn order.
    
    This class checks whether a player's action is legal according to poker
    rules. It does NOT modify game state or pot management; it only validates.
    
    Attributes:
        game_state (GameState): Reference to the current game state.
        min_raise_amount (int): Minimum amount required to raise (default: big blind).
    """
    
    def __init__(self, game_state: GameState, min_raise_amount: Optional[int] = None):
        """
        Initialise the betting validator.
        
        Args:
            game_state (GameState): Reference to the current game state.
            min_raise_amount (Optional[int]): Minimum raise amount (default: big blind).
        
        Raises:
            ValueError: If game_state is None.
        """
        if game_state is None:
            raise ValueError("game_state cannot be None")
        
        self.game_state = game_state
        self.min_raise_amount = min_raise_amount or game_state.big_blind_amount
    
    def is_valid_turn(self, player_id: str) -> bool:
        """
        Check if it is this player's turn to act.
        
        Args:
            player_id (str): The player's unique identifier.
        
        Returns:
            bool: True if it is their turn, False otherwise.
        """
        if self.game_state.current_action_player is None:
            return False
        
        player = self.game_state.get_player_by_id(player_id)
        if player is None:
            return False
        
        current_player = self.game_state.get_player_by_seat(
            self.game_state.current_action_player
        )
        
        return player.seat_number == current_player.seat_number
    
    def validate_action(
        self,
        player_id: str,
        action: ActionType,
        amount: int = 0,
    ) -> None:
        """
        Validate a player's action.
        
        Checks turn order, action legality, and bet constraints.
        Raises InvalidActionError if action is illegal.
        
        Args:
            player_id (str): The player making the action.
            action (ActionType): The type of action.
            amount (int): Bet/raise amount (ignored for check/fold/call).
        
        Raises:
            NotPlayersTurnError: If it is not this player's turn.
            InvalidActionError: If the action is illegal.
        """
        if not self.is_valid_turn(player_id):
            raise NotPlayersTurnError(
                f"Player {player_id} is not the current actor"
            )
        
        player = self.game_state.get_player_by_id(player_id)
        
        if action == ActionType.CHECK:
            self._validate_check(player)
        elif action == ActionType.FOLD:
            self._validate_fold(player)
        elif action == ActionType.CALL:
            self._validate_call(player, amount)
        elif action == ActionType.BET:
            self._validate_bet(player, amount)
        elif action == ActionType.RAISE:
            self._validate_raise(player, amount)
        elif action == ActionType.ALL_IN:
            self._validate_all_in(player, amount)
        else:
            raise InvalidActionError(f"Unknown action type: {action}")
    
    def _validate_check(self, player) -> None:
        """
        Validate a check action.
        
        Only valid if the player has no bet to match this round.
        """
        active_players = self.game_state.get_active_players()
        max_bet = max(p.current_bet for p in active_players) if active_players else 0
        
        if max_bet > 0:
            raise InvalidActionError(
                f"Cannot check; current bet is {max_bet}"
            )
    
    def _validate_fold(self, player) -> None:
        """
        Validate a fold action.
        
        Fold is always valid (can be played anytime).
        """
        pass
    
    def _validate_call(self, player, amount: int) -> None:
        """
        Validate a call action.
        
        Call amount must equal the highest bet in the current round.
        """
        active_players = self.game_state.get_active_players()
        max_bet = max(p.current_bet for p in active_players) if active_players else 0
        call_amount = max_bet - player.current_bet
        
        if amount != call_amount:
            raise InvalidActionError(
                f"Call amount must be {call_amount}, got {amount}"
            )
        
        if call_amount > player.stack:
            raise InvalidActionError(
                f"Call amount {call_amount} exceeds stack {player.stack}"
            )
    
    def _validate_bet(self, player, amount: int) -> None:
        """
        Validate a bet action.
        
        Bet is only valid if no one has bet this round yet.
        Amount must be positive and <= stack.
        """
        active_players = self.game_state.get_active_players()
        max_bet = max(p.current_bet for p in active_players) if active_players else 0
        
        if max_bet > 0:
            raise InvalidActionError(
                f"Cannot bet; someone has already bet {max_bet}"
            )
        
        if amount <= 0:
            raise InvalidActionError(
                f"Bet amount must be positive, got {amount}"
            )
        
        if amount > player.stack:
            raise InvalidActionError(
                f"Bet amount {amount} exceeds stack {player.stack}"
            )
    
    def _validate_raise(self, player, amount: int) -> None:
        """
        Validate a raise action.
        
        Raise amount must be >= min_raise_amount and <= stack.
        Must be more than the current highest bet.
        """
        active_players = self.game_state.get_active_players()
        max_bet = max(p.current_bet for p in active_players) if active_players else 0
        
        if max_bet == 0:
            raise InvalidActionError(
                "Cannot raise; no bet to raise yet"
            )
        
        raise_total = player.current_bet + amount
        
        if raise_total < max_bet + self.min_raise_amount:
            raise InvalidActionError(
                f"Raise must be at least {max_bet + self.min_raise_amount}, got {raise_total}"
            )
        
        if amount > player.stack:
            raise InvalidActionError(
                f"Raise amount {amount} exceeds stack {player.stack}"
            )
    
    def _validate_all_in(self, player, amount: int) -> None:
        """
        Validate an all-in action.
        
        Amount must equal the player's remaining stack.
        """
        if amount != player.stack:
            raise InvalidActionError(
                f"All-in amount must equal remaining stack {player.stack}, got {amount}"
            )
        
        if amount <= 0:
            raise InvalidActionError(
                "Cannot go all-in with zero chips"
            )
