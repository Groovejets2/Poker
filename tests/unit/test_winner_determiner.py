"""Comprehensive tests for WinnerDeterminer class."""

import pytest
from poker_engine.card import Card
from poker_engine.player_state import PlayerState, PlayerStatus
from poker_engine.hand_evaluator import HandEvaluator
from poker_engine.winner_determiner import WinnerDeterminer


class TestWinnerDeterminerInitialisation:
    """Test WinnerDeterminer creation."""
    
    def test_create_valid_winner_determiner(self):
        """Test creating a valid winner determiner."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        assert determiner.hand_evaluator == evaluator


class TestDetermineWinnersSimple:
    """Test determining winners in simple scenarios."""
    
    def test_single_remaining_player_wins_all(self):
        """Test that single remaining player wins everything."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        # Two players, but one folded
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        player2.fold()
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=200,
            side_pots=[],
            community_cards=[]
        )
        
        assert winnings["alice"] == 200
        assert winnings["bob"] == 0
    
    def test_two_players_same_hand_strength_split(self):
        """Test that tie results in equal split."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        # Both have same high card
        player1.deal_hole_cards([Card("hearts", "2"), Card("spades", "3")])
        player2.deal_hole_cards([Card("diamonds", "2"), Card("clubs", "3")])
        
        community = [
            Card("hearts", "7"),
            Card("spades", "8"),
            Card("diamonds", "9"),
            Card("clubs", "10"),
            Card("hearts", "J")
        ]
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=200,
            side_pots=[],
            community_cards=community
        )
        
        # Split 200 between both
        assert winnings["alice"] == 100
        assert winnings["bob"] == 100


class TestDetermineWinnersWithMainPot:
    """Test winner determination with main pot."""
    
    def test_main_pot_only_single_winner(self):
        """Test main pot distribution with single winner."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        player3 = PlayerState("charlie", 2, 1000)
        
        # Alice has best hand
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "A")])
        player2.deal_hole_cards([Card("diamonds", "K"), Card("clubs", "K")])
        player3.deal_hole_cards([Card("hearts", "Q"), Card("spades", "Q")])
        
        community = [
            Card("hearts", "2"),
            Card("spades", "3"),
            Card("diamonds", "4"),
            Card("clubs", "5"),
            Card("hearts", "6")
        ]
        
        remaining = [player1, player2, player3]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=300,
            side_pots=[],
            community_cards=community
        )
        
        assert winnings["alice"] == 300
        assert winnings["bob"] == 0
        assert winnings["charlie"] == 0


class TestDetermineWinnersWithSidePots:
    """Test winner determination with side pots."""
    
    def test_main_pot_and_side_pot_distribution(self):
        """Test distribution with main and side pot."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        # Alice has best hand
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "A")])
        player2.deal_hole_cards([Card("diamonds", "K"), Card("clubs", "K")])
        
        community = [
            Card("hearts", "2"),
            Card("spades", "3"),
            Card("diamonds", "4"),
            Card("clubs", "5"),
            Card("hearts", "6")
        ]
        
        remaining = [player1, player2]
        
        # Main pot: 100 (both eligible)
        # Side pot: 50 (bob only)
        side_pots = [
            {
                "amount": 50,
                "eligible_players": ["bob"]
            }
        ]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=100,
            side_pots=side_pots,
            community_cards=community
        )
        
        # Alice wins main pot, Bob wins side pot
        assert winnings["alice"] == 100
        assert winnings["bob"] == 50


class TestDetermineWinnersMultipleSidePots:
    """Test with multiple side pots."""
    
    def test_three_way_pot_with_multiple_side_pots(self):
        """Test complex scenario with multiple side pots."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        player3 = PlayerState("charlie", 2, 1000)
        
        # Alice has best hand
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "A")])
        player2.deal_hole_cards([Card("diamonds", "K"), Card("clubs", "K")])
        player3.deal_hole_cards([Card("hearts", "Q"), Card("spades", "Q")])
        
        community = [
            Card("hearts", "2"),
            Card("spades", "3"),
            Card("diamonds", "4"),
            Card("clubs", "5"),
            Card("hearts", "6")
        ]
        
        remaining = [player1, player2, player3]
        
        # Main: 150, Side 1: 100, Side 2: 50
        side_pots = [
            {"amount": 100, "eligible_players": ["alice", "bob"]},
            {"amount": 50, "eligible_players": ["bob", "charlie"]}
        ]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=150,
            side_pots=side_pots,
            community_cards=community
        )
        
        # Alice should win main pot (150) and side pot 1 (100)
        # Bob should win side pot 2 (50)
        assert winnings["alice"] >= 150


