"""Hand evaluation logic for poker hands."""

from poker_engine.card import Card


class HandEvaluator:
    """Evaluates and ranks poker hands."""
    
    # Hand ranks (higher is better)
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10
    
    HAND_NAMES = {
        1: "High Card",
        2: "One Pair",
        3: "Two Pair",
        4: "Three of a Kind",
        5: "Straight",
        6: "Flush",
        7: "Full House",
        8: "Four of a Kind",
        9: "Straight Flush",
        10: "Royal Flush",
    }
    
    def __init__(self):
        """Initialise HandEvaluator."""
        pass
    
    def evaluate(self, cards):
        """
        Evaluate a 5-card poker hand.
        
        Args:
            cards (list): List of 5 Card objects
            
        Returns:
            dict: {
                'rank': int (1-10),
                'name': str,
                'kickers': list of Card objects in order,
                'strength': int (for comparison)
            }
            
        Raises:
            ValueError: If not exactly 5 cards provided
        """
        if len(cards) != 5:
            raise ValueError(f"Expected 5 cards, got {len(cards)}")
        
        cards = sorted(cards, key=lambda c: c.get_rank_value())
        
        # Check hand types in order of strength
        if self._is_royal_flush(cards):
            return {
                'rank': self.ROYAL_FLUSH,
                'name': self.HAND_NAMES[self.ROYAL_FLUSH],
                'kickers': cards,
                'strength': self._calculate_strength(self.ROYAL_FLUSH, cards)
            }
        
        if self._is_straight_flush(cards):
            return {
                'rank': self.STRAIGHT_FLUSH,
                'name': self.HAND_NAMES[self.STRAIGHT_FLUSH],
                'kickers': cards,
                'strength': self._calculate_strength(self.STRAIGHT_FLUSH, cards)
            }
        
        if self._is_four_of_a_kind(cards):
            kickers = self._get_kickers_four_of_a_kind(cards)
            return {
                'rank': self.FOUR_OF_A_KIND,
                'name': self.HAND_NAMES[self.FOUR_OF_A_KIND],
                'kickers': kickers,
                'strength': self._calculate_strength(self.FOUR_OF_A_KIND, cards)
            }
        
        if self._is_full_house(cards):
            kickers = self._get_kickers_full_house(cards)
            return {
                'rank': self.FULL_HOUSE,
                'name': self.HAND_NAMES[self.FULL_HOUSE],
                'kickers': kickers,
                'strength': self._calculate_strength(self.FULL_HOUSE, cards)
            }
        
        if self._is_flush(cards):
            kickers = sorted(cards, key=lambda c: c.get_rank_value(), reverse=True)
            return {
                'rank': self.FLUSH,
                'name': self.HAND_NAMES[self.FLUSH],
                'kickers': kickers,
                'strength': self._calculate_strength(self.FLUSH, cards)
            }
        
        if self._is_straight(cards):
            kickers = self._get_kickers_straight(cards)
            return {
                'rank': self.STRAIGHT,
                'name': self.HAND_NAMES[self.STRAIGHT],
                'kickers': kickers,
                'strength': self._calculate_strength(self.STRAIGHT, cards)
            }
        
        if self._is_three_of_a_kind(cards):
            kickers = self._get_kickers_three_of_a_kind(cards)
            return {
                'rank': self.THREE_OF_A_KIND,
                'name': self.HAND_NAMES[self.THREE_OF_A_KIND],
                'kickers': kickers,
                'strength': self._calculate_strength(self.THREE_OF_A_KIND, cards)
            }
        
        if self._is_two_pair(cards):
            kickers = self._get_kickers_two_pair(cards)
            return {
                'rank': self.TWO_PAIR,
                'name': self.HAND_NAMES[self.TWO_PAIR],
                'kickers': kickers,
                'strength': self._calculate_strength(self.TWO_PAIR, cards)
            }
        
        if self._is_one_pair(cards):
            kickers = self._get_kickers_one_pair(cards)
            return {
                'rank': self.ONE_PAIR,
                'name': self.HAND_NAMES[self.ONE_PAIR],
                'kickers': kickers,
                'strength': self._calculate_strength(self.ONE_PAIR, cards)
            }
        
        # High card
        kickers = sorted(cards, key=lambda c: c.get_rank_value(), reverse=True)
        return {
            'rank': self.HIGH_CARD,
            'name': self.HAND_NAMES[self.HIGH_CARD],
            'kickers': kickers,
            'strength': self._calculate_strength(self.HIGH_CARD, cards)
        }
    
    def compare_hands(self, hand1, hand2):
        """
        Compare two 5-card hands.
        
        Args:
            hand1 (list): List of 5 Card objects
            hand2 (list): List of 5 Card objects
            
        Returns:
            int: -1 if hand1 loses, 0 if tie, 1 if hand1 wins
        """
        eval1 = self.evaluate(hand1)
        eval2 = self.evaluate(hand2)
        
        if eval1['rank'] > eval2['rank']:
            return 1
        elif eval1['rank'] < eval2['rank']:
            return -1
        else:
            # Same rank, compare kickers
            for k1, k2 in zip(eval1['kickers'], eval2['kickers']):
                if k1.get_rank_value() > k2.get_rank_value():
                    return 1
                elif k1.get_rank_value() < k2.get_rank_value():
                    return -1
            return 0
    
    # --- Helper methods ---
    
    def _is_flush(self, cards):
        """Check if all cards have same suit."""
        return len(set(c.suit for c in cards)) == 1
    
    def _is_straight(self, cards):
        """Check if cards form a straight."""
        values = [c.get_rank_value() for c in cards]
        values.sort()
        
        # Check normal straight
        if values == list(range(values[0], values[0] + 5)):
            return True
        
        # Check for A-2-3-4-5 (wheel)
        if values == [0, 1, 2, 3, 12]:
            return True
        
        return False
    
    def _is_royal_flush(self, cards):
        """Check for royal flush (A-K-Q-J-10, same suit)."""
        if not self._is_flush(cards):
            return False
        
        values = sorted([c.get_rank_value() for c in cards])
        return values == [8, 9, 10, 11, 12]
    
    def _is_straight_flush(self, cards):
        """Check for straight flush."""
        return self._is_flush(cards) and self._is_straight(cards)
    
    def _is_four_of_a_kind(self, cards):
        """Check for four of a kind."""
        ranks = [c.rank for c in cards]
        return any(ranks.count(rank) == 4 for rank in set(ranks))
    
    def _is_full_house(self, cards):
        """Check for full house."""
        ranks = [c.rank for c in cards]
        counts = [ranks.count(rank) for rank in set(ranks)]
        return sorted(counts) == [2, 3]
    
    def _is_three_of_a_kind(self, cards):
        """Check for three of a kind."""
        ranks = [c.rank for c in cards]
        return any(ranks.count(rank) == 3 for rank in set(ranks))
    
    def _is_two_pair(self, cards):
        """Check for two pair."""
        ranks = [c.rank for c in cards]
        pairs = sum(1 for rank in set(ranks) if ranks.count(rank) == 2)
        return pairs == 2
    
    def _is_one_pair(self, cards):
        """Check for one pair."""
        ranks = [c.rank for c in cards]
        return any(ranks.count(rank) == 2 for rank in set(ranks))
    
    def _get_kickers_one_pair(self, cards):
        """Get kickers for one pair hand."""
        ranks = [c.rank for c in cards]
        pair_rank = None
        for rank in set(ranks):
            if ranks.count(rank) == 2:
                pair_rank = rank
                break
        
        pair_cards = [c for c in cards if c.rank == pair_rank]
        kicker_cards = sorted([c for c in cards if c.rank != pair_rank],
                             key=lambda c: c.get_rank_value(), reverse=True)
        return pair_cards + kicker_cards
    
    def _get_kickers_two_pair(self, cards):
        """Get kickers for two pair hand."""
        ranks = [c.rank for c in cards]
        pairs = [rank for rank in set(ranks) if ranks.count(rank) == 2]
        pairs.sort(key=lambda r: Card.RANK_VALUES[r], reverse=True)
        
        pair1_cards = [c for c in cards if c.rank == pairs[0]]
        pair2_cards = [c for c in cards if c.rank == pairs[1]]
        kicker_cards = [c for c in cards if c.rank not in pairs]
        
        return pair1_cards + pair2_cards + kicker_cards
    
    def _get_kickers_three_of_a_kind(self, cards):
        """Get kickers for three of a kind hand."""
        ranks = [c.rank for c in cards]
        trip_rank = None
        for rank in set(ranks):
            if ranks.count(rank) == 3:
                trip_rank = rank
                break
        
        trip_cards = [c for c in cards if c.rank == trip_rank]
        kicker_cards = sorted([c for c in cards if c.rank != trip_rank],
                             key=lambda c: c.get_rank_value(), reverse=True)
        return trip_cards + kicker_cards
    
    def _get_kickers_straight(self, cards):
        """Get kickers for straight hand (high card of straight)."""
        values = [c.get_rank_value() for c in cards]
        values.sort()
        
        # A-2-3-4-5 special case (wheel)
        if values == [0, 1, 2, 3, 12]:
            return sorted(cards, key=lambda c: c.get_rank_value())[::-1]
        
        return sorted(cards, key=lambda c: c.get_rank_value(), reverse=True)
    
    def _get_kickers_full_house(self, cards):
        """Get kickers for full house hand."""
        ranks = [c.rank for c in cards]
        three_rank = None
        two_rank = None
        
        for rank in set(ranks):
            if ranks.count(rank) == 3:
                three_rank = rank
            elif ranks.count(rank) == 2:
                two_rank = rank
        
        three_cards = [c for c in cards if c.rank == three_rank]
        two_cards = [c for c in cards if c.rank == two_rank]
        return three_cards + two_cards
    
    def _get_kickers_four_of_a_kind(self, cards):
        """Get kickers for four of a kind hand."""
        ranks = [c.rank for c in cards]
        four_rank = None
        for rank in set(ranks):
            if ranks.count(rank) == 4:
                four_rank = rank
                break
        
        four_cards = [c for c in cards if c.rank == four_rank]
        kicker_cards = [c for c in cards if c.rank != four_rank]
        return four_cards + kicker_cards
    
    def _calculate_strength(self, hand_rank, cards):
        """
        Calculate a numeric strength value for comparison.
        
        Args:
            hand_rank (int): The rank of the hand (1-10)
            cards (list): List of Card objects
            
        Returns:
            int: A unique strength value for this hand
        """
        # Base strength is hand rank * large number
        strength = hand_rank * 100000
        
        # Add kicker values
        for i, card in enumerate(sorted(cards, key=lambda c: c.get_rank_value(), reverse=True)):
            strength += card.get_rank_value() * (10 ** (2 - i))
        
        return strength
