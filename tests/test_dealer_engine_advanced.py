"""
Unit tests for advanced dealer engine features: side pots and winner determination.

Tests cover:
- Side pot creation with all-in scenarios
- Winner determination with hand ranking
- Pot distribution to single and multiple winners
- Tie handling (split pots)
- Integration with hand evaluator

Author: Angus Young
Date: 2026-02-21
Version: 1.0
"""

import unittest
from src.dealer_engine import (
    DealerEngine, GameType, Player, Card, PlayerStatus
)
from src.dealer_engine_advanced import (
    SidePotManager, WinnerDeterminer, DealerEngineWithWinners
)
from src.hand_evaluator import HandEvaluator


class TestSidePotManager(unittest.TestCase):
    """Test side pot creation and management."""
    
    def test_no_side_pot_with_even_bets(self):
        """Test no side pots created when all players bet equally."""
        players = [
            Player("p1", "dealer", 1000, 500),
            Player("p2", "sb", 1000, 500),
            Player("p3", "bb", 1000, 500),
        ]
        
        # All players bet same amount
        for p in players:
            p.current_bet_in_round = 100
        
        engine = DealerEngine(GameType.TEXAS_HOLDEM, players, 25, 50)
        main_pot, side_pots = SidePotManager.create_side_pots(engine, players)
        
        self.assertEqual(len(side_pots), 0)
    
    def test_side_pot_created_with_all_in(self):
        """Test side pot is created when player goes all-in with fewer chips."""
        players = [
            Player("p1", "dealer", 100, 0),  # All-in for 100
            Player("p2", "sb", 500, 400),    # Has 400 left to bet
            Player("p3", "bb", 500, 400),    # Has 400 left to bet
        ]
        
        players[0].current_bet_in_round = 100
        players[1].current_bet_in_round = 400
        players[2].current_bet_in_round = 400
        
        engine = DealerEngine(GameType.TEXAS_HOLDEM, players, 25, 50)
        main_pot, side_pots = SidePotManager.create_side_pots(engine, players)
        
        # Main pot: 100 × 3 = 300
        # Side pot: 300 × 2 = 600 (only p2 and p3 eligible)
        self.assertEqual(main_pot.amount, 300)
        self.assertGreater(len(side_pots), 0)
    
    def test_side_pot_eligibility(self):
        """Test side pot eligibility is correctly determined."""
        player = Player("p1", "dealer", 500, 250)
        pot = type('obj', (object,), {
            'amount': 100,
            'contributors': ['p1', 'p2', 'p3']
        })()
        
        is_eligible = SidePotManager.is_side_pot_winner('p1', pot)
        self.assertTrue(is_eligible)
        
        is_not_eligible = SidePotManager.is_side_pot_winner('p4', pot)
        self.assertFalse(is_not_eligible)


class TestWinnerDeterminer(unittest.TestCase):
    """Test winner determination and pot distribution."""
    
    def setUp(self):
        """Create test players and winner determiner."""
        self.players = [
            Player("p1", "dealer", 1000, 1000),
            Player("p2", "sb", 1000, 1000),
            Player("p3", "bb", 1000, 1000),
        ]
        self.determiner = WinnerDeterminer()
    
    def test_single_winner_when_all_fold(self):
        """Test single player wins when others fold."""
        active_players = [self.players[0]]
        
        winners, score = self.determiner.determine_hand_winner(
            active_players, []
        )
        
        self.assertEqual(len(winners), 1)
        self.assertEqual(winners[0], "p1")
    
    def test_hand_ranking_integration(self):
        """Test hand ranking with real cards."""
        # Create players with specific hands
        p1 = Player("p1", "dealer", 1000, 1000)
        p1.hole_cards = [
            Card("hearts", "A"),
            Card("spades", "K")
        ]
        
        p2 = Player("p2", "sb", 1000, 1000)
        p2.hole_cards = [
            Card("diamonds", "Q"),
            Card("clubs", "J")
        ]
        
        community_cards = [
            Card("hearts", "A"),
            Card("diamonds", "K"),
            Card("clubs", "Q"),
            Card("spades", "J"),
            Card("hearts", "10")
        ]
        
        # Determine winner (p1 should have pair of Aces)
        winners, score = self.determiner.determine_hand_winner(
            [p1, p2], community_cards
        )
        
        self.assertIn("p1", winners)
    
    def test_pot_distribution_single_winner(self):
        """Test pot distribution to single winner."""
        from src.dealer_engine import Pot
        
        pot = Pot(300, ["p1", "p2", "p3"])
        distribution = self.determiner.distribute_pot(
            pot, ["p1"], {p.player_id: p for p in self.players}
        )
        
        self.assertEqual(distribution["p1"], 300)
    
    def test_pot_split_two_winners(self):
        """Test pot split evenly between two winners."""
        from src.dealer_engine import Pot
        
        pot = Pot(400, ["p1", "p2", "p3"])
        distribution = self.determiner.distribute_pot(
            pot, ["p1", "p2"], {p.player_id: p for p in self.players}
        )
        
        self.assertEqual(distribution["p1"], 200)
        self.assertEqual(distribution["p2"], 200)
    
    def test_pot_split_three_winners_with_remainder(self):
        """Test pot split with remainder going to first winner."""
        from src.dealer_engine import Pot
        
        pot = Pot(100, ["p1", "p2", "p3"])
        distribution = self.determiner.distribute_pot(
            pot, ["p1", "p2", "p3"], {p.player_id: p for p in self.players}
        )
        
        # 100 / 3 = 33 each, remainder 1 to p1
        self.assertEqual(distribution["p1"], 34)
        self.assertEqual(distribution["p2"], 33)
        self.assertEqual(distribution["p3"], 33)
    
    def test_ineligible_winner_excluded_from_split(self):
        """Test ineligible winner is not included in pot distribution."""
        from src.dealer_engine import Pot
        
        pot = Pot(300, ["p1", "p2"])  # p3 didn't contribute
        distribution = self.determiner.distribute_pot(
            pot, ["p1", "p2", "p3"], {p.player_id: p for p in self.players}
        )
        
        # p3 should not receive anything (not in contributors)
        self.assertNotIn("p3", distribution)
        self.assertEqual(distribution["p1"], 150)
        self.assertEqual(distribution["p2"], 150)
    
    def test_award_winnings_updates_stacks(self):
        """Test award_winnings correctly updates player stacks."""
        initial_stack_p1 = self.players[0].current_stack
        distribution = {"p1": 300}
        
        self.determiner.award_winnings(distribution, self.players)
        
        self.assertEqual(self.players[0].current_stack, initial_stack_p1 + 300)


