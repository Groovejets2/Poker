"""Unit tests for GameState and enums."""

import pytest
from poker_engine.card import Card
from poker_engine.game_state import (
    GameState,
    GamePhase,
    SidePot,
)
from poker_engine.player_state import (
    PlayerState,
    PlayerStatus,
)


class TestGamePhase:
    """Tests for GamePhase enum."""
    
    def test_all_game_phases_defined(self):
        """Test that all required game phases are defined."""
        phases = [
            GamePhase.WAITING_FOR_PLAYERS,
            GamePhase.GAME_STARTED,
            GamePhase.BLINDS_POSTED,
            GamePhase.PRE_FLOP,
            GamePhase.FLOP,
            GamePhase.TURN,
            GamePhase.RIVER,
            GamePhase.SHOWDOWN,
            GamePhase.POT_DISTRIBUTION,
            GamePhase.HAND_COMPLETE,
        ]
        assert len(phases) == 10
    
    def test_phase_values(self):
        """Test that phases have correct string values."""
        assert GamePhase.BLINDS_POSTED.value == "BLINDS_POSTED"
        assert GamePhase.PRE_FLOP.value == "PRE_FLOP"
        assert GamePhase.SHOWDOWN.value == "SHOWDOWN"


class TestSidePot:
    """Tests for SidePot class."""
    
    def test_side_pot_init_valid(self):
        """Test creating a valid side pot."""
        pot = SidePot(100, ["bot_1", "bot_2"])
        assert pot.amount == 100
        assert pot.eligible_players == ["bot_1", "bot_2"]
    
    def test_side_pot_init_invalid_amount_zero(self):
        """Test that zero amount raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            SidePot(0, ["bot_1"])
    
    def test_side_pot_init_invalid_amount_negative(self):
        """Test that negative amount raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            SidePot(-50, ["bot_1"])
    
    def test_side_pot_init_empty_players(self):
        """Test that empty player list raises ValueError."""
        with pytest.raises(ValueError, match="at least one eligible"):
            SidePot(100, [])
    
    def test_side_pot_eligible_players_copied(self):
        """Test that eligible_players list is copied (not referenced)."""
        players = ["bot_1", "bot_2"]
        pot = SidePot(100, players)
        players.append("bot_3")
        assert len(pot.eligible_players) == 2
    
    def test_side_pot_repr(self):
        """Test side pot string representation."""
        pot = SidePot(100, ["bot_1", "bot_2"])
        repr_str = repr(pot)
        assert "100" in repr_str
        assert "2" in repr_str


class TestGameStateInitialisation:
    """Tests for GameState initialisation."""
    
    def test_game_state_init_valid_two_players(self):
        """Test creating game with 2 players."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        assert game.game_id == "game_1"
        assert len(game.players) == 2
        assert game.current_phase == GamePhase.WAITING_FOR_PLAYERS
        assert game.main_pot == 0
        assert game.side_pots == []
        assert game.community_cards == []
        assert game.dealer_button == 0
        assert game.small_blind_amount == 10
        assert game.big_blind_amount == 20
    
    def test_game_state_init_valid_eight_players(self):
        """Test creating game with maximum 8 players."""
        players = [PlayerState(f"bot_{i}", i, 1000) for i in range(8)]
        game = GameState("game_1", players, 10, 20)
        assert len(game.players) == 8
    
    def test_game_state_init_invalid_one_player(self):
        """Test that 1 player raises ValueError."""
        players = [PlayerState("bot_1", 0, 1000)]
        with pytest.raises(ValueError, match="2-8 players"):
            GameState("game_1", players, 10, 20)
    
    def test_game_state_init_invalid_nine_players(self):
        """Test that 9 players raises ValueError."""
        players = [PlayerState(f"bot_{i}", i, 1000) for i in range(9)]
        with pytest.raises(ValueError, match="2-8 players"):
            GameState("game_1", players, 10, 20)
    
    def test_game_state_init_invalid_small_blind_zero(self):
        """Test that zero small blind raises ValueError."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        with pytest.raises(ValueError, match="Small blind must be positive"):
            GameState("game_1", players, 0, 20)
    
    def test_game_state_init_invalid_big_blind_equal_small(self):
        """Test that big blind equal to small blind raises ValueError."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        with pytest.raises(ValueError, match="must be > small blind"):
            GameState("game_1", players, 10, 10)
    
    def test_game_state_init_invalid_big_blind_less_than_small(self):
        """Test that big blind less than small blind raises ValueError."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        with pytest.raises(ValueError, match="must be > small blind"):
            GameState("game_1", players, 20, 10)
    
    def test_game_state_init_invalid_dealer_button_negative(self):
        """Test that negative dealer button raises ValueError."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        with pytest.raises(ValueError, match="out of range"):
            GameState("game_1", players, 10, 20, dealer_button=-1)
    
    def test_game_state_init_invalid_dealer_button_too_high(self):
        """Test that dealer button >= player count raises ValueError."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        with pytest.raises(ValueError, match="out of range"):
            GameState("game_1", players, 10, 20, dealer_button=2)


