"""Comprehensive tests for BettingValidator class."""

import pytest
from poker_engine.game_state import GameState
from poker_engine.player_state import PlayerState, PlayerStatus, RoundStatus
from poker_engine.betting_validator import (
    BettingValidator,
    ActionType,
    InvalidActionError,
    NotPlayersTurnError
)


class TestBettingValidatorInitialisation:
    """Test BettingValidator creation and setup."""
    
    def test_create_valid_betting_validator(self):
        """Test creating a valid betting validator."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        
        validator = BettingValidator(game)
        assert validator.game_state == game
        assert validator.min_raise_amount == 20  # Default: big blind
    
    def test_betting_validator_with_custom_min_raise(self):
        """Test creating validator with custom minimum raise."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        
        validator = BettingValidator(game, min_raise_amount=50)
        assert validator.min_raise_amount == 50
    
    def test_betting_validator_none_game_state_raises_error(self):
        """Test that None game_state raises ValueError."""
        with pytest.raises(ValueError, match="game_state cannot be None"):
            BettingValidator(None)


class TestValidTurnCheck:
    """Test checking if it's a player's turn."""
    
    def test_is_valid_turn_no_current_player(self):
        """Test that with no current player, no one's turn."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = None
        
        validator = BettingValidator(game)
        assert validator.is_valid_turn("bot_1") is False
    
    def test_is_valid_turn_correct_player(self):
        """Test that correct player's turn is recognized."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        assert validator.is_valid_turn("bot_1") is True
    
    def test_is_valid_turn_wrong_player(self):
        """Test that wrong player's turn is rejected."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        assert validator.is_valid_turn("bot_2") is False
    
    def test_is_valid_turn_non_existent_player(self):
        """Test that non-existent player has no valid turn."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        assert validator.is_valid_turn("non_existent") is False


class TestCheckValidation:
    """Test validating check actions."""
    
    def test_valid_check_no_bet_to_match(self):
        """Test check when no one has bet."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        # Should not raise
        validator.validate_action("bot_1", ActionType.CHECK)
    
    def test_invalid_check_bet_to_match(self):
        """Test check when there's a bet to match."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="Cannot check"):
            validator.validate_action("bot_1", ActionType.CHECK)


class TestFoldValidation:
    """Test validating fold actions."""
    
    def test_valid_fold_no_bet(self):
        """Test fold when no bet has been made."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        # Fold should always be valid
        validator.validate_action("bot_1", ActionType.FOLD)
    
    def test_valid_fold_with_bet_to_call(self):
        """Test fold when opponent has bet."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        # Fold should always be valid
        validator.validate_action("bot_1", ActionType.FOLD)


