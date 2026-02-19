"""Dealer engine for managing game flow and state."""

from enum import Enum
from typing import List, Optional, Dict


class PlayerStatus(Enum):
    """Enumeration of possible player statuses in a poker game."""
    
    ACTIVE = "active"
    FOLDED = "folded"
    ALL_IN = "all_in"
    INACTIVE = "inactive"


class GamePhase(Enum):
    """Enumeration of poker game phases."""
    
    PRE_FLOP = "pre_flop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    COMPLETE = "complete"


class PlayerState:
    """
    Represents the state of a single player in a poker game.
    
    Attributes:
        player_id (int): Unique identifier for the player.
        starting_stack (int): Initial chip stack at the start of the hand.
        current_stack (int): Current chip count available for betting.
        current_bet (int): Total amount bet in the current round.
        total_contributed (int): Total amount contributed to the pot this hand.
        status (PlayerStatus): Current player status (active, folded, all-in).
        position (int): Player position at the table (0 = button, increases clockwise).
    """
    
    def __init__(
        self,
        player_id: int,
        starting_stack: int,
        position: int
    ) -> None:
        """
        Initialise a PlayerState instance.
        
        Args:
            player_id (int): Unique identifier for the player.
            starting_stack (int): Initial chip stack in chips.
            position (int): Seating position at the table.
        
        Raises:
            ValueError: If starting_stack is negative or player_id is negative.
        """
        if starting_stack < 0:
            raise ValueError("Starting stack cannot be negative")
        if player_id < 0:
            raise ValueError("Player ID cannot be negative")
        
        self.player_id = player_id
        self.starting_stack = starting_stack
        self.current_stack = starting_stack
        self.current_bet = 0
        self.total_contributed = 0
        self.status = PlayerStatus.ACTIVE
        self.position = position
    
    def place_bet(self, amount: int) -> None:
        """
        Place a bet and deduct from the player's stack.
        
        Args:
            amount (int): Amount to bet in chips.
        
        Raises:
            ValueError: If amount exceeds current stack or is negative.
        """
        if amount < 0:
            raise ValueError("Bet amount cannot be negative")
        if amount > self.current_stack:
            raise ValueError(
                f"Insufficient chips: bet {amount} exceeds stack {self.current_stack}"
            )
        
        self.current_stack -= amount
        self.current_bet += amount
        self.total_contributed += amount
    
    def reset_round_bet(self) -> None:
        """Reset the current round bet (called at the start of each betting round)."""
        self.current_bet = 0
    
    def set_all_in(self) -> None:
        """Mark the player as all-in and place remaining stack as bet."""
        if self.current_stack > 0:
            self.place_bet(self.current_stack)
        self.status = PlayerStatus.ALL_IN
    
    def fold(self) -> None:
        """Mark the player as folded."""
        self.status = PlayerStatus.FOLDED
    
    def is_active(self) -> bool:
        """
        Check if the player is active (can take action).
        
        Returns:
            bool: True if player status is ACTIVE, False otherwise.
        """
        return self.status == PlayerStatus.ACTIVE
    
    def get_remaining_stack(self) -> int:
        """
        Get the player's remaining chip stack.
        
        Returns:
            int: Current stack in chips.
        """
        return self.current_stack


class GameState:
    """
    Represents the state of a complete poker game.
    
    Manages multiple players, pot distribution, current betting round, and game phases.
    
    Attributes:
        players (List[PlayerState]): List of players in the game.
        pot (int): Total chips in the main pot.
        side_pots (List[int]): List of side pot amounts (for all-in situations).
        current_phase (GamePhase): Current phase of the game.
        current_bet_to_call (int): The current bet amount to match.
        min_bet (int): Minimum bet increment (big blind).
    """
    
    def __init__(self, players: List[PlayerState], min_bet: int = 2) -> None:
        """
        Initialise a GameState instance.
        
        Args:
            players (List[PlayerState]): List of players in the game.
            min_bet (int): Minimum bet increment (typically the big blind). Defaults to 2.
        
        Raises:
            ValueError: If fewer than 2 players or min_bet is invalid.
        """
        if len(players) < 2:
            raise ValueError("Game requires at least 2 players")
        if min_bet <= 0:
            raise ValueError("Minimum bet must be positive")
        
        self.players = players
        self.pot = 0
        self.side_pots = []
        self.current_phase = GamePhase.PRE_FLOP
        self.current_bet_to_call = min_bet
        self.min_bet = min_bet
    
    def add_to_pot(self, amount: int) -> None:
        """
        Add chips to the main pot.
        
        Args:
            amount (int): Amount in chips to add to the pot.
        
        Raises:
            ValueError: If amount is negative.
        """
        if amount < 0:
            raise ValueError("Pot amount cannot be negative")
        self.pot += amount
    
    def get_total_pot(self) -> int:
        """
        Calculate the total pot (main pot plus all side pots).
        
        Returns:
            int: Total chips in play across all pots.
        """
        return self.pot + sum(self.side_pots)
    
    def move_to_next_phase(self) -> None:
        """
        Advance the game to the next phase.
        
        Phases progress as: PRE_FLOP -> FLOP -> TURN -> RIVER -> SHOWDOWN -> COMPLETE
        """
        phase_progression = {
            GamePhase.PRE_FLOP: GamePhase.FLOP,
            GamePhase.FLOP: GamePhase.TURN,
            GamePhase.TURN: GamePhase.RIVER,
            GamePhase.RIVER: GamePhase.SHOWDOWN,
            GamePhase.SHOWDOWN: GamePhase.COMPLETE,
            GamePhase.COMPLETE: GamePhase.COMPLETE
        }
        self.current_phase = phase_progression.get(
            self.current_phase,
            GamePhase.COMPLETE
        )
        # Reset betting round
        self.current_bet_to_call = 0
        for player in self.players:
            player.reset_round_bet()
    
    def get_active_players(self) -> List[PlayerState]:
        """
        Get all players who are still active in the hand.
        
        Returns:
            List[PlayerState]: List of players with status ACTIVE or ALL_IN.
        """
        return [
            p for p in self.players
            if p.status in (PlayerStatus.ACTIVE, PlayerStatus.ALL_IN)
        ]
    
    def get_active_action_players(self) -> List[PlayerState]:
        """
        Get players who can take action (ACTIVE status only, not all-in).
        
        Returns:
            List[PlayerState]: List of ACTIVE players who can make decisions.
        """
        return [p for p in self.players if p.status == PlayerStatus.ACTIVE]
    
    def get_player_by_id(self, player_id: int) -> Optional[PlayerState]:
        """
        Retrieve a player by their ID.
        
        Args:
            player_id (int): The player's unique identifier.
        
        Returns:
            Optional[PlayerState]: The player if found, None otherwise.
        """
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def create_side_pot(self, amount: int) -> None:
        """
        Create a side pot (used when players go all-in with different amounts).
        
        Args:
            amount (int): Amount in chips to allocate to the side pot.
        
        Raises:
            ValueError: If amount is negative.
        """
        if amount < 0:
            raise ValueError("Side pot amount cannot be negative")
        self.side_pots.append(amount)
    
    def get_game_summary(self) -> Dict:
        """
        Generate a summary of the current game state.
        
        Returns:
            Dict: Dictionary containing pot, phase, active players count, and min bet.
        """
        return {
            "pot": self.pot,
            "total_pot": self.get_total_pot(),
            "phase": self.current_phase.value,
            "active_players": len(self.get_active_players()),
            "min_bet": self.min_bet,
            "current_bet_to_call": self.current_bet_to_call
        }
