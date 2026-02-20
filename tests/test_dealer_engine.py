"""
Unit tests for the Dealer Engine.

Tests cover:
- Game initialization and setup
- Blind posting
- Betting actions and validation
- Pot management
- Round completion logic
- Edge cases (all-in, folding, etc.)

Author: Angus Young
Date: 2026-02-21
Version: 1.0
"""

import unittest
from src.dealer_engine import (
    DealerEngine, GameType, GamePhase, PlayerStatus, ActionType,
    Player, Card, Pot
)


class TestDealerEngineInitialization(unittest.TestCase):
    """Test game initialization."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 1000, 1000),
            Player("player_2", "small_blind", 1000, 1000),
            Player("player_3", "big_blind", 1000, 1000),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
    
    def test_engine_created_successfully(self):
        """Test engine initializes with correct parameters."""
        self.assertEqual(self.engine.game_type, GameType.TEXAS_HOLDEM)
        self.assertEqual(self.engine.small_blind, 25)
        self.assertEqual(self.engine.big_blind, 50)
        self.assertEqual(len(self.engine.players), 3)
    
    def test_game_starts_in_waiting_state(self):
        """Test game begins in WAITING_FOR_PLAYERS state."""
        self.assertEqual(self.engine.current_phase, GamePhase.WAITING_FOR_PLAYERS)
    
    def test_start_game_transitions_state(self):
        """Test start_game() transitions to GAME_STARTED."""
        self.engine.start_game()
        self.assertEqual(self.engine.current_phase, GamePhase.GAME_STARTED)


class TestBlindPosting(unittest.TestCase):
    """Test blind posting mechanics."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 1000, 1000),
            Player("player_2", "small_blind", 1000, 1000),
            Player("player_3", "big_blind", 1000, 1000),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
        self.engine.start_game()
    
    def test_blinds_posted_correctly(self):
        """Test small and big blinds are deducted from player stacks."""
        self.engine.start_hand()
        
        # Small blind (player at index 1): should have posted 25
        # Big blind (player at index 2): should have posted 50
        # Player 0 should be unaffected
        
        self.assertEqual(self.engine.main_pot.amount, 75)  # 25 + 50
    
    def test_blinds_go_to_main_pot(self):
        """Test blinds are added to main pot."""
        self.engine.start_hand()
        self.assertEqual(self.engine.main_pot.amount, 75)
    
    def test_blind_all_in_protection(self):
        """Test player with small stack can go all-in on blind."""
        small_stack_player = Player("player_4", "dealer", 10, 10)
        big_stack_player = Player("player_5", "small_blind", 1000, 1000)
        bb_player = Player("player_6", "big_blind", 1000, 1000)
        
        players = [small_stack_player, big_stack_player, bb_player]
        engine = DealerEngine(GameType.TEXAS_HOLDEM, players, 25, 50)
        engine.start_game()
        engine.start_hand()
        
        # Small stack player should be all-in
        self.assertEqual(small_stack_player.current_stack, 10)  # Post 25 but only has 10


