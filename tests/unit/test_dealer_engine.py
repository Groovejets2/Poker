"""Comprehensive tests for DealerEngine class - integration tests."""

import pytest
from poker_engine.card import Card
from poker_engine.player_state import PlayerState, PlayerStatus
from poker_engine.game_state import GameState, GamePhase
from poker_engine.dealer_engine import DealerEngine, GameType
from poker_engine.betting_validator import ActionType


class TestDealerEngineInitialisation:
    """Test DealerEngine creation and setup."""
    
    def test_create_valid_dealer_engine(self):
        """Test creating a valid dealer engine."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        assert engine.game_type == GameType.TEXAS_HOLDEM
        assert len(engine.game_state.players) == 2
        assert engine.small_blind_amount == 10
        assert engine.big_blind_amount == 20
    
    def test_create_engine_invalid_player_count(self):
        """Test that invalid player count raises ValueError."""
        players = [PlayerState("bot_1", 0, 1000)]
        
        with pytest.raises(ValueError, match="2-8 players"):
            DealerEngine(
                game_type=GameType.TEXAS_HOLDEM,
                players=players,
                small_blind_amount=10,
                big_blind_amount=20
            )
    
    def test_create_engine_invalid_blinds(self):
        """Test that invalid blind amounts raise ValueError."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        
        with pytest.raises(ValueError, match="Big blind"):
            DealerEngine(
                game_type=GameType.TEXAS_HOLDEM,
                players=players,
                small_blind_amount=20,
                big_blind_amount=20
            )
    
    def test_create_engine_with_custom_game_id(self):
        """Test creating engine with custom game ID."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20,
            game_id="custom_game_123"
        )
        
        assert engine.game_state.game_id == "custom_game_123"
    
    def test_create_engine_five_card_draw(self):
        """Test creating engine for Five Card Draw variant."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.FIVE_CARD_DRAW,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        assert engine.game_type == GameType.FIVE_CARD_DRAW


class TestHandLifecycle:
    """Test starting and ending hands."""
    
    def test_start_hand_initialises_game(self):
        """Test that start_hand initialises the game properly."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        assert engine.game_state.current_phase == GamePhase.PRE_FLOP
        assert engine.game_state.current_action_player is not None
    
    def test_start_hand_resets_players(self):
        """Test that start_hand resets player states."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        # Fold a player before starting
        players[0].fold()
        
        engine.start_hand()
        
        # After start_hand, both should be active again
        assert players[0].status == PlayerStatus.ACTIVE
        assert players[1].status == PlayerStatus.ACTIVE
    
    def test_end_hand_transitions_phase(self):
        """Test that end_hand advances phase."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        engine.end_hand()
        
        assert engine.game_state.current_phase == GamePhase.HAND_COMPLETE


class TestGameSizing:
    """Test games with different player counts."""
    
    def test_two_player_game_heads_up(self):
        """Test heads-up game with two players."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        assert len(engine.game_state.players) == 2
    
    def test_three_player_game(self):
        """Test game with three players."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000)
        ]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        assert len(engine.game_state.players) == 3
    
    def test_six_player_game(self):
        """Test typical 6-max game."""
        players = [PlayerState(f"bot_{i}", i, 1000) for i in range(6)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        assert len(engine.game_state.players) == 6
    
    def test_eight_player_game(self):
        """Test maximum size 8-player game."""
        players = [PlayerState(f"bot_{i}", i, 1000) for i in range(8)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        assert len(engine.game_state.players) == 8


class TestBettingIntegration:
    """Test betting interactions with dealer engine."""
    
    def test_process_valid_action(self):
        """Test processing a valid betting action."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        # Get current action player
        current_seat = engine.game_state.current_action_player
        current_player_id = engine.game_state.players[current_seat].player_id
        
        # Get current bet amount to match
        max_bet = max(p.current_bet for p in engine.game_state.get_active_players())
        
        # Process action - call if someone has bet, otherwise check
        if max_bet > 0:
            call_amount = max_bet - engine.game_state.players[current_seat].current_bet
            engine.betting_validator.validate_action(
                current_player_id,
                ActionType.CALL,
                amount=call_amount
            )
        else:
            engine.betting_validator.validate_action(
                current_player_id,
                ActionType.CHECK
            )
        # Should not raise
    
    def test_pot_manager_tracks_bets(self):
        """Test that pot manager tracks player bets."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        # Add to pot
        engine.pot_manager.add_to_pot("bot_1", 50)
        
        assert engine.pot_manager.get_player_contribution("bot_1") == 50


class TestCommunityCards:
    """Test community card management."""
    
    def test_reveal_flop(self):
        """Test revealing flop cards."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        flop = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q")
        ]
        
        for card in flop:
            engine.game_state.reveal_community_card(card)
        
        assert len(engine.game_state.community_cards) == 3
    
    def test_reveal_turn(self):
        """Test revealing turn card."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        # Reveal flop
        for card in [Card("hearts", "A"), Card("spades", "K"), Card("diamonds", "Q")]:
            engine.game_state.reveal_community_card(card)
        
        # Reveal turn
        engine.game_state.reveal_community_card(Card("clubs", "J"))
        
        assert len(engine.game_state.community_cards) == 4
    
    def test_reveal_river(self):
        """Test revealing river card (all 5 community cards)."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        # Reveal all 5 cards
        community = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "10")
        ]
        
        for card in community:
            engine.game_state.reveal_community_card(card)
        
        assert len(engine.game_state.community_cards) == 5