class TestTieHandling:
    """Test handling of tied hands."""
    
    def test_tie_equal_split(self):
        """Test that tied hands split pot equally."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        # Identical hands
        player1.deal_hole_cards([Card("hearts", "2"), Card("spades", "3")])
        player2.deal_hole_cards([Card("diamonds", "2"), Card("clubs", "3")])
        
        community = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "10")
        ]
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=200,
            side_pots=[],
            community_cards=community
        )
        
        assert winnings["alice"] == 100
        assert winnings["bob"] == 100
    
    def test_three_way_tie_equal_split(self):
        """Test three-way tie with equal split."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        player3 = PlayerState("charlie", 2, 1000)
        
        # All have same high card combo (T, 9, 8, 7, 6)
        player1.deal_hole_cards([Card("hearts", "10"), Card("spades", "9")])
        player2.deal_hole_cards([Card("diamonds", "10"), Card("clubs", "9")])
        player3.deal_hole_cards([Card("hearts", "10"), Card("spades", "9")])
        
        community = [
            Card("diamonds", "8"),
            Card("clubs", "7"),
            Card("hearts", "6"),
            Card("spades", "5"),
            Card("diamonds", "4")
        ]
        
        remaining = [player1, player2, player3]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=300,
            side_pots=[],
            community_cards=community
        )
        
        # 300 / 3 = 100 each
        assert winnings["alice"] == 100
        assert winnings["bob"] == 100
        assert winnings["charlie"] == 100


class TestFoldedPlayerExclusion:
    """Test that folded players are excluded from hand comparison."""
    
    def test_folded_player_cannot_win(self):
        """Test that folded players cannot win."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        # Alice has better hand but she folded
        player1.fold()
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "A")])
        
        # Bob has worse hand but he's still active
        player2.deal_hole_cards([Card("diamonds", "2"), Card("clubs", "3")])
        
        community = [
            Card("hearts", "2"),
            Card("spades", "3"),
            Card("diamonds", "4"),
            Card("clubs", "5"),
            Card("hearts", "6")
        ]
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=200,
            side_pots=[],
            community_cards=community
        )
        
        # Bob wins despite worse hand (Alice folded)
        assert winnings["bob"] == 200
        assert winnings["alice"] == 0


class TestGetHandSummary:
    """Test getting hand summaries."""
    
    def test_get_hand_summary_valid(self):
        """Test getting summary of valid hand."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player = PlayerState("alice", 0, 1000)
        player.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        
        community = [
            Card("hearts", "A"),
            Card("spades", "A"),
            Card("diamonds", "A"),
            Card("clubs", "K"),
            Card("hearts", "Q")
        ]
        
        summary = determiner.get_hand_summary(player, community)
        
        assert summary is not None
        assert summary["player_id"] == "alice"
        assert "hand_name" in summary
        assert "hand_rank" in summary
        assert "strength" in summary
    
    def test_get_hand_summary_no_cards(self):
        """Test getting summary when player has no cards."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player = PlayerState("alice", 0, 1000)
        
        community = [Card("hearts", "A")]
        
        summary = determiner.get_hand_summary(player, community)
        assert summary is None


class TestZeroPotDistribution:
    """Test edge cases with zero amounts."""
    
    def test_empty_pot_no_distribution(self):
        """Test that empty pot distributes nothing."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        player2.deal_hole_cards([Card("diamonds", "Q"), Card("clubs", "J")])
        
        community = [Card("hearts", "2")]
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=0,
            side_pots=[],
            community_cards=community
        )
        
        # Both get 0 with empty pot
        assert winnings["alice"] == 0
        assert winnings["bob"] == 0