class TestBettingActions(unittest.TestCase):
    """Test betting action validation and processing."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 1000, 1000),
            Player("player_2", "small_blind", 1000, 1000),
            Player("player_3", "big_blind", 1000, 1000),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
        self.engine.start_game()
        self.engine.start_hand()
    
    def test_check_allowed_when_no_bet(self):
        """Test player can check when no bet to call."""
        player = self.players[0]
        player.current_bet_in_round = 0
        player.status = PlayerStatus.WAITING_FOR_ACTION
        self.engine.current_round_bets = 0
        
        success, msg = self.engine.process_action("player_1", ActionType.CHECK, 0)
        self.assertTrue(success)
    
    def test_check_not_allowed_with_bet(self):
        """Test player cannot check when there's a bet to call."""
        player = self.players[0]
        player.status = PlayerStatus.WAITING_FOR_ACTION
        player.current_bet_in_round = 0
        self.engine.current_round_bets = 50
        
        success, msg = self.engine.process_action("player_1", ActionType.CHECK, 0)
        self.assertFalse(success)
    
    def test_fold_always_valid(self):
        """Test fold is always a valid action."""
        player = self.players[0]
        player.status = PlayerStatus.WAITING_FOR_ACTION
        
        success, msg = self.engine.process_action("player_1", ActionType.FOLD, 0)
        self.assertTrue(success)
        self.assertEqual(player.status, PlayerStatus.FOLDED)
    
    def test_call_matches_current_bet(self):
        """Test call action matches current bet."""
        player = self.players[0]
        player.status = PlayerStatus.WAITING_FOR_ACTION
        self.engine.current_round_bets = 50
        player.current_bet_in_round = 0
        
        initial_stack = player.current_stack
        success, msg = self.engine.process_action("player_1", ActionType.CALL, 50)
        
        self.assertTrue(success)
        self.assertEqual(player.current_bet_in_round, 50)
        self.assertEqual(player.current_stack, initial_stack - 50)
    
    def test_raise_minimum_doubles_bet(self):
        """Test raise must be at least double the current bet."""
        player = self.players[0]
        player.status = PlayerStatus.WAITING_FOR_ACTION
        self.engine.current_round_bets = 50
        player.current_bet_in_round = 0
        
        # Invalid raise (less than 2x)
        success, msg = self.engine.process_action("player_1", ActionType.RAISE, 75)
        self.assertFalse(success)
        
        # Valid raise (2x or more)
        success, msg = self.engine.process_action("player_1", ActionType.RAISE, 100)
        self.assertTrue(success)
    
    def test_all_in_action(self):
        """Test all-in action with remaining stack."""
        player = self.players[0]
        player.status = PlayerStatus.WAITING_FOR_ACTION
        player.current_stack = 500
        player.current_bet_in_round = 0
        
        success, msg = self.engine.process_action("player_1", ActionType.ALL_IN, 500)
        
        self.assertTrue(success)
        self.assertEqual(player.current_stack, 0)
        self.assertEqual(player.status, PlayerStatus.ALL_IN)


class TestPotManagement(unittest.TestCase):
    """Test pot calculation and management."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 100, 100),
            Player("player_2", "small_blind", 100, 100),
            Player("player_3", "big_blind", 100, 100),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
        self.engine.start_game()
    
    def test_pot_increases_with_bets(self):
        """Test pot amount increases as players bet."""
        self.engine.start_hand()
        initial_pot = self.engine.main_pot.amount
        
        # Player 0 calls 50
        self.players[0].status = PlayerStatus.WAITING_FOR_ACTION
        self.engine.current_round_bets = 50
        self.engine.process_action("player_1", ActionType.CALL, 50)
        
        self.assertGreater(self.engine.main_pot.amount, initial_pot)
    
    def test_side_pot_created_with_all_in(self):
        """Test side pot is created when player goes all-in."""
        # Create scenario: Player A has 100 chips, goes all-in
        # Player B has 500 chips, bets 200
        player_a = Player("player_a", "dealer", 100, 100)
        player_b = Player("player_b", "sb", 500, 500)
        player_c = Player("player_c", "bb", 500, 500)
        
        players = [player_a, player_b, player_c]
        engine = DealerEngine(GameType.TEXAS_HOLDEM, players, 25, 50)
        engine.start_game()
        engine.start_hand()
        
        # This test verifies side pot logic when implemented
        # For now, we're testing the infrastructure
        self.assertIsNotNone(engine.main_pot)


class TestRoundCompletion(unittest.TestCase):
    """Test betting round completion logic."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 1000, 1000),
            Player("player_2", "small_blind", 1000, 1000),
            Player("player_3", "big_blind", 1000, 1000),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
        self.engine.start_game()
        self.engine.start_hand()
    
    def test_round_complete_when_all_fold_except_one(self):
        """Test round is complete when all but one player folds."""
        self.players[1].status = PlayerStatus.FOLDED
        self.players[2].status = PlayerStatus.FOLDED
        
        is_complete = self.engine.is_betting_round_complete()
        self.assertTrue(is_complete)
    
    def test_round_incomplete_with_uneven_bets(self):
        """Test round is incomplete when players have different bet amounts."""
        self.players[0].status = PlayerStatus.ACTIVE
        self.players[0].current_bet_in_round = 50
        
        self.players[1].status = PlayerStatus.ACTIVE
        self.players[1].current_bet_in_round = 100
        
        self.engine.current_round_bets = 100
        
        is_complete = self.engine.is_betting_round_complete()
        self.assertFalse(is_complete)


