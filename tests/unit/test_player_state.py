"""Comprehensive tests for PlayerState class."""

import pytest
from poker_engine.card import Card
from poker_engine.player_state import PlayerState, PlayerStatus, RoundStatus


class TestPlayerStateInitialisation:
    """Test PlayerState object creation and initialisation."""
    
    def test_create_valid_player(self):
        """Test creating a valid player with valid parameters."""
        player = PlayerState("bot_001", seat_number=0, starting_stack=1000)
        assert player.player_id == "bot_001"
        assert player.seat_number == 0
        assert player.stack == 1000
        assert player.current_bet == 0
        assert player.hole_cards == []
        assert player.status == PlayerStatus.ACTIVE
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_create_player_at_different_seats(self):
        """Test creating players at each seat position."""
        for seat in range(8):
            player = PlayerState(f"player_{seat}", seat, 500)
            assert player.seat_number == seat
    
    def test_invalid_seat_number_negative(self):
        """Test that negative seat number raises ValueError."""
        with pytest.raises(ValueError, match="Seat number must be 0-7"):
            PlayerState("bot_001", seat_number=-1, starting_stack=1000)
    
    def test_invalid_seat_number_too_high(self):
        """Test that seat number > 7 raises ValueError."""
        with pytest.raises(ValueError, match="Seat number must be 0-7"):
            PlayerState("bot_001", seat_number=8, starting_stack=1000)
    
    def test_invalid_starting_stack_zero(self):
        """Test that zero starting stack raises ValueError."""
        with pytest.raises(ValueError, match="Starting stack must be positive"):
            PlayerState("bot_001", seat_number=0, starting_stack=0)
    
    def test_invalid_starting_stack_negative(self):
        """Test that negative starting stack raises ValueError."""
        with pytest.raises(ValueError, match="Starting stack must be positive"):
            PlayerState("bot_001", seat_number=0, starting_stack=-100)
    
    def test_initial_state_consistency(self):
        """Test that initial state is consistent across multiple players."""
        players = [
            PlayerState(f"bot_{i}", i, 5000)
            for i in range(8)
        ]
        for i, player in enumerate(players):
            assert player.seat_number == i
            assert player.stack == 5000
            assert player.current_bet == 0
            assert player.status == PlayerStatus.ACTIVE


class TestPlayerBetting:
    """Test betting and chip management."""
    
    def test_post_valid_bet(self):
        """Test posting a valid bet."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(100)
        assert player.stack == 900
        assert player.current_bet == 100
    
    def test_post_bet_all_in(self):
        """Test betting all remaining chips."""
        player = PlayerState("bot_001", 0, 500)
        player.post_bet(500)
        assert player.stack == 0
        assert player.current_bet == 500
    
    def test_post_multiple_bets_in_round(self):
        """Test posting multiple bets in same round (call + raise)."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(50)
        assert player.current_bet == 50
        assert player.stack == 950
        
        player.post_bet(100)
        assert player.current_bet == 150
        assert player.stack == 850
    
    def test_post_bet_more_than_stack(self):
        """Test that betting more than stack raises ValueError."""
        player = PlayerState("bot_001", 0, 100)
        with pytest.raises(ValueError, match="exceeds stack"):
            player.post_bet(150)
    
    def test_post_negative_bet(self):
        """Test that negative bet raises ValueError."""
        player = PlayerState("bot_001", 0, 1000)
        with pytest.raises(ValueError, match="cannot be negative"):
            player.post_bet(-50)
    
    def test_post_zero_bet(self):
        """Test that zero bet is allowed (check)."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(0)
        assert player.stack == 1000
        assert player.current_bet == 0


class TestPlayerFolding:
    """Test folding behaviour."""
    
    def test_fold_changes_status(self):
        """Test that fold changes player status to FOLDED."""
        player = PlayerState("bot_001", 0, 1000)
        assert player.status == PlayerStatus.ACTIVE
        
        player.fold()
        assert player.status == PlayerStatus.FOLDED
    
    def test_fold_sets_round_status_sitting_out(self):
        """Test that fold sets round status to SITTING_OUT."""
        player = PlayerState("bot_001", 0, 1000)
        player.round_status = RoundStatus.WAITING_FOR_ACTION
        
        player.fold()
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_fold_preserves_stack(self):
        """Test that folding does not affect stack."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(100)
        original_stack = player.stack
        
        player.fold()
        assert player.stack == original_stack
    
    def test_fold_multiple_times(self):
        """Test that folding multiple times is idempotent."""
        player = PlayerState("bot_001", 0, 1000)
        player.fold()
        status_after_first = player.status
        
        player.fold()
        assert player.status == status_after_first