class TestGameStatePotManagement:
    """Tests for pot management methods."""
    
    def test_add_to_main_pot_valid(self):
        """Test adding to main pot."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(50)
        assert game.main_pot == 50
    
    def test_add_to_main_pot_multiple_times(self):
        """Test adding to main pot multiple times."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(50)
        game.add_to_main_pot(30)
        assert game.main_pot == 80
    
    def test_add_to_main_pot_zero(self):
        """Test adding zero to pot (should be allowed)."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(0)
        assert game.main_pot == 0
    
    def test_add_to_main_pot_negative(self):
        """Test that adding negative amount raises ValueError."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        with pytest.raises(ValueError, match="cannot be negative"):
            game.add_to_main_pot(-50)
    
    def test_create_side_pot(self):
        """Test creating a side pot."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.create_side_pot(100, ["bot_2", "bot_3"])
        assert len(game.side_pots) == 1
        assert game.side_pots[0].amount == 100
    
    def test_create_multiple_side_pots(self):
        """Test creating multiple side pots."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.create_side_pot(100, ["bot_1", "bot_2"])
        game.create_side_pot(200, ["bot_2", "bot_3"])
        assert len(game.side_pots) == 2
    
    def test_get_total_pot_main_only(self):
        """Test total pot with main pot only."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(100)
        assert game.get_total_pot() == 100
    
    def test_get_total_pot_with_side_pots(self):
        """Test total pot with main and side pots."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(100)
        game.create_side_pot(50, ["bot_1", "bot_2"])
        game.create_side_pot(75, ["bot_2", "bot_3"])
        assert game.get_total_pot() == 225


class TestGameStatePhaseManagement:
    """Tests for phase management."""
    
    def test_advance_phase_valid(self):
        """Test advancing to a valid phase."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        game.advance_phase(GamePhase.BLINDS_POSTED)
        assert game.current_phase == GamePhase.BLINDS_POSTED
    
    def test_advance_phase_sequence(self):
        """Test advancing through phase sequence."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        phases = [
            GamePhase.BLINDS_POSTED,
            GamePhase.PRE_FLOP,
            GamePhase.FLOP,
            GamePhase.SHOWDOWN,
        ]
        for phase in phases:
            game.advance_phase(phase)
            assert game.current_phase == phase
    
    def test_advance_phase_invalid(self):
        """Test that invalid phase raises ValueError."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        with pytest.raises(ValueError, match="Invalid phase"):
            game.advance_phase("INVALID_PHASE")


class TestGameStateCommunityCards:
    """Tests for community card management."""
    
    def test_reveal_community_card_first(self):
        """Test revealing the first community card."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        card = Card("hearts", "A")
        game.reveal_community_card(card)
        assert len(game.community_cards) == 1
        assert game.community_cards[0] == card
    
    def test_reveal_community_cards_all_five(self):
        """Test revealing all 5 community cards."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        cards = [
            Card("hearts", "A"),
            Card("spades", "K"),
            Card("diamonds", "Q"),
            Card("clubs", "J"),
            Card("hearts", "10"),
        ]
        for card in cards:
            game.reveal_community_card(card)
        assert len(game.community_cards) == 5
    
    def test_reveal_community_card_too_many(self):
        """Test that revealing > 5 cards raises ValueError."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        for i in range(5):
            game.reveal_community_card(Card("hearts", "A"))
        with pytest.raises(ValueError, match="more than 5"):
            game.reveal_community_card(Card("spades", "K"))
    
    def test_reveal_community_card_invalid_type(self):
        """Test that revealing non-Card raises ValueError."""
        players = [PlayerState("bot_1", 0, 1000), PlayerState("bot_2", 1, 1000)]
        game = GameState("game_1", players, 10, 20)
        with pytest.raises(ValueError, match="Expected Card"):
            game.reveal_community_card("A")


