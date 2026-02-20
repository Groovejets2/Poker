"""Tests for HandEvaluator class."""

import pytest
from poker_engine.card import Card
from poker_engine.hand_evaluator import HandEvaluator


class TestHandEvaluatorBasics:
    """Basic tests for hand evaluation."""
    
    @pytest.fixture
    def evaluator(self):
        """Create HandEvaluator instance."""
        return HandEvaluator()
    
    def test_evaluate_high_card(self, evaluator):
        """Test evaluation of high card hand."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "9"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.HIGH_CARD
        assert result['name'] == "High Card"
    
    def test_evaluate_one_pair(self, evaluator):
        """Test evaluation of one pair hand."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.ONE_PAIR
        assert result['name'] == "One Pair"
    
    def test_evaluate_two_pair(self, evaluator):
        """Test evaluation of two pair hand."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "K"),
            Card("hearts", "Q"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.TWO_PAIR
        assert result['name'] == "Two Pair"
    
    def test_evaluate_three_of_a_kind(self, evaluator):
        """Test evaluation of three of a kind."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "K"),
            Card("hearts", "Q"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.THREE_OF_A_KIND
        assert result['name'] == "Three of a Kind"
    
    def test_evaluate_straight(self, evaluator):
        """Test evaluation of straight."""
        cards = [
            Card("hearts", "5"),
            Card("spades", "6"),
            Card("diamonds", "7"),
            Card("clubs", "8"),
            Card("hearts", "9"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.STRAIGHT
        assert result['name'] == "Straight"
    
    def test_evaluate_flush(self, evaluator):
        """Test evaluation of flush."""
        cards = [
            Card("hearts", "A"),
            Card("hearts", "K"),
            Card("hearts", "Q"),
            Card("hearts", "J"),
            Card("hearts", "9"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.FLUSH
        assert result['name'] == "Flush"
    
    def test_evaluate_full_house(self, evaluator):
        """Test evaluation of full house."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "K"),
            Card("hearts", "K"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.FULL_HOUSE
        assert result['name'] == "Full House"
    
    def test_evaluate_four_of_a_kind(self, evaluator):
        """Test evaluation of four of a kind."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "A"),
            Card("hearts", "K"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.FOUR_OF_A_KIND
        assert result['name'] == "Four of a Kind"
    
    def test_evaluate_straight_flush(self, evaluator):
        """Test evaluation of straight flush."""
        cards = [
            Card("hearts", "5"),
            Card("hearts", "6"),
            Card("hearts", "7"),
            Card("hearts", "8"),
            Card("hearts", "9"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.STRAIGHT_FLUSH
        assert result['name'] == "Straight Flush"
    
    def test_evaluate_royal_flush(self, evaluator):
        """Test evaluation of royal flush."""
        cards = [
            Card("hearts", "10"),
            Card("hearts", "J"),
            Card("hearts", "Q"),
            Card("hearts", "K"),
            Card("hearts", "A"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.ROYAL_FLUSH
        assert result['name'] == "Royal Flush"


class TestHandComparison:
    """Tests for hand comparison."""
    
    @pytest.fixture
    def evaluator(self):
        """Create HandEvaluator instance."""
        return HandEvaluator()
    
    def test_compare_pair_beats_high_card(self, evaluator):
        """Test that pair beats high card."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        hand2 = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "9"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_compare_flush_beats_straight(self, evaluator):
        """Test that flush beats straight."""
        hand1 = [
            Card("hearts", "A"),
            Card("hearts", "K"),
            Card("hearts", "Q"),
            Card("hearts", "J"),
            Card("hearts", "9"),
        ]
        hand2 = [
            Card("hearts", "5"),
            Card("spades", "6"),
            Card("diamonds", "7"),
            Card("clubs", "8"),
            Card("hearts", "9"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_compare_identical_hands_tie(self, evaluator):
        """Test that identical hands are a tie."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        hand2 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 0


class TestHandEvaluatorErrors:
    """Test error handling."""
    
    @pytest.fixture
    def evaluator(self):
        """Create HandEvaluator instance."""
        return HandEvaluator()
    
    def test_evaluate_wrong_card_count(self, evaluator):
        """Test that wrong card count raises error."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
        ]
        with pytest.raises(ValueError):
            evaluator.evaluate(cards)


class TestEdgeCases:
    """Edge case tests for hand evaluation and comparison."""
    
    @pytest.fixture
    def evaluator(self):
        """Create HandEvaluator instance."""
        return HandEvaluator()
    
    def test_wheel_straight_ace_low(self, evaluator):
        """Test wheel straight (A-2-3-4-5) — ace acts as low."""
        cards = [
            Card("hearts", "A"),
            Card("spades", "2"),
            Card("diamonds", "3"),
            Card("clubs", "4"),
            Card("hearts", "5"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.STRAIGHT
        assert result['name'] == "Straight"
    
    def test_wheel_straight_beats_high_card(self, evaluator):
        """Test that wheel straight beats high card."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "2"),
            Card("diamonds", "3"),
            Card("clubs", "4"),
            Card("hearts", "5"),
        ]
        hand2 = [
            Card("hearts", "K"),
            Card("spades", "Q"),
            Card("diamonds", "J"),
            Card("clubs", "9"),
            Card("hearts", "7"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_pair_kicker_comparison_ace_kicker_wins(self, evaluator):
        """Test that pair with ace kicker beats pair with king kicker."""
        hand1 = [
            Card("hearts", "K"),
            Card("spades", "K"),
            Card("diamonds", "A"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        hand2 = [
            Card("hearts", "K"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "9"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_pair_identical_same_rank_different_suits(self, evaluator):
        """Test that pairs of same rank with same kickers are equal."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        hand2 = [
            Card("diamonds", "A"),
            Card("clubs", "A"),
            Card("diamonds", "K"),
            Card("spades", "Q"),
            Card("hearts", "J"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 0
    
    def test_two_pair_higher_trips_wins(self, evaluator):
        """Test that two pair with higher trip wins."""
        hand1 = [
            Card("hearts", "K"),
            Card("spades", "K"),
            Card("diamonds", "5"),
            Card("clubs", "5"),
            Card("hearts", "A"),
        ]
        hand2 = [
            Card("hearts", "Q"),
            Card("spades", "Q"),
            Card("diamonds", "J"),
            Card("clubs", "J"),
            Card("hearts", "A"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_two_pair_same_trips_higher_second_pair_wins(self, evaluator):
        """Test that two pair with higher second pair wins."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "K"),
            Card("clubs", "K"),
            Card("hearts", "2"),
        ]
        hand2 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "Q"),
            Card("clubs", "Q"),
            Card("hearts", "K"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_three_of_a_kind_higher_kicker_wins(self, evaluator):
        """Test that three of a kind with higher kicker wins."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "K"),
            Card("hearts", "Q"),
        ]
        hand2 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "Q"),
            Card("hearts", "J"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_straight_higher_straight_wins(self, evaluator):
        """Test that higher straight wins."""
        hand1 = [
            Card("hearts", "6"),
            Card("spades", "7"),
            Card("diamonds", "8"),
            Card("clubs", "9"),
            Card("hearts", "10"),
        ]
        hand2 = [
            Card("hearts", "5"),
            Card("spades", "6"),
            Card("diamonds", "7"),
            Card("clubs", "8"),
            Card("hearts", "9"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_flush_different_suits_equal(self, evaluator):
        """Test that flushes of different suits with same cards are equal."""
        hand1 = [
            Card("hearts", "A"),
            Card("hearts", "K"),
            Card("hearts", "Q"),
            Card("hearts", "J"),
            Card("hearts", "9"),
        ]
        hand2 = [
            Card("spades", "A"),
            Card("spades", "K"),
            Card("spades", "Q"),
            Card("spades", "J"),
            Card("spades", "9"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 0
    
    def test_flush_higher_kicker_wins(self, evaluator):
        """Test that flush with higher kicker wins."""
        hand1 = [
            Card("hearts", "A"),
            Card("hearts", "K"),
            Card("hearts", "Q"),
            Card("hearts", "J"),
            Card("hearts", "10"),
        ]
        hand2 = [
            Card("spades", "A"),
            Card("spades", "K"),
            Card("spades", "Q"),
            Card("spades", "J"),
            Card("spades", "9"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_full_house_higher_trips_wins(self, evaluator):
        """Test that full house with higher trips wins."""
        hand1 = [
            Card("hearts", "K"),
            Card("spades", "K"),
            Card("diamonds", "K"),
            Card("clubs", "A"),
            Card("hearts", "A"),
        ]
        hand2 = [
            Card("hearts", "Q"),
            Card("spades", "Q"),
            Card("diamonds", "Q"),
            Card("clubs", "A"),
            Card("hearts", "A"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_full_house_same_trips_higher_pair_wins(self, evaluator):
        """Test that full house with same trips but higher pair wins."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "K"),
            Card("hearts", "K"),
        ]
        hand2 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "Q"),
            Card("hearts", "Q"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_four_of_a_kind_higher_kicker_wins(self, evaluator):
        """Test that four of a kind with higher kicker wins."""
        hand1 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "A"),
            Card("hearts", "K"),
        ]
        hand2 = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "A"),
            Card("hearts", "Q"),
        ]
        result = evaluator.compare_hands(hand1, hand2)
        assert result == 1
    
    def test_straight_flush_wheel_straight_flush(self, evaluator):
        """Test wheel straight flush (A-2-3-4-5 all same suit)."""
        cards = [
            Card("hearts", "A"),
            Card("hearts", "2"),
            Card("hearts", "3"),
            Card("hearts", "4"),
            Card("hearts", "5"),
        ]
        result = evaluator.evaluate(cards)
        assert result['rank'] == HandEvaluator.STRAIGHT_FLUSH
        assert result['name'] == "Straight Flush"
