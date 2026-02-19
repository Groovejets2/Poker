"""Unit tests for the dealer engine PlayerState and GameState classes."""

import pytest
from poker_engine.dealer_engine import (
    PlayerState,
    GameState,
    PlayerStatus,
    GamePhase
)


class TestPlayerState:
    """Test suite for PlayerState class."""
    
    def test_player_state_initialisation(self) -> None:
        """Test PlayerState initialisation with valid parameters."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        
        assert player.player_id == 1
        assert player.starting_stack == 1000
        assert player.current_stack == 1000
        assert player.current_bet == 0
        assert player.total_contributed == 0
        assert player.status == PlayerStatus.ACTIVE
        assert player.position == 0
    
    def test_player_state_invalid_stack(self) -> None:
        """Test PlayerState raises error with negative starting stack."""
        with pytest.raises(ValueError, match="Starting stack cannot be negative"):
            PlayerState(player_id=1, starting_stack=-100, position=0)
    
    def test_player_state_invalid_player_id(self) -> None:
        """Test PlayerState raises error with negative player ID."""
        with pytest.raises(ValueError, match="Player ID cannot be negative"):
            PlayerState(player_id=-1, starting_stack=1000, position=0)
    
    def test_place_bet_valid(self) -> None:
        """Test placing a valid bet deducts from stack and updates current_bet."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        player.place_bet(100)
        
        assert player.current_stack == 900
        assert player.current_bet == 100
        assert player.total_contributed == 100
    
    def test_place_bet_multiple(self) -> None:
        """Test placing multiple bets accumulates correctly."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        player.place_bet(50)
        player.place_bet(50)
        
        assert player.current_stack == 900
        assert player.current_bet == 100
        assert player.total_contributed == 100
    
    def test_place_bet_exceeds_stack(self) -> None:
        """Test placing a bet that exceeds stack raises error."""
        player = PlayerState(player_id=1, starting_stack=100, position=0)
        
        with pytest.raises(ValueError, match="Insufficient chips"):
            player.place_bet(150)
    
    def test_place_bet_negative(self) -> None:
        """Test placing a negative bet raises error."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        
        with pytest.raises(ValueError, match="Bet amount cannot be negative"):
            player.place_bet(-50)
    
    def test_reset_round_bet(self) -> None:
        """Test resetting round bet without affecting total_contributed."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        player.place_bet(100)
        player.reset_round_bet()
        
        assert player.current_bet == 0
        assert player.total_contributed == 100
        assert player.current_stack == 900
    
    def test_fold_status(self) -> None:
        """Test folding changes player status."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        player.fold()
        
        assert player.status == PlayerStatus.FOLDED
        assert not player.is_active()
    
    def test_all_in_status(self) -> None:
        """Test all-in bets remaining stack and changes status."""
        player = PlayerState(player_id=1, starting_stack=100, position=0)
        player.set_all_in()
        
        assert player.status == PlayerStatus.ALL_IN
        assert player.current_stack == 0
        assert player.current_bet == 100
    
    def test_get_remaining_stack(self) -> None:
        """Test getting remaining stack after bets."""
        player = PlayerState(player_id=1, starting_stack=1000, position=0)
        player.place_bet(250)
        
        assert player.get_remaining_stack() == 750


class TestGameState:
    """Test suite for GameState class."""
    
    def test_game_state_initialisation(self) -> None:
        """Test GameState initialisation with valid players."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players, min_bet=2)
        
        assert len(game.players) == 2
        assert game.pot == 0
        assert game.current_phase == GamePhase.PRE_FLOP
        assert game.current_bet_to_call == 2
        assert game.min_bet == 2
    
    def test_game_state_insufficient_players(self) -> None:
        """Test GameState raises error with only one player."""
        players = [PlayerState(player_id=1, starting_stack=1000, position=0)]
        
        with pytest.raises(ValueError, match="Game requires at least 2 players"):
            GameState(players=players)
    
    def test_game_state_invalid_min_bet(self) -> None:
        """Test GameState raises error with invalid min_bet."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        
        with pytest.raises(ValueError, match="Minimum bet must be positive"):
            GameState(players=players, min_bet=0)
    
    def test_add_to_pot(self) -> None:
        """Test adding chips to the pot."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        game.add_to_pot(100)
        
        assert game.pot == 100
    
    def test_add_to_pot_negative(self) -> None:
        """Test adding negative amount to pot raises error."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        
        with pytest.raises(ValueError, match="Pot amount cannot be negative"):
            game.add_to_pot(-50)
    
    def test_get_total_pot_main_only(self) -> None:
        """Test calculating total pot with only main pot."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        game.add_to_pot(150)
        
        assert game.get_total_pot() == 150
    
    def test_get_total_pot_with_side_pots(self) -> None:
        """Test calculating total pot with main and side pots."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        game.add_to_pot(100)
        game.create_side_pot(50)
        game.create_side_pot(25)
        
        assert game.get_total_pot() == 175
    
    def test_move_to_next_phase(self) -> None:
        """Test advancing through game phases."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        
        assert game.current_phase == GamePhase.PRE_FLOP
        
        game.move_to_next_phase()
        assert game.current_phase == GamePhase.FLOP
        
        game.move_to_next_phase()
        assert game.current_phase == GamePhase.TURN
        
        game.move_to_next_phase()
        assert game.current_phase == GamePhase.RIVER
        
        game.move_to_next_phase()
        assert game.current_phase == GamePhase.SHOWDOWN
    
    def test_get_active_players(self) -> None:
        """Test retrieving active players (not folded)."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1),
            PlayerState(player_id=3, starting_stack=1000, position=2)
        ]
        game = GameState(players=players)
        
        players[1].fold()
        
        active = game.get_active_players()
        assert len(active) == 2
        assert players[0] in active
        assert players[2] in active
    
    def test_get_active_action_players(self) -> None:
        """Test retrieving players who can take action."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1),
            PlayerState(player_id=3, starting_stack=1000, position=2)
        ]
        game = GameState(players=players)
        
        players[1].fold()
        players[2].set_all_in()
        
        action_players = game.get_active_action_players()
        assert len(action_players) == 1
        assert action_players[0] == players[0]
    
    def test_get_player_by_id(self) -> None:
        """Test retrieving a player by ID."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        
        player = game.get_player_by_id(1)
        assert player is not None
        assert player.player_id == 1
    
    def test_get_player_by_id_not_found(self) -> None:
        """Test retrieving a non-existent player returns None."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        
        player = game.get_player_by_id(999)
        assert player is None
    
    def test_create_side_pot(self) -> None:
        """Test creating a side pot."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players)
        
        game.create_side_pot(100)
        assert game.side_pots == [100]
        
        game.create_side_pot(50)
        assert game.side_pots == [100, 50]
    
    def test_get_game_summary(self) -> None:
        """Test generating a game state summary."""
        players = [
            PlayerState(player_id=1, starting_stack=1000, position=0),
            PlayerState(player_id=2, starting_stack=1000, position=1)
        ]
        game = GameState(players=players, min_bet=5)
        game.add_to_pot(100)
        
        summary = game.get_game_summary()
        
        assert summary["pot"] == 100
        assert summary["total_pot"] == 100
        assert summary["phase"] == "pre_flop"
        assert summary["active_players"] == 2
        assert summary["min_bet"] == 5
        assert summary["current_bet_to_call"] == 5
