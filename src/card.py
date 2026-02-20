"""Card representation and utilities."""

class Card:
    """Represents a single playing card."""
    
    # Suit constants
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"
    
    SUITS = [HEARTS, DIAMONDS, CLUBS, SPADES]
    
    # Rank constants (ordered by value, lowest to highest)
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    RANK_VALUES = {rank: i for i, rank in enumerate(RANKS)}
    
    def __init__(self, suit, rank):
        """
        Initialise a Card.
        
        Args:
            suit (str): One of HEARTS, DIAMONDS, CLUBS, SPADES
            rank (str): One of 2-10, J, Q, K, A
            
        Raises:
            ValueError: If suit or rank is invalid
        """
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank: {rank}")
        
        self.suit = suit
        self.rank = rank
    
    def __eq__(self, other):
        """Check equality with another Card."""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        """Return hash for use in sets/dicts."""
        return hash((self.suit, self.rank))
    
    def __repr__(self):
        """Return string representation."""
        return f"{self.rank}{self.suit[0].upper()}"
    
    def __str__(self):
        """Return human-readable string."""
        return f"{self.rank} of {self.suit}"
    
    def get_rank_value(self):
        """
        Get numeric value of the rank.
        
        Returns:
            int: 0-12 (2=0, 3=1, ..., A=12)
        """
        return self.RANK_VALUES[self.rank]
