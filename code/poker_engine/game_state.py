"""Game state representation for the dealer engine."""

from enum import Enum
from typing import List, Optional, Dict
from poker_engine.card import Card
from poker_engine.player_state import PlayerState, PlayerStatus


class GamePhase(Enum):
    """Phases of a poker hand."""
    
    WAITING_FOR_PLAYERS = "WAITING_FOR_PLAYERS"
    """Awaiting players to join the table."""
    
    GAME_STARTED = "GAME_STARTED"
    """All players seated, game beginning."""
    
    BLINDS_POSTED = "BLINDS_POSTED"
    """Small and big blinds have been posted."""
    
    PRE_FLOP = "PRE_FLOP"
    """First betting round (Texas Hold'em) or initial betting (5-card draw)."""
    
    FLOP = "FLOP"
    """Texas Hold'em only: 3 community cards revealed."""
    
    TURN = "TURN"
    """Texas Hold'em only: 4th community card revealed."""
    
    RIVER = "RIVER"
    """Texas Hold'em only: 5th community card revealed."""
    
    SHOWDOWN = "SHOWDOWN"
    """All remaining active players reveal hands."""
    
    POT_DISTRIBUTION = "POT_DISTRIBUTION"
    """Winners determined, pot being distributed."""
    
    HAND_COMPLETE = "HAND_COMPLETE"
    """Hand finished, preparing for next hand."""


class SidePot:
    """
    Represents a side pot in the game.
    
    A side pot is created when a player goes all-in with fewer chips than others.
    Each side pot can only be won by players who contributed to it.
    
    Attributes:
        amount (int): Total chips in this side pot.
        eligible_players (List[str]): Player IDs who can win this pot.
    """
    
    def __init__(self, amount: int, eligible_players: List[str]):
        """
        Initialise a side pot.
        
        Args:
            amount (int): Total chips in pot (must be positive).
            eligible_players (List[str]): List of player IDs who contributed.
        
        Raises:
            ValueError: If amount <= 0 or eligible_players is empty.
        """
        if amount <= 0:
            raise ValueError(f"Side pot amount must be positive, got {amount}")
        if not eligible_players:
            raise ValueError("Side pot must have at least one eligible player")
        
        self.amount = amount
        self.eligible_players = eligible_players.copy()
    
    def __repr__(self) -> str:
        """Return string representation of side pot."""
        return f"SidePot(amount={self.amount}, players={len(self.eligible_players)})"