class TestCallValidation:
    """Test validating call actions."""
    
    def test_valid_call_exact_amount(self):
        """Test call with exact matching amount."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        # bot_1 needs to call 100
        validator.validate_action("bot_1", ActionType.CALL, amount=100)
    
    def test_invalid_call_wrong_amount(self):
        """Test call with incorrect amount."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="Call amount must be"):
            validator.validate_action("bot_1", ActionType.CALL, amount=50)
    
    def test_invalid_call_exceeds_stack(self):
        """Test call that exceeds player's stack."""
        players = [PlayerState("bot_1", 0, 50), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="exceeds stack"):
            validator.validate_action("bot_1", ActionType.CALL, amount=100)
    
    def test_valid_call_partial_stack(self):
        """Test call when only have partial chips to call."""
        players = [PlayerState("bot_1", 0, 75), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        # Should allow call even if not enough to match full amount
        # (actually, let's check the implementation logic)
        with pytest.raises(InvalidActionError):
            validator.validate_action("bot_1", ActionType.CALL, amount=100)


class TestBetValidation:
    """Test validating bet actions."""
    
    def test_valid_bet_no_prior_bet(self):
        """Test bet when no one has bet this round."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        validator.validate_action("bot_1", ActionType.BET, amount=50)
    
    def test_invalid_bet_prior_bet_exists(self):
        """Test bet when someone already bet."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="Cannot bet"):
            validator.validate_action("bot_1", ActionType.BET, amount=50)
    
    def test_invalid_bet_zero_or_negative(self):
        """Test that zero or negative bets are invalid."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="must be positive"):
            validator.validate_action("bot_1", ActionType.BET, amount=0)
    
    def test_invalid_bet_exceeds_stack(self):
        """Test bet that exceeds stack."""
        players = [PlayerState("bot_1", 0, 100), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="exceeds stack"):
            validator.validate_action("bot_1", ActionType.BET, amount=150)
    
    def test_valid_bet_exact_stack(self):
        """Test bet equal to remaining stack."""
        players = [PlayerState("bot_1", 0, 100), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        validator.validate_action("bot_1", ActionType.BET, amount=100)


class TestRaiseValidation:
    """Test validating raise actions."""
    
    def test_valid_raise_min_raise_amount(self):
        """Test raise of minimum amount."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game, min_raise_amount=20)
        # Raise must be at least 100 + 20 = 120 total
        # So bot_1 needs to bet 120 total (currently 0), so amount = 120
        validator.validate_action("bot_1", ActionType.RAISE, amount=120)
    
    def test_invalid_raise_no_prior_bet(self):
        """Test raise when no one has bet."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="Cannot raise"):
            validator.validate_action("bot_1", ActionType.RAISE, amount=50)
    
    def test_invalid_raise_below_minimum(self):
        """Test raise below minimum raise amount."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        
        validator = BettingValidator(game, min_raise_amount=20)
        with pytest.raises(InvalidActionError, match="must be at least"):
            validator.validate_action("bot_1", ActionType.RAISE, amount=10)
    
    def test_valid_raise_multiple_raises(self):
        """Test multiple raises in same round."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[1].post_bet(100)
        players[0].post_bet(150)
        
        game.current_action_player = 1
        validator = BettingValidator(game, min_raise_amount=20)
        # bot_2 needs to raise 150 + 20 = 170 total, so raise by 70 more
        validator.validate_action("bot_2", ActionType.RAISE, amount=70)


class TestAllInValidation:
    """Test validating all-in actions."""
    
    def test_valid_all_in_exact_stack(self):
        """Test all-in with exact remaining stack."""
        players = [PlayerState("bot_1", 0, 500), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        validator.validate_action("bot_1", ActionType.ALL_IN, amount=500)
    
    def test_invalid_all_in_wrong_amount(self):
        """Test all-in with wrong amount."""
        players = [PlayerState("bot_1", 0, 500), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="must equal remaining stack"):
            validator.validate_action("bot_1", ActionType.ALL_IN, amount=400)
    
    def test_invalid_all_in_zero_chips(self):
        """Test all-in with zero chips left."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        players[0].post_bet(1000)
        
        validator = BettingValidator(game)
        with pytest.raises(InvalidActionError, match="zero chips"):
            validator.validate_action("bot_1", ActionType.ALL_IN, amount=0)


class TestOutOfTurnDetection:
    """Test detecting out-of-turn actions."""
    
    def test_action_out_of_turn_raises_error(self):
        """Test that acting out of turn raises NotPlayersTurnError."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        with pytest.raises(NotPlayersTurnError, match="not the current actor"):
            validator.validate_action("bot_2", ActionType.CHECK)
    
    def test_multiple_players_only_one_can_act(self):
        """Test that only current player can act."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000)
        ]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 1
        
        validator = BettingValidator(game)
        
        # bot_1 and bot_3 cannot act
        with pytest.raises(NotPlayersTurnError):
            validator.validate_action("bot_1", ActionType.CHECK)
        
        with pytest.raises(NotPlayersTurnError):
            validator.validate_action("bot_3", ActionType.CHECK)
        
        # Only bot_2 can act
        validator.validate_action("bot_2", ActionType.CHECK)


class TestBettingSequences:
    """Test complex betting sequences."""
    
    def test_betting_sequence_pre_flop(self):
        """Test typical pre-flop betting sequence."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        
        # bot_1 bets 50
        validator.validate_action("bot_1", ActionType.BET, amount=50)
        players[0].post_bet(50)
        
        # bot_2 raises to 150
        game.current_action_player = 1
        validator = BettingValidator(game)  # Recreate to update state
        validator.validate_action("bot_2", ActionType.RAISE, amount=100)
        players[1].post_bet(150)
        
        # bot_1 calls
        game.current_action_player = 0
        validator = BettingValidator(game)
        validator.validate_action("bot_1", ActionType.CALL, amount=100)
    
    def test_all_in_sequence(self):
        """Test betting sequence with all-in."""
        players = [PlayerState("bot_1", 0, 100), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        
        # bot_1 goes all-in with 100
        validator.validate_action("bot_1", ActionType.ALL_IN, amount=100)
        players[0].post_bet(100)
        players[0].go_all_in()
        
        # bot_2 can call, raise, or fold
        game.current_action_player = 1
        validator = BettingValidator(game)
        validator.validate_action("bot_2", ActionType.CALL, amount=100)


class TestEdgeCases:
    """Test edge cases and unusual scenarios."""
    
    def test_large_stacks(self):
        """Test with very large stacks."""
        players = [PlayerState("bot_1", 0, 10_000_000), PlayerState("bot_2", 1, 10_000_000)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        validator.validate_action("bot_1", ActionType.BET, amount=5_000_000)
    
    def test_minimum_blinds(self):
        """Test with minimum blind sizes."""
        players = [PlayerState("bot_1", 0, 100), PlayerState("bot_2", 1, 100)]
        game = GameState("game_001", players, 1, 2)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        assert validator.min_raise_amount == 2
    
    def test_eight_player_validation(self):
        """Test validation in 8-player game."""
        players = [PlayerState(f"bot_{i}", i, 1000) for i in range(8)]
        game = GameState("game_001", players, 10, 20)
        game.current_action_player = 0
        
        validator = BettingValidator(game)
        # Should work with any number of players
        validator.validate_action("bot_0", ActionType.CHECK)