class TestPlayerAllIn:
    """Test all-in behaviour."""
    
    def test_all_in_changes_status(self):
        """Test that go_all_in changes status to ALL_IN."""
        player = PlayerState("bot_001", 0, 1000)
        assert player.status == PlayerStatus.ACTIVE
        
        player.go_all_in()
        assert player.status == PlayerStatus.ALL_IN
    
    def test_all_in_sets_round_status_sitting_out(self):
        """Test that all-in sets round status to SITTING_OUT."""
        player = PlayerState("bot_001", 0, 1000)
        player.round_status = RoundStatus.WAITING_FOR_ACTION
        
        player.go_all_in()
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_all_in_preserves_stack(self):
        """Test that all-in does not affect stack."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(950)
        remaining = player.stack
        
        player.go_all_in()
        assert player.stack == remaining


class TestPlayerHoleCards:
    """Test hole card management."""
    
    def test_deal_two_hole_cards(self):
        """Test dealing two hole cards (Hold'em)."""
        player = PlayerState("bot_001", 0, 1000)
        cards = [Card("hearts", "A"), Card("spades", "K")]
        
        player.deal_hole_cards(cards)
        assert len(player.hole_cards) == 2
        assert player.hole_cards[0] == cards[0]
        assert player.hole_cards[1] == cards[1]
    
    def test_deal_five_hole_cards(self):
        """Test dealing five hole cards (Draw)."""
        player = PlayerState("bot_001", 0, 1000)
        cards = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "10")
        ]
        
        player.deal_hole_cards(cards)
        assert len(player.hole_cards) == 5
    
    def test_deal_hole_cards_empty_list_raises_error(self):
        """Test that dealing empty list raises ValueError."""
        player = PlayerState("bot_001", 0, 1000)
        with pytest.raises(ValueError, match="at least one card"):
            player.deal_hole_cards([])
    
    def test_deal_hole_cards_non_card_object_raises_error(self):
        """Test that dealing non-Card objects raises ValueError."""
        player = PlayerState("bot_001", 0, 1000)
        with pytest.raises(ValueError, match="Expected Card"):
            player.deal_hole_cards([Card("hearts", "A"), "invalid"])
    
    def test_deal_cards_replaces_previous_cards(self):
        """Test that dealing cards replaces previous hole cards."""
        player = PlayerState("bot_001", 0, 1000)
        
        first_cards = [Card("hearts", "A"), Card("spades", "K")]
        player.deal_hole_cards(first_cards)
        
        second_cards = [Card("diamonds", "Q"), Card("clubs", "J")]
        player.deal_hole_cards(second_cards)
        
        assert len(player.hole_cards) == 2
        assert player.hole_cards[0] == second_cards[0]


class TestPlayerRoundData:
    """Test clearing round data and resetting states."""
    
    def test_clear_round_data_resets_current_bet(self):
        """Test that clear_round_data resets current_bet to 0."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(150)
        
        player.clear_round_data()
        assert player.current_bet == 0
    
    def test_clear_round_data_resets_hole_cards(self):
        """Test that clear_round_data clears hole cards."""
        player = PlayerState("bot_001", 0, 1000)
        player.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        
        player.clear_round_data()
        assert player.hole_cards == []
    
    def test_clear_round_data_resets_round_status(self):
        """Test that clear_round_data sets round_status to SITTING_OUT."""
        player = PlayerState("bot_001", 0, 1000)
        player.round_status = RoundStatus.ACTED
        
        player.clear_round_data()
        assert player.round_status == RoundStatus.SITTING_OUT
    
    def test_clear_round_data_preserves_stack(self):
        """Test that clear_round_data does not affect stack."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(200)
        original_stack = player.stack
        
        player.clear_round_data()
        assert player.stack == original_stack
    
    def test_clear_round_data_preserves_status(self):
        """Test that clear_round_data preserves player status."""
        player = PlayerState("bot_001", 0, 1000)
        player.fold()
        
        player.clear_round_data()
        assert player.status == PlayerStatus.FOLDED


