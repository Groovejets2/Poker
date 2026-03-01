"""Pot management for the dealer engine."""

from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class Pot:
    """
    Represents a single pot in the game.
    
    A pot tracks the total chips and which players are eligible to win it.
    The main pot includes equal contributions from all active players.
    Side pots are created when players go all-in with fewer chips.
    
    Attributes:
        amount (int): Total chips in this pot.
        eligible_players (List[str]): Player IDs who contributed and can win.
    """
    
    def __init__(self, amount: int, eligible_players: List[str]):
        """
        Initialise a pot.
        
        Args:
            amount (int): Initial chips in pot (must be non-negative).
            eligible_players (List[str]): Player IDs eligible for this pot.
        
        Raises:
            ValueError: If amount < 0 or eligible_players is empty.
        """
        if amount < 0:
            raise ValueError(f"Pot amount cannot be negative: {amount}")
        if not eligible_players:
            raise ValueError("Pot must have at least one eligible player")
        
        self.amount = amount
        self.eligible_players = eligible_players.copy()
    
    def add(self, chips: int) -> None:
        """
        Add chips to this pot.
        
        Args:
            chips (int): Chips to add (must be non-negative).
        
        Raises:
            ValueError: If chips < 0.
        """
        if chips < 0:
            raise ValueError(f"Cannot add negative chips: {chips}")
        self.amount += chips
    
    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"Pot(amount={self.amount}, "
            f"eligible_players={len(self.eligible_players)})"
        )


class PotManager:
    """
    Manages main pot and side pots during a hand.
    
    Tracks player contributions and creates side pots when players go all-in.
    
    Attributes:
        main_pot (Pot): Main pot accessible to all active players.
        side_pots (List[Pot]): Side pots for all-in scenarios.
        player_contributions (Dict[str, int]): Total chips each player has contributed.
        all_in_amounts (Dict[str, int]): Stack size when each player went all-in.
    """
    
    def __init__(self, active_player_ids: List[str]):
        """
        Initialise the pot manager for a hand.
        
        Args:
            active_player_ids (List[str]): IDs of all active players at start of hand.
        
        Raises:
            ValueError: If active_player_ids is empty.
        """
        if not active_player_ids:
            raise ValueError("Must have at least one active player")
        
        self.main_pot = Pot(0, active_player_ids.copy())
        self.side_pots: List[Pot] = []
        self.player_contributions: Dict[str, int] = {
            player_id: 0 for player_id in active_player_ids
        }
        self.all_in_amounts: Dict[str, int] = {}
    
    def add_to_pot(self, player_id: str, amount: int) -> None:
        """
        Add chips to the appropriate pot from a player.
        
        Chips go to the main pot first. When a player is all-in, chips beyond
        their all-in amount create side pots.
        
        Args:
            player_id (str): ID of player adding chips.
            amount (int): Chips to add.
        
        Raises:
            ValueError: If amount < 0 or player_id not in game.
        """
        if amount < 0:
            raise ValueError(f"Cannot add negative chips: {amount}")
        if player_id not in self.player_contributions:
            raise ValueError(f"Player {player_id} not in this game")
        
        # Track total contribution
        self.player_contributions[player_id] += amount
        
        # Add to main pot (simple case: chips go to main pot)
        self.main_pot.add(amount)
    
    def set_all_in(self, player_id: str, remaining_stack: int) -> None:
        """
        Mark a player as all-in and record their maximum winning amount.
        
        When a player goes all-in, they can only win up to their contribution.
        Side pots are calculated after the hand to determine eligible winners.
        
        Args:
            player_id (str): ID of player going all-in.
            remaining_stack (int): Chips player had left before final all-in bet.
        
        Raises:
            ValueError: If player_id not in game.
        """
        if player_id not in self.player_contributions:
            raise ValueError(f"Player {player_id} not in this game")
        
        # Record total contributed amount as their all-in limit
        self.all_in_amounts[player_id] = self.player_contributions[player_id]
    
    def calculate_side_pots(self) -> None:
        """
        Create side pots based on all-in amounts.
        
        When multiple players have different all-in amounts, side pots ensure
        that only eligible players can win. For example:
        
        - Player A: contributes 50 (all-in)
        - Player B: contributes 100
        - Player C: contributes 100
        
        Main pot: 50 × 3 = 150 (everyone eligible)
        Side pot 1: 50 × 2 = 100 (B and C only)
        
        Side pots are created in order of contribution amounts.
        """
        if not self.all_in_amounts:
            # No all-ins: everything stays in main pot
            return
        
        # Get unique all-in amounts, sorted low to high
        sorted_amounts = sorted(set(self.all_in_amounts.values()))
        
        # Move chips from main pot to side pots
        # For each all-in level, create a side pot
        previous_level = 0
        
        for all_in_level in sorted_amounts:
            # Chips contributed between previous level and this level
            chips_per_player = all_in_level - previous_level
            
            # Count how many players contributed at least this much
            eligible = [
                player_id for player_id, contributed in self.player_contributions.items()
                if contributed >= all_in_level
            ]
            
            if eligible:
                side_pot_amount = chips_per_player * len(eligible)
                # Move chips from main pot into this side pot to prevent
                # double-counting in get_pot_total().
                self.main_pot.amount -= side_pot_amount
                side_pot = Pot(side_pot_amount, eligible)
                self.side_pots.append(side_pot)
            
            previous_level = all_in_level
    
    def get_pot_total(self) -> int:
        """
        Get the total of all pots in the game.
        
        Returns:
            int: Sum of main pot and all side pots.
        """
        total = self.main_pot.amount
        for side_pot in self.side_pots:
            total += side_pot.amount
        return total
    
    def get_main_pot(self) -> int:
        """
        Get the main pot amount.
        
        Returns:
            int: Chips in main pot.
        """
        return self.main_pot.amount
    
    def get_side_pots(self) -> List[Dict[str, any]]:
        """
        Get information about all side pots.
        
        Returns:
            List[Dict]: List of dicts with 'amount' and 'eligible_players' keys.
        """
        return [
            {
                "amount": pot.amount,
                "eligible_players": pot.eligible_players.copy()
            }
            for pot in self.side_pots
        ]
    
    def get_all_pots(self) -> Dict[str, any]:
        """
        Get complete pot structure.
        
        Returns:
            Dict: Contains 'main_pot', 'side_pots', and 'total'.
        """
        return {
            "main_pot": self.main_pot.amount,
            "side_pots": self.get_side_pots(),
            "total": self.get_pot_total()
        }
    
    def get_player_contribution(self, player_id: str) -> int:
        """
        Get total chips contributed by a player this hand.
        
        Args:
            player_id (str): Player's ID.
        
        Returns:
            int: Total contribution amount.
        
        Raises:
            ValueError: If player_id not in game.
        """
        if player_id not in self.player_contributions:
            raise ValueError(f"Player {player_id} not in this game")
        return self.player_contributions[player_id]
    
    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"PotManager(main_pot={self.main_pot.amount}, "
            f"side_pots={len(self.side_pots)}, "
            f"total={self.get_pot_total()})"
        )