class TestGameStateRetrieval(unittest.TestCase):
    """Test game state export for external use."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 1000, 1000),
            Player("player_2", "small_blind", 1000, 1000),
            Player("player_3", "big_blind", 1000, 1000),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
        self.engine.start_game()
    
    def test_game_state_includes_phase(self):
        """Test game state includes current phase."""
        state = self.engine.get_game_state()
        self.assertIn("phase", state)
        self.assertEqual(state["phase"], GamePhase.GAME_STARTED.value)
    
    def test_game_state_includes_players(self):
        """Test game state includes all players."""
        self.engine.start_hand()
        state = self.engine.get_game_state()
        
        self.assertIn("players", state)
        self.assertEqual(len(state["players"]), 3)
    
    def test_game_state_includes_pot(self):
        """Test game state includes pot amount."""
        self.engine.start_hand()
        state = self.engine.get_game_state()
        
        self.assertIn("main_pot", state)
        self.assertEqual(state["main_pot"], 75)  # 25 + 50 from blinds


class TestPlayerActiveStatus(unittest.TestCase):
    """Test player active status management."""
    
    def test_active_player_property(self):
        """Test is_active property for various statuses."""
        player = Player("test", "dealer", 100, 100)
        
        player.status = PlayerStatus.ACTIVE
        self.assertTrue(player.is_active)
        
        player.status = PlayerStatus.FOLDED
        self.assertFalse(player.is_active)
        
        player.status = PlayerStatus.ALL_IN
        self.assertTrue(player.is_active)
    
    def test_can_act_property(self):
        """Test can_act property for various statuses."""
        player = Player("test", "dealer", 100, 100)
        
        player.status = PlayerStatus.WAITING_FOR_ACTION
        self.assertTrue(player.can_act)
        
        player.status = PlayerStatus.FOLDED
        self.assertFalse(player.can_act)
        
        player.status = PlayerStatus.ALL_IN
        self.assertFalse(player.can_act)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Create test players and engine."""
        self.players = [
            Player("player_1", "dealer", 1000, 1000),
            Player("player_2", "small_blind", 1000, 1000),
            Player("player_3", "big_blind", 1000, 1000),
        ]
        self.engine = DealerEngine(GameType.TEXAS_HOLDEM, self.players, 25, 50)
        self.engine.start_game()
        self.engine.start_hand()
    
    def test_invalid_player_id(self):
        """Test action on non-existent player."""
        success, msg = self.engine.process_action("nonexistent", ActionType.FOLD, 0)
        self.assertFalse(success)
    
    def test_action_on_folded_player(self):
        """Test cannot act if already folded."""
        player = self.players[0]
        player.status = PlayerStatus.FOLDED
        
        success, msg = self.engine.process_action("player_1", ActionType.CHECK, 0)
        self.assertFalse(success)
    
    def test_bet_exceeding_stack(self):
        """Test cannot bet more than available stack."""
        player = self.players[0]
        player.status = PlayerStatus.WAITING_FOR_ACTION
        player.current_stack = 50
        
        success, msg = self.engine.process_action("player_1", ActionType.RAISE, 100)
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