class TestButtonMovement:
    """Test dealer button movement across hands."""
    
    def test_button_moves_after_hand(self):
        """Test that button moves clockwise after hand."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000)
        ]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        initial_button = engine.game_state.dealer_button
        
        engine.start_hand()
        # Button position after start_hand (moved during reset)
        button_after_start = engine.game_state.dealer_button
        
        engine.end_hand()
        engine.start_hand()
        
        # Button should have moved again (it moves during reset_for_new_hand)
        button_after_second_start = engine.game_state.dealer_button
        # Should be different from the first start
        assert button_after_second_start != button_after_start


class TestActionSequence:
    """Test sequences of actions in a hand."""
    
    def test_check_check_sequence(self):
        """Test check-check sequence."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        # Both players can check if no one has bet
        # Set up state for valid check
        current_seat = engine.game_state.current_action_player
        current_player_id = engine.game_state.players[current_seat].player_id
        
        # Clear any forced bets (blinds)
        engine.game_state.players[0].current_bet = 0
        engine.game_state.players[1].current_bet = 0
        
        # Both can check
        engine.betting_validator.validate_action(
            current_player_id,
            ActionType.CHECK
        )
    
    def test_bet_call_sequence(self):
        """Test bet-call sequence."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        # Clear bets for clean test
        for player in engine.game_state.players:
            player.current_bet = 0
        
        current_seat = engine.game_state.current_action_player
        current_player_id = engine.game_state.players[current_seat].player_id
        
        # Player bets 50
        engine.betting_validator.validate_action(
            current_player_id,
            ActionType.BET,
            amount=50
        )


class TestGamePhaseTransitions:
    """Test game phase transitions."""
    
    def test_blinds_posted_phase(self):
        """Test BLINDS_POSTED phase."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        
        # After start_hand, should be in PRE_FLOP (after blinds are posted)
        assert engine.game_state.current_phase == GamePhase.PRE_FLOP
    
    def test_flop_phase_transition(self):
        """Test transitioning to FLOP phase."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        engine.game_state.advance_phase(GamePhase.FLOP)
        
        assert engine.game_state.current_phase == GamePhase.FLOP
    
    def test_showdown_phase(self):
        """Test transitioning to SHOWDOWN phase."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        engine.start_hand()
        engine.game_state.advance_phase(GamePhase.SHOWDOWN)
        
        assert engine.game_state.current_phase == GamePhase.SHOWDOWN