class TestDealerEngineWithWinners(unittest.TestCase):
    """Test extended dealer engine with winner determination."""
    
    def setUp(self):
        """Create test engine with winner determination."""
        self.players = [
            Player("p1", "dealer", 1000, 1000),
            Player("p2", "sb", 1000, 1000),
            Player("p3", "bb", 1000, 1000),
        ]
        self.engine = DealerEngineWithWinners(
            GameType.TEXAS_HOLDEM, self.players, 25, 50
        )
        self.engine.start_game()
    
    def test_engine_has_winner_determiner(self):
        """Test engine is properly equipped with winner determiner."""
        self.assertIsNotNone(self.engine.winner_determiner)
    
    def test_finalize_hand_with_single_active_player(self):
        """Test finalize_hand when only one player remains."""
        self.engine.start_hand()
        
        # Everyone folds except one
        self.players[0].status = PlayerStatus.FOLDED
        self.players[1].status = PlayerStatus.FOLDED
        
        self.engine.players_in_hand = {"p3"}
        
        community_cards = []
        distribution = self.engine.finalize_hand(community_cards)
        
        self.assertIn("p3", distribution)
        self.assertEqual(distribution["p3"], self.engine.main_pot.amount)


class TestEdgeCasesAdvanced(unittest.TestCase):
    """Test advanced edge cases."""
    
    def test_side_pot_with_three_all_ins(self):
        """Test side pots with multiple all-in scenarios."""
        players = [
            Player("p1", "dealer", 50, 0),    # All-in for 50
            Player("p2", "sb", 200, 150),     # All-in for 200
            Player("p3", "bb", 500, 500),     # Bets 500
        ]
        
        players[0].current_bet_in_round = 50
        players[1].current_bet_in_round = 200
        players[2].current_bet_in_round = 500
        
        engine = DealerEngine(GameType.TEXAS_HOLDEM, players, 25, 50)
        main_pot, side_pots = SidePotManager.create_side_pots(engine, players)
        
        # Main pot: 50 × 3 = 150
        # Side pot 1: 150 × 2 = 300 (p2, p3)
        # Side pot 2: 300 × 1 = 300 (p3 only)
        self.assertEqual(main_pot.amount, 150)
        self.assertGreaterEqual(len(side_pots), 1)
    
    def test_pot_with_no_eligible_winners(self):
        """Test pot distribution when no player is eligible (edge case)."""
        from src.dealer_engine import Pot
        
        determiner = WinnerDeterminer()
        pot = Pot(100, ["p1", "p2"])
        
        # Try to distribute to ineligible player
        distribution = determiner.distribute_pot(
            pot, ["p3", "p4"], {"p1": None, "p2": None, "p3": None, "p4": None}
        )
        
        # Should return empty distribution
        self.assertEqual(len(distribution), 0)


if __name__ == "__main__":
    unittest.main()
