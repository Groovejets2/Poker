"""Unit tests for PlayerState and enums."""

import pytest
from poker_engine.card import Card
from poker_engine.player_state import (
    PlayerState,
    PlayerStatus,
    RoundStatus,
)


class TestPlayerStatus:
    """Tests for PlayerStatus enum."""
    
    def test_player_status_active_value(self):
        """Test ACTIVE status has correct value."""
        assert PlayerStatus.ACTIVE.value == "ACTIVE"
    
    def test_player_status_folded_value(self):
        """Test FOLDED status has correct value."""
        assert PlayerStatus.FOLDED.value == "FOLDED"
    
    def test_player_status_all_in_value(self):
        """Test ALL_IN status has correct value."""
        assert PlayerStatus.ALL_IN.value == "ALL_IN"
    
    def test_player_status_out_of_hand_value(self):
        """Test OUT_OF_HAND status has correct value."""
        assert PlayerStatus.OUT_OF_HAND.value == "OUT_OF_HAND"


class TestRoundStatus:
    """Tests for RoundStatus enum."""
    
    def test_round_status_waiting_for_action_value(self):
        """Test WAITING_FOR_ACTION status has correct value."""
        assert RoundStatus.WAITING_FOR_ACTION.value == "WAITING_FOR_ACTION"
    
    def test_round_status_acted_value(self):
        """Test ACTED status has correct value."""
        assert RoundStatus.ACTED.value == "ACTED"
    
    def test_round_status_sitting_out_value(self):
        """Test SITTING_OUT status has correct value."""
        assert RoundStatus.SITTING_OUT.value == "SITTING_OUT"


class TestPlayerStateInitialisation:
    """Tests for PlayerState initialisation."""
    
    def test_player_state_init_valid(self):
        """Test creating a valid player."""
        player = PlayerState("bot_1", 0, 1000)
        assert player.player_id == "bot_1"
        assert player.seat_number == 0
        assert player.stack == 1000
        assert player.current_bet == 0
        assert player.hole_cards == []
        assert player.status == PlayerStatus.ACTIVE
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_player_state_init_various_seats(self):
        """Test player initialisation at different seats."""
        for seat in range(8):
            player = PlayerState(f"bot_{seat}", seat, 500)
            assert player.seat_number == seat
    
    def test_player_state_init_invalid_seat_negative(self):
        """Test that negative seat number raises ValueError."""
        with pytest.raises(ValueError, match="Seat number must be 0-7"):
            PlayerState("bot_1", -1, 1000)
    
    def test_player_state_init_invalid_seat_too_high(self):
        """Test that seat > 7 raises ValueError."""
        with pytest.raises(ValueError, match="Seat number must be 0-7"):
            PlayerState("bot_1", 8, 1000)
    
    def test_player_state_init_invalid_stack_zero(self):
        """Test that zero stack raises ValueError."""
        with pytest.raises(ValueError, match="Starting stack must be positive"):
            PlayerState("bot_1", 0, 0)
    
    def test_player_state_init_invalid_stack_negative(self):
        """Test that negative stack raises ValueError."""
        with pytest.raises(ValueError, match="Starting stack must be positive"):
            PlayerState("bot_1", 0, -100)


class TestPlayerStateBetting:
    """Tests for player betting operations."""
    
    def test_post_bet_valid(self):
        """Test posting a valid bet."""
        player = PlayerState("bot_1", 0, 1000)
        player.post_bet(50)
        assert player.stack == 950
        assert player.current_bet == 50
    
    def test_post_bet_multiple_times(self):
        """Test multiple bets accumulate correctly."""
        player = PlayerState("bot_1", 0, 1000)
        player.post_bet(50)
        player.post_bet(30)
        assert player.stack == 920
        assert player.current_bet == 80
    
    def test_post_bet_all_in(self):
        """Test betting entire stack."""
        player = PlayerState("bot_1", 0, 100)
        player.post_bet(100)
        assert player.stack == 0
        assert player.current_bet == 100
    
    def test_post_bet_exceeds_stack(self):
        """Test that betting more than stack raises ValueError."""
        player = PlayerState("bot_1", 0, 100)
        with pytest.raises(ValueError, match="exceeds stack"):
            player.post_bet(150)
    
    def test_post_bet_negative(self):
        """Test that negative bet raises ValueError."""
        player = PlayerState("bot_1", 0, 1000)
        with pytest.raises(ValueError, match="cannot be negative"):
            player.post_bet(-50)