class TestGameStatePlayerQueries:
    """Tests for player query methods."""
    
    def test_get_active_players_all_active(self):
        """Test getting active players when all are active."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        active = game.get_active_players()
        assert len(active) == 2
    
    def test_get_active_players_some_folded(self):
        """Test getting active players when some have folded."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
            PlayerState("bot_3", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.players[1].status = PlayerStatus.FOLDED
        active = game.get_active_players()
        assert len(active) == 2
        assert players[1] not in active
    
    def test_get_active_players_with_all_in(self):
        """Test that ALL_IN players are included in active."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.players[1].status = PlayerStatus.ALL_IN
        active = game.get_active_players()
        assert len(active) == 2
    
    def test_get_player_by_id_found(self):
        """Test getting player by ID when found."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        player = game.get_player_by_id("bot_1")
        assert player is not None
        assert player.player_id == "bot_1"
    
    def test_get_player_by_id_not_found(self):
        """Test getting player by ID when not found."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        player = game.get_player_by_id("bot_999")
        assert player is None
    
    def test_get_player_by_seat_found(self):
        """Test getting player by seat when found."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        player = game.get_player_by_seat(0)
        assert player is not None
        assert player.player_id == "bot_1"
    
    def test_get_player_by_seat_out_of_range(self):
        """Test getting player by seat when out of range."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        player = game.get_player_by_seat(10)
        assert player is None
    
    def test_get_next_active_seat_clockwise(self):
        """Test finding next active player clockwise."""
        players = [
            PlayerState("bot_0", 0, 1000),
            PlayerState("bot_1", 1, 1000),
            PlayerState("bot_2", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        next_seat = game.get_next_active_seat(0)
        assert next_seat == 1
    
    def test_get_next_active_seat_skip_folded(self):
        """Test that folded players are skipped."""
        players = [
            PlayerState("bot_0", 0, 1000),
            PlayerState("bot_1", 1, 1000),
            PlayerState("bot_2", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.players[1].status = PlayerStatus.FOLDED
        next_seat = game.get_next_active_seat(0)
        assert next_seat == 2
    
    def test_get_next_active_seat_wraps_around(self):
        """Test that seat numbering wraps around from 7 to 0."""
        players = [
            PlayerState(f"bot_{i}", i, 1000) for i in range(8)
        ]
        game = GameState("game_1", players, 10, 20)
        next_seat = game.get_next_active_seat(7)
        assert next_seat == 0
    
    def test_get_next_active_seat_no_active_players(self):
        """Test finding next seat when no players active."""
        players = [
            PlayerState("bot_0", 0, 1000),
            PlayerState("bot_1", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.players[0].status = PlayerStatus.FOLDED
        game.players[1].status = PlayerStatus.FOLDED
        next_seat = game.get_next_active_seat(0)
        assert next_seat is None


class TestGameStateReset:
    """Tests for hand reset functionality."""
    
    def test_reset_for_new_hand(self):
        """Test resetting game for new hand."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(100)
        game.create_side_pot(50, ["bot_1"])
        game.reveal_community_card(Card("hearts", "A"))
        game.current_phase = GamePhase.RIVER
        game.players[0].post_bet(50)
        game.players[1].status = PlayerStatus.FOLDED
        
        game.reset_for_new_hand()
        
        assert game.main_pot == 0
        assert game.side_pots == []
        assert game.community_cards == []
        assert game.current_phase == GamePhase.BLINDS_POSTED
        assert game.players[0].current_bet == 0
        assert game.players[1].status == PlayerStatus.ACTIVE
        assert game.dealer_button == 1
    
    def test_reset_for_new_hand_button_rotation(self):
        """Test that dealer button rotates correctly."""
        players = [
            PlayerState("bot_0", 0, 1000),
            PlayerState("bot_1", 1, 1000),
            PlayerState("bot_2", 2, 1000),
        ]
        game = GameState("game_1", players, 10, 20, dealer_button=0)
        game.reset_for_new_hand()
        assert game.dealer_button == 1
        game.reset_for_new_hand()
        assert game.dealer_button == 2
        game.reset_for_new_hand()
        assert game.dealer_button == 0


class TestGameStateRepr:
    """Tests for string representation."""
    
    def test_repr(self):
        """Test that __repr__ returns a valid string."""
        players = [
            PlayerState("bot_1", 0, 1000),
            PlayerState("bot_2", 1, 1000),
        ]
        game = GameState("game_1", players, 10, 20)
        game.add_to_main_pot(50)
        repr_str = repr(game)
        assert "game_1" in repr_str
        assert "WAITING_FOR_PLAYERS" in repr_str
        assert "2" in repr_str
        assert "50" in repr_str