class TestEdgeCases:
    """Test edge cases and unusual scenarios."""
    
    def test_short_stack_player(self):
        """Test game with short stack player."""
        players = [PlayerState("bot_1", 0, 50), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        initial_stack = engine.game_state.players[0].stack
        engine.start_hand()
        
        # After start_hand, blinds are posted, so stack may be reduced
        # Just verify the short stack player still exists with a lower stack
        assert engine.game_state.players[0].stack <= initial_stack
    
    def test_large_blinds(self):
        """Test with large blind sizes."""
        players = [PlayerState("bot_1", 0, 10000), PlayerState("bot_2", 1, 10000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=500,
            big_blind_amount=1000
        )
        
        assert engine.small_blind_amount == 500
        assert engine.big_blind_amount == 1000
    
    def test_minimum_blinds(self):
        """Test with minimum blind sizes."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=1,
            big_blind_amount=2
        )
        
        assert engine.small_blind_amount == 1
        assert engine.big_blind_amount == 2


class TestMultipleHands:
    """Test running multiple consecutive hands."""
    
    def test_two_hands_in_sequence(self):
        """Test running two hands back-to-back."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        # Hand 1
        engine.start_hand()
        button_after_hand1 = engine.game_state.dealer_button
        engine.end_hand()
        
        # Hand 2
        engine.start_hand()
        button_after_hand2 = engine.game_state.dealer_button
        
        # Button should have moved
        assert button_after_hand2 != button_after_hand1
    
    def test_three_hands_with_button_rotation(self):
        """Test three hands with button rotation."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000)
        ]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        initial_button = engine.game_state.dealer_button
        buttons = [initial_button]
        
        for _ in range(3):
            engine.start_hand()
            engine.end_hand()
            buttons.append(engine.game_state.dealer_button)
        
        # All buttons should be different in sequence
        for i in range(len(buttons) - 1):
            expected = (buttons[i] + 1) % 3
            assert buttons[i + 1] == expected


class TestDealerEngineRepr:
    """Test string representation."""
    
    def test_dealer_engine_repr_contains_game_id(self):
        """Test that repr contains game ID."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20,
            game_id="test_game"
        )
        
        repr_str = repr(engine.game_state)
        assert "test_game" in repr_str


class TestComplexGameScenario:
    """Test complex real-world game scenarios."""
    
    def test_full_game_lifecycle(self):
        """Test a complete game lifecycle."""
        players = [
            PlayerState("alice", 0, 1000),
            PlayerState("bob", 1, 1000),
            PlayerState("charlie", 2, 1000)
        ]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=10,
            big_blind_amount=20
        )
        
        # Start hand
        engine.start_hand()
        assert engine.game_state.current_phase == GamePhase.PRE_FLOP
        
        # Move to flop
        engine.game_state.advance_phase(GamePhase.FLOP)
        flop = [Card("hearts", "A"), Card("spades", "K"), Card("diamonds", "Q")]
        for card in flop:
            engine.game_state.reveal_community_card(card)
        
        # Move to turn
        engine.game_state.advance_phase(GamePhase.TURN)
        engine.game_state.reveal_community_card(Card("clubs", "J"))
        
        # Move to river
        engine.game_state.advance_phase(GamePhase.RIVER)
        engine.game_state.reveal_community_card(Card("hearts", "10"))
        
        # Move to showdown
        engine.game_state.advance_phase(GamePhase.SHOWDOWN)
        
        # Finish hand
        engine.end_hand()
        assert engine.game_state.current_phase == GamePhase.HAND_COMPLETE
    
    def test_game_with_all_in_scenario(self):
        """Test game where player goes all-in."""
        players = [
            PlayerState("short_stack", 0, 50),
            PlayerState("big_stack", 1, 5000)
        ]
        engine = DealerEngine(
            game_type=GameType.TEXAS_HOLDEM,
            players=players,
            small_blind_amount=5,
            big_blind_amount=10
        )
        
        engine.start_hand()
        
        # Short stack player
        short_stack = players[0]
        initial_stack = short_stack.stack  # Will have blinds deducted
        
        # Can go all-in with remaining stack
        remaining = short_stack.stack
        if remaining > 0:
            short_stack.post_bet(remaining)
            short_stack.go_all_in()
            
            assert short_stack.status == PlayerStatus.ALL_IN
            assert short_stack.stack == 0
