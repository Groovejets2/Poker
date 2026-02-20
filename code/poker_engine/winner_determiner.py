"""Winner determination and pot distribution logic."""

from typing import List, Dict, Optional
from poker_engine.hand_evaluator import HandEvaluator
from poker_engine.player_state import PlayerState, PlayerStatus


class WinnerDeterminer:
    """Determines winners of pots and distributes winnings."""
    
    def __init__(self, hand_evaluator: HandEvaluator):
        """
        Initialise winner determiner.
        
        Args:
            hand_evaluator (HandEvaluator): Evaluator for comparing hands.
        """
        self.hand_evaluator = hand_evaluator
    
    def determine_winners(
        self,
        remaining_players: List[PlayerState],
        main_pot: int,
        side_pots: List[Dict],
        community_cards: List
    ) -> Dict[str, int]:
        """
        Determine winners for all pots and calculate winnings.
        
        Args:
            remaining_players (List[PlayerState]): Players still in the hand.
            main_pot (int): Amount in the main pot.
            side_pots (List[Dict]): Side pots with structure:
                [{'amount': int, 'eligible_players': [player_ids]}]
            community_cards (List): Community cards (for hand evaluation).
        
        Returns:
            Dict[str, int]: Winnings per player_id (may be 0 for losers).
        """
        # Initialise winnings tracker
        winnings = {player.player_id: 0 for player in remaining_players}
        
        # Build quick lookup for players
        players_by_id = {p.player_id: p for p in remaining_players}
        
        # Only evaluate hands for non-folded players
        active_players = [p for p in remaining_players if p.status != PlayerStatus.FOLDED]
        
        # If only one player remains, they win everything
        if len(active_players) == 1:
            winner_id = active_players[0].player_id
            total_pot = main_pot + sum(pot['amount'] for pot in side_pots)
            winnings[winner_id] = total_pot
            return winnings
        
        # Evaluate hands for remaining players
        player_hands = {}
        for player in active_players:
            try:
                hand = player.hole_cards + community_cards
                # Use best 5-card hand
                hand = hand[:5]  # Take first 5 (dealer should have selected best)
                evaluation = self.hand_evaluator.evaluate(hand)
                player_hands[player.player_id] = {
                    'hand': hand,
                    'evaluation': evaluation,
                    'strength': evaluation['strength']
                }
            except ValueError:
                # Skip players with incomplete hands
                continue
        
        # Distribute main pot
        self._distribute_pot(
            main_pot,
            active_players,
            player_hands,
            None,  # Main pot: all active players eligible
            winnings
        )
        
        # Distribute side pots
        for side_pot in side_pots:
            eligible_ids = side_pot['eligible_players']
            eligible_players = [
                p for p in active_players if p.player_id in eligible_ids
            ]
            
            self._distribute_pot(
                side_pot['amount'],
                eligible_players,
                player_hands,
                eligible_ids,
                winnings
            )
        
        return winnings
    
    def _distribute_pot(
        self,
        pot_amount: int,
        eligible_players: List[PlayerState],
        player_hands: Dict,
        eligible_ids: Optional[List[str]],
        winnings: Dict[str, int]
    ) -> None:
        """
        Distribute a single pot among eligible winners.
        
        Handles ties by splitting the pot equally.
        Only compares hands of eligible players in this pot.
        
        Args:
            pot_amount (int): Amount to distribute.
            eligible_players (List[PlayerState]): Players eligible for this pot.
            player_hands (Dict): Evaluated hands for all active players.
            eligible_ids (Optional[List[str]]): Explicit list of eligible player IDs.
            winnings (Dict[str, int]): Winnings tracker to update.
        """
        if not eligible_players or pot_amount == 0:
            return
        
        # Filter to only eligible players with valid hands
        valid_players = [
            p for p in eligible_players
            if p.player_id in player_hands
        ]
        
        if not valid_players:
            # All eligible players folded, split among remaining
            split_amount = pot_amount // len(eligible_players)
            for player in eligible_players:
                winnings[player.player_id] += split_amount
            return
        
        # Find best hand(s)
        best_strength = max(
            player_hands[p.player_id]['strength'] for p in valid_players
        )
        
        # Get all winners (in case of tie)
        winners = [
            p for p in valid_players
            if player_hands[p.player_id]['strength'] == best_strength
        ]
        
        # Split pot among winners
        split_amount = pot_amount // len(winners)
        remainder = pot_amount % len(winners)
        
        for i, winner in enumerate(winners):
            # Give remainder chips to first winner
            extra = 1 if i < remainder else 0
            winnings[winner.player_id] += split_amount + extra
    
    def get_hand_summary(
        self,
        player: PlayerState,
        community_cards: List
    ) -> Optional[Dict]:
        """
        Get a summary of a player's final hand.
        
        Args:
            player (PlayerState): The player to evaluate.
            community_cards (List): Community cards.
        
        Returns:
            Optional[Dict]: Hand evaluation with name and rank, or None if error.
        """
        if not player.hole_cards:
            return None
        
        try:
            hand = player.hole_cards + community_cards
            hand = hand[:5]
            evaluation = self.hand_evaluator.evaluate(hand)
            return {
                'player_id': player.player_id,
                'hand_name': evaluation['name'],
                'hand_rank': evaluation['rank'],
                'strength': evaluation['strength'],
                'cards': [str(c) for c in hand]
            }
        except ValueError:
            return None
