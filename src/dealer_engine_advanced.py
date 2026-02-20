"""
Advanced dealer engine features: side pot management and winner determination.

This module extends the base dealer engine with:
- Side pot creation and management
- Hand ranking and comparison
- Winner determination with pot distribution
- Tie handling

Author: Angus Young
Date: 2026-02-21
Version: 1.0
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from src.dealer_engine import DealerEngine, Player, Pot, Card
from src.hand_evaluator import HandEvaluator


@dataclass
class PotContribution:
    """Tracks how much each player contributed to a specific amount."""
    amount: int
    contributors: Dict[str, int]  # player_id -> amount contributed at this level


class SidePotManager:
    """
    Manages creation and distribution of side pots.
    
    When a player goes all-in with fewer chips than others, side pots are created
    to ensure fair betting and pot distribution.
    """
    
    @staticmethod
    def create_side_pots(
        engine: DealerEngine,
        active_players: List[Player]
    ) -> Tuple[Pot, List[Pot]]:
        """
        Create main pot and side pots based on player stacks and bets.
        
        Algorithm:
        1. Sort unique bet amounts
        2. For each amount, create a pot level
        3. Only players who bet at that level can win that pot
        
        Args:
            engine: The dealer engine
            active_players: Players still in the hand (not folded)
            
        Returns:
            (main_pot, side_pots)
        """
        # Collect all unique bet levels
        bet_levels = sorted(set(p.current_bet_in_round for p in active_players))
        
        if not bet_levels:
            return Pot(0, []), []
        
        main_pot = Pot(0, [])
        side_pots = []
        previous_level = 0
        
        for level in bet_levels:
            bet_increment = level - previous_level
            
            # Determine which players contributed at this level
            contributors = [
                p.player_id for p in active_players
                if p.current_bet_in_round >= level
            ]
            
            if not contributors:
                previous_level = level
                continue
            
            # Calculate pot amount for this level
            pot_amount = bet_increment * len([p for p in active_players if p.is_active])
            
            if previous_level == 0:
                # This is the main pot
                main_pot.amount = pot_amount
                main_pot.contributors = contributors
            else:
                # This is a side pot
                side_pot = Pot(pot_amount, contributors)
                side_pots.append(side_pot)
            
            previous_level = level
        
        return main_pot, side_pots
    
    @staticmethod
    def is_side_pot_winner(
        player_id: str,
        pot: Pot
    ) -> bool:
        """
        Check if a player is eligible to win a specific pot.
        
        A player can only win a pot if they contributed to it.
        """
        return player_id in pot.contributors


class WinnerDeterminer:
    """
    Determines winners and distributes pots.
    
    Responsibilities:
    - Rank hands using HandEvaluator
    - Compare hands
    - Determine winners for each pot
    - Handle ties (split pots)
    - Distribute chips to winners
    """
    
    def __init__(self, hand_evaluator: Optional[HandEvaluator] = None):
        """
        Initialize winner determiner.
        
        Args:
            hand_evaluator: HandEvaluator instance (if None, creates one)
        """
        self.hand_evaluator = hand_evaluator or HandEvaluator()
    
    def determine_hand_winner(
        self,
        active_players: List[Player],
        community_cards: List[Card]
    ) -> Tuple[List[str], int]:
        """
        Determine the winner(s) of a hand.
        
        Args:
            active_players: Players still in the hand
            community_cards: Community cards (Texas Hold'em)
            
        Returns:
            (winning_player_ids, hand_rank_score)
        """
        if len(active_players) == 1:
            # Only one player left, they win
            return [active_players[0].player_id], 0
        
        # Evaluate each player's hand
        hand_rankings = {}
        for player in active_players:
            if player.status.value == "folded":
                continue
            
            # Combine hole cards with community cards
            all_cards = player.hole_cards + community_cards
            
            # Evaluate best 5-card hand from 7 cards
            eval_result = self.hand_evaluator.evaluate_best_hand(all_cards)
            rank = eval_result['rank']
            strength = eval_result['strength']
            hand_rankings[player.player_id] = (rank, strength)
        
        if not hand_rankings:
            return [active_players[0].player_id], 0
        
        # Find best hand(s)
        best_strength = max(strength for _, strength in hand_rankings.values())
        winners = [
            pid for pid, (_, strength) in hand_rankings.items()
            if strength == best_strength
        ]
        
        return winners, best_strength
    
    def distribute_pot(
        self,
        pot: Pot,
        winners: List[str],
        player_dict: Dict[str, Player]
    ) -> Dict[str, int]:
        """
        Distribute a pot among winners.
        
        If multiple winners, split evenly with remainder going to earliest position.
        
        Args:
            pot: Pot to distribute
            winners: List of winning player IDs
            player_dict: Dict of player_id -> Player
            
        Returns:
            Distribution dict: {player_id: amount_won}
        """
        distribution = {}
        
        # Filter winners to only those eligible for this pot
        eligible_winners = [w for w in winners if w in pot.contributors]
        
        if not eligible_winners:
            # No eligible winner, return pot (shouldn't happen)
            return distribution
        
        # Calculate split
        share = pot.amount // len(eligible_winners)
        remainder = pot.amount % len(eligible_winners)
        
        for winner in eligible_winners:
            distribution[winner] = share
        
        # Give remainder to first winner in position order
        if remainder > 0 and eligible_winners:
            distribution[eligible_winners[0]] += remainder
        
        return distribution
    
    def distribute_all_pots(
        self,
        main_pot: Pot,
        side_pots: List[Pot],
        winners: List[str],
        player_dict: Dict[str, Player]
    ) -> Dict[str, int]:
        """
        Distribute all pots to winners.
        
        Args:
            main_pot: Main pot
            side_pots: List of side pots
            winners: List of winning player IDs
            player_dict: Dict of player_id -> Player
            
        Returns:
            Total distribution: {player_id: total_amount_won}
        """
        total_distribution = {}
        
        # Distribute main pot
        main_dist = self.distribute_pot(main_pot, winners, player_dict)
        for pid, amount in main_dist.items():
            total_distribution[pid] = total_distribution.get(pid, 0) + amount
        
        # Distribute each side pot
        for side_pot in side_pots:
            side_dist = self.distribute_pot(side_pot, winners, player_dict)
            for pid, amount in side_dist.items():
                total_distribution[pid] = total_distribution.get(pid, 0) + amount
        
        return total_distribution
    
    def award_winnings(
        self,
        distribution: Dict[str, int],
        players: List[Player]
    ) -> None:
        """
        Award winnings to players (credit their stacks).
        
        Args:
            distribution: {player_id: amount_won}
            players: List of all players
        """
        player_dict = {p.player_id: p for p in players}
        
        for player_id, amount in distribution.items():
            if player_id in player_dict:
                player_dict[player_id].current_stack += amount


class DealerEngineWithWinners(DealerEngine):
    """
    Extended dealer engine with winner determination and pot distribution.
    
    Combines base engine with side pot and winner determination logic.
    """
    
    def __init__(self, game_type, players, small_blind, big_blind, hand_evaluator=None):
        """Initialize with optional custom hand evaluator."""
        super().__init__(game_type, players, small_blind, big_blind)
        self.side_pot_manager = SidePotManager()
        self.winner_determiner = WinnerDeterminer(hand_evaluator)
    
    def finalize_hand(self, community_cards: List[Card]) -> Dict[str, int]:
        """
        Determine winner(s) and distribute pot(s).
        
        Args:
            community_cards: Community cards for hand evaluation
            
        Returns:
            Distribution: {player_id: amount_won}
        """
        # Get active players
        active_players = [
            p for p in self.players
            if p.player_id in self.players_in_hand and p.status.value != "folded"
        ]
        
        if len(active_players) == 1:
            # Everyone folded, winner takes all
            winner_id = active_players[0].player_id
            distribution = {winner_id: self.main_pot.amount}
        else:
            # Determine winner
            winners, _ = self.winner_determiner.determine_hand_winner(
                active_players, community_cards
            )
            
            # Create side pots if needed
            main_pot, side_pots = self.side_pot_manager.create_side_pots(
                self, active_players
            )
            self.main_pot = main_pot
            self.side_pots = side_pots
            
            # Distribute pots
            player_dict = {p.player_id: p for p in self.players}
            distribution = self.winner_determiner.distribute_all_pots(
                main_pot, side_pots, winners, player_dict
            )
        
        # Award winnings
        player_dict = {p.player_id: p for p in self.players}
        self.winner_determiner.award_winnings(distribution, self.players)
        
        return distribution