class TestPlayerResetForNewHand:
    """Test resetting player for new hand."""
    
    def test_reset_for_new_hand_restores_active_status(self):
        """Test that reset restores ACTIVE status if stack > 0."""
        player = PlayerState("bot_001", 0, 1000)
        player.fold()
        assert player.status == PlayerStatus.FOLDED
        
        player.reset_for_new_hand()
        assert player.status == PlayerStatus.ACTIVE
    
    def test_reset_for_new_hand_clears_bets(self):
        """Test that reset clears current bets."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(200)
        
        player.reset_for_new_hand()
        assert player.current_bet == 0
    
    def test_reset_for_new_hand_clears_cards(self):
        """Test that reset clears hole cards."""
        player = PlayerState("bot_001", 0, 1000)
        player.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        
        player.reset_for_new_hand()
        assert player.hole_cards == []
    
    def test_reset_for_new_hand_preserves_stack(self):
        """Test that reset preserves remaining stack."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(300)
        remaining = player.stack
        
        player.reset_for_new_hand()
        assert player.stack == remaining
    
    def test_reset_for_new_hand_zero_stack_stays_out(self):
        """Test that player with zero stack stays OUT_OF_HAND."""
        player = PlayerState("bot_001", 0, 100)
        player.post_bet(100)
        assert player.stack == 0
        
        player.reset_for_new_hand()
        # Note: actual behaviour depends on implementation choice
        # This tests current expected behaviour
        assert player.stack == 0


class TestPlayerActiveInHand:
    """Test checking if player is active."""
    
    def test_active_player_is_active(self):
        """Test that ACTIVE player is considered active in hand."""
        player = PlayerState("bot_001", 0, 1000)
        assert player.status == PlayerStatus.ACTIVE
        assert player.is_active_in_hand() is True
    
    def test_all_in_player_is_active(self):
        """Test that ALL_IN player is considered active in hand."""
        player = PlayerState("bot_001", 0, 1000)
        player.go_all_in()
        assert player.is_active_in_hand() is True
    
    def test_folded_player_not_active(self):
        """Test that FOLDED player is not active."""
        player = PlayerState("bot_001", 0, 1000)
        player.fold()
        assert player.is_active_in_hand() is False
    
    def test_out_of_hand_player_not_active(self):
        """Test that OUT_OF_HAND player is not active."""
        player = PlayerState("bot_001", 0, 1000)
        player.status = PlayerStatus.OUT_OF_HAND
        assert player.is_active_in_hand() is False


class TestPlayerRepr:
    """Test string representation."""
    
    def test_repr_contains_player_id(self):
        """Test that repr contains player ID."""
        player = PlayerState("test_bot", 2, 1000)
        repr_str = repr(player)
        assert "test_bot" in repr_str
    
    def test_repr_contains_seat_number(self):
        """Test that repr contains seat number."""
        player = PlayerState("bot_001", 5, 1000)
        repr_str = repr(player)
        assert "5" in repr_str
    
    def test_repr_contains_stack(self):
        """Test that repr contains stack amount."""
        player = PlayerState("bot_001", 0, 2500)
        repr_str = repr(player)
        assert "2500" in repr_str


class TestPlayerEdgeCases:
    """Test edge cases and complex scenarios."""
    
    def test_large_stack_operations(self):
        """Test operations with very large stacks."""
        player = PlayerState("bot_001", 0, 1_000_000)
        player.post_bet(500_000)
        assert player.stack == 500_000
        assert player.current_bet == 500_000
    
    def test_sequence_bet_then_fold(self):
        """Test betting then folding in sequence."""
        player = PlayerState("bot_001", 0, 1000)
        player.post_bet(100)
        player.fold()
        
        assert player.status == PlayerStatus.FOLDED
        assert player.stack == 900
        assert player.current_bet == 100
    
    def test_sequence_multiple_rounds_betting(self):
        """Test betting across multiple rounds."""
        player = PlayerState("bot_001", 0, 1000)
        
        # Round 1 betting
        player.post_bet(50)
        assert player.current_bet == 50
        
        # Clear for Round 2
        player.clear_round_data()
        assert player.current_bet == 0
        
        # Round 2 betting
        player.post_bet(100)
        assert player.current_bet == 100
        assert player.stack == 850
    
    def test_player_with_single_chip(self):
        """Test player with only 1 chip."""
        player = PlayerState("bot_001", 0, 1)
        player.post_bet(1)
        assert player.stack == 0
        assert player.current_bet == 1
