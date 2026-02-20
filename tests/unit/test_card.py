"""Tests for Card class."""

import pytest
from poker_engine.card import Card


class TestCardCreation:
    """Test Card object creation."""
    
    def test_create_valid_card(self):
        """Test creating a valid card."""
        card = Card("hearts", "A")
        assert card.suit == "hearts"
        assert card.rank == "A"
    
    def test_invalid_suit(self):
        """Test that invalid suit raises error."""
        with pytest.raises(ValueError):
            Card("invalid", "A")
    
    def test_invalid_rank(self):
        """Test that invalid rank raises error."""
        with pytest.raises(ValueError):
            Card("hearts", "X")


class TestCardEquality:
    """Test Card equality."""
    
    def test_same_cards_equal(self):
        """Test that identical cards are equal."""
        card1 = Card("hearts", "A")
        card2 = Card("hearts", "A")
        assert card1 == card2
    
    def test_different_rank_not_equal(self):
        """Test that cards with different ranks are not equal."""
        card1 = Card("hearts", "A")
        card2 = Card("hearts", "K")
        assert card1 != card2
    
    def test_different_suit_not_equal(self):
        """Test that cards with different suits are not equal."""
        card1 = Card("hearts", "A")
        card2 = Card("spades", "A")
        assert card1 != card2


class TestCardRankValue:
    """Test Card rank values."""
    
    def test_rank_value_2(self):
        """Test that rank 2 has value 0."""
        card = Card("hearts", "2")
        assert card.get_rank_value() == 0
    
    def test_rank_value_10(self):
        """Test that rank 10 has value 8."""
        card = Card("hearts", "10")
        assert card.get_rank_value() == 8
    
    def test_rank_value_ace(self):
        """Test that rank A has value 12."""
        card = Card("hearts", "A")
        assert card.get_rank_value() == 12


class TestCardRepresentation:
    """Test Card string representations."""
    
    def test_repr(self):
        """Test Card repr."""
        card = Card("hearts", "A")
        assert repr(card) == "AH"
    
    def test_str(self):
        """Test Card str."""
        card = Card("hearts", "A")
        assert str(card) == "A of hearts"