class GameState:
    """
    Represents the state of the entire game.
    
    This class tracks all information about an active poker game: which players
    are seated, what phase the hand is in, the pot(s), community cards, and
    whose turn it is to act. It is updated by the dealer engine as the hand
    progresses.
    
    Attributes:
        game_id (str): Unique identifier for this game.
        players (List[PlayerState]): Array of 2-8 players at the table.
        current_phase (GamePhase): Current phase of the hand.
        current_action_player (Optional[int]): Seat number of player to act.
        main_pot (int): Chips in the main pot (accessible to all).
        side_pots (List[SidePot]): Side pots for all-in scenarios.
        community_cards (List[Card]): Shared cards (Texas Hold'em only).
        dealer_button (int): Seat number of the dealer.
        small_blind_amount (int): Small blind bet amount.
        big_blind_amount (int): Big blind bet amount.
    """
    
    def __init__(
        self,
        game_id: str,
        players: List[PlayerState],
        small_blind_amount: int,
        big_blind_amount: int,
        dealer_button: int = 0,
    ):
        """
        Initialise a game.
        
        Args:
            game_id (str): Unique identifier for this game.
            players (List[PlayerState]): List of 2-8 players at the table.
            small_blind_amount (int): Small blind amount (must be positive).
            big_blind_amount (int): Big blind amount (must be > small blind).
            dealer_button (int): Initial dealer seat (default: 0).
        
        Raises:
            ValueError: If player count not in range 2-8, blind amounts invalid,
                       or dealer_button out of range.
        """
        if not 2 <= len(players) <= 8:
            raise ValueError(f"Game must have 2-8 players, got {len(players)}")
        
        if small_blind_amount <= 0:
            raise ValueError(
                f"Small blind must be positive, got {small_blind_amount}"
            )
        
        if big_blind_amount <= small_blind_amount:
            raise ValueError(
                f"Big blind {big_blind_amount} must be > small blind {small_blind_amount}"
            )
        
        if not 0 <= dealer_button < len(players):
            raise ValueError(
                f"Dealer button {dealer_button} out of range 0-{len(players)-1}"
            )
        
        self.game_id = game_id
        self.players = players
        self.current_phase = GamePhase.WAITING_FOR_PLAYERS
        self.current_action_player: Optional[int] = None
        self.main_pot = 0
        self.side_pots: List[SidePot] = []
        self.community_cards: List[Card] = []
        self.dealer_button = dealer_button
        self.small_blind_amount = small_blind_amount
        self.big_blind_amount = big_blind_amount
    
    def add_to_main_pot(self, amount: int) -> None:
        """
        Add chips to the main pot.
        
        Args:
            amount (int): Chips to add (must be non-negative).
        
        Raises:
            ValueError: If amount < 0.
        """
        if amount < 0:
            raise ValueError(f"Pot amount cannot be negative: {amount}")
        self.main_pot += amount
    
    def create_side_pot(self, amount: int, eligible_players: List[str]) -> None:
        """
        Create a new side pot.
        
        Called when a player goes all-in with fewer chips than others.
        
        Args:
            amount (int): Chips in this side pot.
            eligible_players (List[str]): Player IDs who contributed.
        
        Raises:
            ValueError: If side pot parameters invalid.
        """
        side_pot = SidePot(amount, eligible_players)
        self.side_pots.append(side_pot)
    
    def get_total_pot(self) -> int:
        """
        Calculate the total pot across main and side pots.
        
        Returns:
            int: Sum of main_pot and all side_pots.
        """
        return self.main_pot + sum(pot.amount for pot in self.side_pots)
    
    def advance_phase(self, new_phase: GamePhase) -> None:
        """
        Move to the next phase.
        
        Args:
            new_phase (GamePhase): The phase to transition to.
        
        Raises:
            ValueError: If new_phase is not a valid GamePhase.
        """
        if not isinstance(new_phase, GamePhase):
            raise ValueError(f"Invalid phase: {new_phase}")
        self.current_phase = new_phase
    
    def reveal_community_card(self, card: Card) -> None:
        """
        Reveal a community card (Texas Hold'em only).
        
        Args:
            card (Card): The card to reveal.
        
        Raises:
            ValueError: If card is not a Card object or too many cards revealed.
        """
        if not isinstance(card, Card):
            raise ValueError(f"Expected Card, got {type(card)}")
        if len(self.community_cards) >= 5:
            raise ValueError(
                f"Cannot reveal more than 5 community cards, already have {len(self.community_cards)}"
            )
        self.community_cards.append(card)
    
    def get_active_players(self) -> List[PlayerState]:
        """
        Get all players who are still active in the hand.
        
        Returns:
            List[PlayerState]: Players with status ACTIVE or ALL_IN.
        """
        return [p for p in self.players if p.is_active_in_hand()]
    
    def get_player_by_id(self, player_id: str) -> Optional[PlayerState]:
        """
        Find a player by their ID.
        
        Args:
            player_id (str): The player's unique identifier.
        
        Returns:
            Optional[PlayerState]: The player, or None if not found.
        """
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def get_player_by_seat(self, seat_number: int) -> Optional[PlayerState]:
        """
        Find a player by their seat number.
        
        Args:
            seat_number (int): The seat (0-7).
        
        Returns:
            Optional[PlayerState]: The player, or None if seat empty.
        """
        if not 0 <= seat_number < len(self.players):
            return None
        return self.players[seat_number]
    
    def get_next_active_seat(self, from_seat: int) -> Optional[int]:
        """
        Find the next active player's seat in clockwise order.
        
        Wraps around from seat 7 back to seat 0.
        Skips folded and sitting-out players.
        
        Args:
            from_seat (int): Starting seat (searches from next seat onwards).
        
        Returns:
            Optional[int]: Next active seat, or None if no active players remain.
        """
        num_seats = len(self.players)
        for offset in range(1, num_seats):
            seat = (from_seat + offset) % num_seats
            player = self.players[seat]
            if player.is_active_in_hand():
                return seat
        return None
    
    def reset_for_new_hand(self) -> None:
        """
        Reset game state for a new hand.
        
        Clears pots, community cards, and resets player states.
        Advances to BLINDS_POSTED phase.
        Moves dealer button to next seat.
        """
        # Reset all players
        for player in self.players:
            player.reset_for_new_hand()
        
        # Reset game pots and cards
        self.main_pot = 0
        self.side_pots = []
        self.community_cards = []
        
        # Advance phase and move button
        self.current_phase = GamePhase.BLINDS_POSTED
        self.current_action_player = None
        self.dealer_button = (self.dealer_button + 1) % len(self.players)
    
    def __repr__(self) -> str:
        """Return string representation of game state."""
        return (
            f"GameState(id={self.game_id}, phase={self.current_phase.value}, "
            f"players={len(self.players)}, pot={self.get_total_pot()}, "
            f"action_player={self.current_action_player})"
        )