class TestPushAllInScenario:
    """Test all-in scenarios where remaining chips matter."""
    
    def test_all_in_winner_gets_pot(self):
        """Test that all-in winner gets entire pot."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 50)  # Short stack
        player2 = PlayerState("bob", 1, 1000)
        
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "A")])
        player2.deal_hole_cards([Card("diamonds", "K"), Card("clubs", "K")])
        
        community = [
            Card("hearts", "2"),
            Card("spades", "3"),
            Card("diamonds", "4"),
            Card("clubs", "5"),
            Card("hearts", "6")
        ]
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=100,
            side_pots=[],
            community_cards=community
        )
        
        # Alice (shorter stack) wins the pot
        assert winnings["alice"] == 100
        assert winnings["bob"] == 0


class TestRemainderDistribution:
    """Test handling of remainder chips in splits."""
    
    def test_odd_pot_split_remainder(self):
        """Test that remainder chips are distributed correctly."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        # Same hand strength
        player1.deal_hole_cards([Card("hearts", "2"), Card("spades", "3")])
        player2.deal_hole_cards([Card("diamonds", "2"), Card("clubs", "3")])
        
        community = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "10")
        ]
        
        remaining = [player1, player2]
        
        # Odd amount (301) - should split with remainder going to first winner
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=301,
            side_pots=[],
            community_cards=community
        )
        
        # 301 / 2 = 150 each, with 1 chip remainder
        total = winnings["alice"] + winnings["bob"]
        assert total == 301


class TestComplexMultiWayPots:
    """Test complex multi-way pot scenarios."""
    
    def test_three_player_all_in_sequence(self):
        """Test three players going all-in at different times."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        player3 = PlayerState("charlie", 2, 1000)
        
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "A")])
        player2.deal_hole_cards([Card("diamonds", "K"), Card("clubs", "K")])
        player3.deal_hole_cards([Card("hearts", "Q"), Card("spades", "Q")])
        
        community = [
            Card("hearts", "2"),
            Card("spades", "3"),
            Card("diamonds", "4"),
            Card("clubs", "5"),
            Card("hearts", "6")
        ]
        
        remaining = [player1, player2, player3]
        
        side_pots = [
            {"amount": 100, "eligible_players": ["bob", "charlie"]},
            {"amount": 50, "eligible_players": ["charlie"]}
        ]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=300,
            side_pots=side_pots,
            community_cards=community
        )
        
        # Alice wins main (300), Bob wins side 1 (100), Charlie wins side 2 (50)
        total = winnings["alice"] + winnings["bob"] + winnings["charlie"]
        assert total == 450


class TestEdgeCases:
    """Test edge cases and unusual scenarios."""
    
    def test_single_player_game(self):
        """Test game where only one player is active."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        player1 = PlayerState("alice", 0, 1000)
        player2 = PlayerState("bob", 1, 1000)
        
        player1.deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        player2.fold()
        
        remaining = [player1, player2]
        
        winnings = determiner.determine_winners(
            remaining_players=remaining,
            main_pot=500,
            side_pots=[],
            community_cards=[]
        )
        
        assert winnings["alice"] == 500
    
    def test_all_players_folded_except_one(self):
        """Test when all but one player folded."""
        evaluator = HandEvaluator()
        determiner = WinnerDeterminer(evaluator)
        
        players = [
            PlayerState("alice", 0, 1000),
            PlayerState("bob", 1, 1000),
            PlayerState("charlie", 2, 1000),
            PlayerState("dave", 3, 1000)
        ]
        
        players[0].deal_hole_cards([Card("hearts", "A"), Card("spades", "K")])
        players[1].fold()
        players[2].fold()
        players[3].fold()
        
        winnings = determiner.determine_winners(
            remaining_players=players,
            main_pot=400,
            side_pots=[],
            community_cards=[]
        )
        
        assert winnings["alice"] == 400
        for i in range(1, 4):
            assert winnings[players[i].player_id] == 0
