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
