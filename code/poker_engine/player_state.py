"""Player state representation for the dealer engine."""

from enum import Enum
from typing import List, Optional
from poker_engine.card import Card


class PlayerStatus(Enum):
    """Status of a player in the current hand."""
    
    ACTIVE = "ACTIVE"
    """Player is still in the hand and may act."""
    
    FOLDED = "FOLDED"
    """Player has folded; no longer eligible to win the pot."""
    
    ALL_IN = "ALL_IN"
    """Player has gone all-in; cannot act further this hand."""
    
    OUT_OF_HAND = "OUT_OF_HAND"
    """Player has folded or is sitting out; not participating."""


class RoundStatus(Enum):
    """Status of a player within the current betting round."""
    
    WAITING_FOR_ACTION = "WAITING_FOR_ACTION"
    """It is this player's turn to act."""
    
    ACTED = "ACTED"
    """Player has acted; waiting for others."""
    
    SITTING_OUT = "SITTING_OUT"
    """Player is folded or all-in; no further action this round."""


class PlayerState:
    """
    Represents the state of a single player in the game.
    
    This class tracks all information about a player: their stack, cards, position,
    and current status. It is updated by the dealer engine as the hand progresses.
    
    Attributes:
        player_id (str): Unique identifier for the player/bot.
        seat_number (int): Seat position at the table (0-7).
        stack (int): Number of chips remaining (cannot be negative).
        current_bet (int): Number of chips bet in current round.
        hole_cards (List[Card]): Private cards dealt to this player.
        status (PlayerStatus): Current status (ACTIVE, FOLDED, ALL_IN, OUT_OF_HAND).
        round_status (RoundStatus): Status within current betting round.
    """
    
    def __init__(
        self,
        player_id: str,
        seat_number: int,
        starting_stack: int,
    ):
        """
        Initialise a player in the game.
        
        Args:
            player_id (str): Unique identifier for the player/bot.
            seat_number (int): Seat position at the table (0-7).
            starting_stack (int): Initial chip stack (must be positive).
        
        Raises:
            ValueError: If seat_number is not in range 0-7 or starting_stack <= 0.
        """
        if not 0 <= seat_number <= 7:
            raise ValueError(f"Seat number must be 0-7, got {seat_number}")
        if starting_stack <= 0:
            raise ValueError(f"Starting stack must be positive, got {starting_stack}")
        
        self.player_id = player_id
        self.seat_number = seat_number
        self.stack = starting_stack
        self.current_bet = 0
        self.hole_cards: List[Card] = []
        self.status = PlayerStatus.ACTIVE
        self.round_status = RoundStatus.SITTING_OUT
    
    def post_bet(self, amount: int) -> None:
        """
        Record a bet or raise by this player.
        
        This adds to the player's current_bet for the round.
        Deducts from the player's stack.
        
        Args:
            amount (int): Amount to bet (must be <= stack).
        
        Raises:
            ValueError: If amount > stack or amount < 0.
        """
        if amount < 0:
            raise ValueError(f"Bet amount cannot be negative: {amount}")
        if amount > self.stack:
            raise ValueError(
                f"Bet amount {amount} exceeds stack {self.stack}"
            )
        
        self.stack -= amount
        self.current_bet += amount
    
    def fold(self) -> None:
        """
        Mark this player as folded.
        
        The player forfeits all bets in the current pot.
        They cannot win the pot and cannot act further.
        """
        self.status = PlayerStatus.FOLDED
        self.round_status = RoundStatus.SITTING_OUT
    
    def go_all_in(self) -> None:
        """
        Mark this player as all-in.
        
        All remaining chips have been bet.
        The player cannot act further but may still win the pot.
        """
        self.status = PlayerStatus.ALL_IN
        self.round_status = RoundStatus.SITTING_OUT
    
    def deal_hole_cards(self, cards: List[Card]) -> None:
        """
        Deal hole cards to this player.
        
        Args:
            cards (List[Card]): List of cards to deal (usually 2 for Hold'em, 5 for Draw).
        
        Raises:
            ValueError: If cards list is empty or contains non-Card objects.
        """
        if not cards:
            raise ValueError("Must deal at least one card")
        for card in cards:
            if not isinstance(card, Card):
                raise ValueError(f"Expected Card, got {type(card)}")
        
        self.hole_cards = cards.copy()
    
    def clear_round_data(self) -> None:
        """
        Reset player data for the next round.
        
        Clears current bet, round status, and hole cards.
        Does NOT reset stack or player status (that persists across rounds).
        """
        self.current_bet = 0
        self.round_status = RoundStatus.SITTING_OUT
        self.hole_cards = []
    
    def is_active_in_hand(self) -> bool:
        """
        Check if the player is still active in the current hand.
        
        Returns:
            bool: True if status is ACTIVE or ALL_IN, False otherwise.
        """
        return self.status in [PlayerStatus.ACTIVE, PlayerStatus.ALL_IN]
    
    def reset_for_new_hand(self) -> None:
        """
        Reset player for a new hand.
        
        Restores ACTIVE status, clears round data, and resets bets.
        Does NOT reset stack (chips are preserved).
        """
        if self.stack > 0:
            self.status = PlayerStatus.ACTIVE
        self.clear_round_data()
    
    def __repr__(self) -> str:
        """Return string representation of player state."""
        return (
            f"PlayerState(id={self.player_id}, seat={self.seat_number}, "
            f"stack={self.stack}, bet={self.current_bet}, "
            f"status={self.status.value})"
        )