class TestPlayerStateActions:
    """Tests for player action methods."""
    
    def test_fold(self):
        """Test folding a player."""
        player = PlayerState("bot_1", 0, 1000)
        player.status = PlayerStatus.ACTIVE
        player.round_status = RoundStatus.WAITING_FOR_ACTION
        player.fold()
        assert player.status == PlayerStatus.FOLDED
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_go_all_in(self):
        """Test marking player all-in."""
        player = PlayerState("bot_1", 0, 1000)
        player.status = PlayerStatus.ACTIVE
        player.round_status = RoundStatus.WAITING_FOR_ACTION
        player.go_all_in()
        assert player.status == PlayerStatus.ALL_IN
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_deal_hole_cards_texas_holdem(self):
        """Test dealing hole cards (2 cards for Texas Hold'em)."""
        player = PlayerState("bot_1", 0, 1000)
        cards = [Card("hearts", "A"), Card("spades", "K")]
        player.deal_hole_cards(cards)
        assert len(player.hole_cards) == 2
        assert player.hole_cards[0] == cards[0]
        assert player.hole_cards[1] == cards[1]
    
    def test_deal_hole_cards_five_card_draw(self):
        """Test dealing hole cards (5 cards for 5-card draw)."""
        player = PlayerState("bot_1", 0, 1000)
        cards = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "10"),
        ]
        player.deal_hole_cards(cards)
        assert len(player.hole_cards) == 5
    
    def test_deal_hole_cards_empty_list(self):
        """Test that dealing empty list raises ValueError."""
        player = PlayerState("bot_1", 0, 1000)
        with pytest.raises(ValueError, match="at least one card"):
            player.deal_hole_cards([])
    
    def test_deal_hole_cards_invalid_card_type(self):
        """Test that dealing non-Card objects raises ValueError."""
        player = PlayerState("bot_1", 0, 1000)
        with pytest.raises(ValueError, match="Expected Card"):
            player.deal_hole_cards(["A", "K"])
    
    def test_deal_hole_cards_replaces_previous(self):
        """Test that dealing cards replaces previous hole cards."""
        player = PlayerState("bot_1", 0, 1000)
        cards1 = [Card("hearts", "A"), Card("spades", "K")]
        player.deal_hole_cards(cards1)
        
        cards2 = [Card("diamonds", "Q"), Card("clubs", "J")]
        player.deal_hole_cards(cards2)
        
        assert len(player.hole_cards) == 2
        assert player.hole_cards[0] == cards2[0]
        assert player.hole_cards[1] == cards2[1]


class TestPlayerStateRoundData:
    """Tests for clearing and resetting round data."""
    
    def test_clear_round_data(self):
        """Test clearing round data."""
        player = PlayerState("bot_1", 0, 1000)
        player.post_bet(50)
        player.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        player.round_status = RoundStatus.ACTED
        
        player.clear_round_data()
        
        assert player.current_bet == 0
        assert player.hole_cards == []
        assert player.round_status == RoundStatus.SITTING_OUT
        assert player.stack == 950  # Stack not reset
    
    def test_reset_for_new_hand_active_player(self):
        """Test resetting an active player for new hand."""
        player = PlayerState("bot_1", 0, 1000)
        player.post_bet(50)
        player.status = PlayerStatus.ALL_IN
        player.round_status = RoundStatus.SITTING_OUT
        
        player.reset_for_new_hand()
        
        assert player.status == PlayerStatus.ACTIVE
        assert player.current_bet == 0
        assert player.hole_cards == []
        assert player.stack == 950
    
    def test_reset_for_new_hand_busted_player(self):
        """Test that busted player stays busted after reset."""
        player = PlayerState("bot_1", 0, 100)
        player.post_bet(100)
        player.status = PlayerStatus.ALL_IN
        
        player.reset_for_new_hand()
        
        assert player.status == PlayerStatus.ALL_IN  # Still all-in (no chips)
        assert player.stack == 0


class TestPlayerStateQueries:
    """Tests for player query methods."""
    
    def test_is_active_in_hand_active(self):
        """Test that ACTIVE player is considered active."""
        player = PlayerState("bot_1", 0, 1000)
        player.status = PlayerStatus.ACTIVE
        assert player.is_active_in_hand() is True
    
    def test_is_active_in_hand_all_in(self):
        """Test that ALL_IN player is still considered active."""
        player = PlayerState("bot_1", 0, 1000)
        player.status = PlayerStatus.ALL_IN
        assert player.is_active_in_hand() is True
    
    def test_is_active_in_hand_folded(self):
        """Test that FOLDED player is not active."""
        player = PlayerState("bot_1", 0, 1000)
        player.status = PlayerStatus.FOLDED
        assert player.is_active_in_hand() is False
    
    def test_is_active_in_hand_out_of_hand(self):
        """Test that OUT_OF_HAND player is not active."""
        player = PlayerState("bot_1", 0, 1000)
        player.status = PlayerStatus.OUT_OF_HAND
        assert player.is_active_in_hand() is False


class TestPlayerStateRepr:
    """Tests for string representation."""
    
    def test_repr(self):
        """Test that __repr__ returns a valid string."""
        player = PlayerState("bot_1", 0, 1000)
        repr_str = repr(player)
        assert "bot_1" in repr_str
        assert "seat=0" in repr_str
        assert "stack=1000" in repr_str
        assert "ACTIVE" in repr_str
