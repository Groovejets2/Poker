"""Comprehensive tests for PotManager class."""

import pytest
from poker_engine.pot_manager import PotManager, Pot


class TestPotInitialisation:
    """Test Pot object creation."""
    
    def test_create_valid_pot(self):
        """Test creating a valid pot."""
        pot = Pot(100, ["player1", "player2"])
        assert pot.amount == 100
        assert "player1" in pot.eligible_players
        assert "player2" in pot.eligible_players
    
    def test_pot_copies_player_list(self):
        """Test that Pot copies player list (not reference)."""
        players = ["player1", "player2"]
        pot = Pot(100, players)
        
        players.append("player3")
        assert "player3" not in pot.eligible_players
    
    def test_pot_zero_amount_allowed(self):
        """Test that zero pot amount is allowed."""
        pot = Pot(0, ["player1"])
        assert pot.amount == 0
    
    def test_pot_negative_amount_raises_error(self):
        """Test that negative pot amount raises ValueError."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Pot(-50, ["player1"])
    
    def test_pot_empty_players_raises_error(self):
        """Test that empty player list raises ValueError."""
        with pytest.raises(ValueError, match="at least one eligible"):
            Pot(100, [])
    
    def test_pot_single_player(self):
        """Test pot with single eligible player."""
        pot = Pot(100, ["player1"])
        assert len(pot.eligible_players) == 1
    
    def test_pot_multiple_players(self):
        """Test pot with multiple eligible players."""
        pot = Pot(100, ["p1", "p2", "p3", "p4"])
        assert len(pot.eligible_players) == 4


class TestPotAddChips:
    """Test adding chips to pots."""
    
    def test_add_positive_chips(self):
        """Test adding positive chips to pot."""
        pot = Pot(100, ["player1"])
        pot.add(50)
        assert pot.amount == 150
    
    def test_add_zero_chips(self):
        """Test adding zero chips (should be allowed)."""
        pot = Pot(100, ["player1"])
        pot.add(0)
        assert pot.amount == 100
    
    def test_add_negative_chips_raises_error(self):
        """Test that adding negative chips raises ValueError."""
        pot = Pot(100, ["player1"])
        with pytest.raises(ValueError, match="Cannot add negative"):
            pot.add(-50)
    
    def test_add_multiple_times(self):
        """Test adding chips multiple times."""
        pot = Pot(0, ["player1"])
        pot.add(50)
        pot.add(100)
        pot.add(75)
        assert pot.amount == 225


class TestPotRepr:
    """Test string representation of Pot."""
    
    def test_pot_repr_contains_amount(self):
        """Test that repr contains pot amount."""
        pot = Pot(500, ["player1"])
        repr_str = repr(pot)
        assert "500" in repr_str
    
    def test_pot_repr_contains_player_count(self):
        """Test that repr contains eligible player count."""
        pot = Pot(100, ["p1", "p2", "p3"])
        repr_str = repr(pot)
        assert "3" in repr_str


class TestPotManagerInitialisation:
    """Test PotManager creation."""
    
    def test_create_valid_pot_manager(self):
        """Test creating a valid pot manager."""
        pm = PotManager(["player1", "player2"])
        assert pm.main_pot.amount == 0
        assert len(pm.side_pots) == 0
        assert pm.player_contributions["player1"] == 0
        assert pm.player_contributions["player2"] == 0
    
    def test_pot_manager_with_multiple_players(self):
        """Test pot manager with multiple players."""
        players = ["p1", "p2", "p3", "p4"]
        pm = PotManager(players)
        for player in players:
            assert player in pm.player_contributions
    
    def test_pot_manager_empty_players_raises_error(self):
        """Test that empty player list raises ValueError."""
        with pytest.raises(ValueError, match="at least one active"):
            PotManager([])
    
    def test_main_pot_eligibility(self):
        """Test that main pot includes all initial players."""
        players = ["p1", "p2", "p3"]
        pm = PotManager(players)
        for player in players:
            assert player in pm.main_pot.eligible_players


class TestPotManagerContributions:
    """Test tracking player contributions."""
    
    def test_add_to_pot_simple(self):
        """Test adding chips from a player."""
        pm = PotManager(["player1", "player2"])
        
        pm.add_to_pot("player1", 100)
        assert pm.player_contributions["player1"] == 100
        assert pm.main_pot.amount == 100
    
    def test_add_to_pot_multiple_players(self):
        """Test multiple players adding chips."""
        pm = PotManager(["p1", "p2", "p3"])
        
        pm.add_to_pot("p1", 100)
        pm.add_to_pot("p2", 150)
        pm.add_to_pot("p3", 75)
        
        assert pm.player_contributions["p1"] == 100
        assert pm.player_contributions["p2"] == 150
        assert pm.player_contributions["p3"] == 75
        assert pm.main_pot.amount == 325
    
    def test_add_zero_chips(self):
        """Test adding zero chips is allowed."""
        pm = PotManager(["player1"])
        pm.add_to_pot("player1", 0)
        assert pm.player_contributions["player1"] == 0
    
    def test_add_negative_chips_raises_error(self):
        """Test adding negative chips raises ValueError."""
        pm = PotManager(["player1"])
        with pytest.raises(ValueError, match="Cannot add negative"):
            pm.add_to_pot("player1", -50)
    
    def test_add_for_non_existent_player_raises_error(self):
        """Test adding for non-existent player raises ValueError."""
        pm = PotManager(["player1"])
        with pytest.raises(ValueError, match="not in this game"):
            pm.add_to_pot("player2", 100)
    
    def test_multiple_contributions_from_same_player(self):
        """Test player contributing multiple times (betting rounds)."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 50)
        assert pm.player_contributions["p1"] == 50
        
        pm.add_to_pot("p1", 100)
        assert pm.player_contributions["p1"] == 150
        
        assert pm.main_pot.amount == 150


class TestPotManagerAllIn:
    """Test all-in tracking."""
    
    def test_set_all_in_single_player(self):
        """Test marking a player as all-in."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 100)
        pm.set_all_in("p1", 0)
        
        assert "p1" in pm.all_in_amounts
        assert pm.all_in_amounts["p1"] == 100
    
    def test_set_all_in_non_existent_player_raises_error(self):
        """Test setting all-in for non-existent player raises error."""
        pm = PotManager(["p1"])
        with pytest.raises(ValueError, match="not in this game"):
            pm.set_all_in("p2", 0)
    
    def test_multiple_all_ins(self):
        """Test multiple players going all-in."""
        pm = PotManager(["p1", "p2", "p3"])
        
        pm.add_to_pot("p1", 50)
        pm.set_all_in("p1", 0)
        
        pm.add_to_pot("p2", 100)
        pm.set_all_in("p2", 0)
        
        assert len(pm.all_in_amounts) == 2
        assert pm.all_in_amounts["p1"] == 50
        assert pm.all_in_amounts["p2"] == 100


class TestSidePotCalculation:
    """Test side pot calculation."""
    
    def test_no_side_pots_when_no_all_ins(self):
        """Test that no side pots are created with no all-ins."""
        pm = PotManager(["p1", "p2", "p3"])
        
        pm.add_to_pot("p1", 100)
        pm.add_to_pot("p2", 100)
        pm.add_to_pot("p3", 100)
        
        pm.calculate_side_pots()
        
        assert len(pm.side_pots) == 0
        assert pm.main_pot.amount == 300
    
    def test_side_pots_with_one_all_in(self):
        """Test side pot creation with one all-in player."""
        pm = PotManager(["p1", "p2"])
        
        # p1 goes all-in with 50
        pm.add_to_pot("p1", 50)
        pm.set_all_in("p1", 0)
        
        # p2 contributes 150 total
        pm.add_to_pot("p2", 150)
        
        initial_total = pm.main_pot.amount
        pm.calculate_side_pots()
        
        # Should have created side pots when all-in amounts differ
        # Main pot + side pots should track the contributions
        assert "p1" in pm.all_in_amounts
    
    def test_side_pots_with_two_all_ins_different_amounts(self):
        """Test side pots with two all-in players at different amounts."""
        pm = PotManager(["p1", "p2", "p3"])
        
        # p1 goes all-in with 50
        pm.add_to_pot("p1", 50)
        pm.set_all_in("p1", 0)
        
        # p2 goes all-in with 100
        pm.add_to_pot("p2", 100)
        pm.set_all_in("p2", 0)
        
        # p3 contributes 200
        pm.add_to_pot("p3", 200)
        
        pm.calculate_side_pots()
        
        # Should track multiple all-ins
        assert len(pm.all_in_amounts) == 2
        assert pm.all_in_amounts["p1"] == 50
        assert pm.all_in_amounts["p2"] == 100
    
    def test_side_pots_with_three_all_ins(self):
        """Test side pots with three all-in players."""
        pm = PotManager(["p1", "p2", "p3", "p4"])
        
        pm.add_to_pot("p1", 50)
        pm.set_all_in("p1", 0)
        
        pm.add_to_pot("p2", 100)
        pm.set_all_in("p2", 0)
        
        pm.add_to_pot("p3", 200)
        pm.set_all_in("p3", 0)
        
        pm.add_to_pot("p4", 400)
        
        pm.calculate_side_pots()
        
        # Should track three all-ins
        assert len(pm.all_in_amounts) == 3
        assert len(pm.side_pots) >= 1


class TestPotManagerPotQueries:
    """Test querying pot information."""
    
    def test_get_pot_total(self):
        """Test calculating total pot."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 100)
        pm.add_to_pot("p2", 150)
        
        assert pm.get_pot_total() == 250
    
    def test_get_main_pot(self):
        """Test getting main pot amount."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 100)
        pm.add_to_pot("p2", 100)
        
        assert pm.get_main_pot() == 200
    
    def test_get_side_pots(self):
        """Test getting side pots info."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 50)
        pm.set_all_in("p1", 0)
        pm.add_to_pot("p2", 150)
        
        pm.calculate_side_pots()
        
        side_pots = pm.get_side_pots()
        assert len(side_pots) >= 1
        assert all("amount" in sp for sp in side_pots)
        assert all("eligible_players" in sp for sp in side_pots)
    
    def test_get_all_pots(self):
        """Test getting complete pot structure."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 100)
        pm.add_to_pot("p2", 150)
        
        all_pots = pm.get_all_pots()
        assert "main_pot" in all_pots
        assert "side_pots" in all_pots
        assert "total" in all_pots
        assert all_pots["total"] == 250
    
    def test_get_player_contribution(self):
        """Test getting single player's contribution."""
        pm = PotManager(["p1", "p2", "p3"])
        
        pm.add_to_pot("p1", 100)
        pm.add_to_pot("p2", 250)
        pm.add_to_pot("p3", 150)
        
        assert pm.get_player_contribution("p1") == 100
        assert pm.get_player_contribution("p2") == 250
        assert pm.get_player_contribution("p3") == 150
    
    def test_get_player_contribution_non_existent_player(self):
        """Test getting contribution for non-existent player."""
        pm = PotManager(["p1"])
        with pytest.raises(ValueError, match="not in this game"):
            pm.get_player_contribution("p2")


class TestPotManagerRepr:
    """Test string representation."""
    
    def test_repr_contains_main_pot(self):
        """Test that repr contains main pot amount."""
        pm = PotManager(["p1"])
        pm.add_to_pot("p1", 500)
        repr_str = repr(pm)
        assert "500" in repr_str
    
    def test_repr_contains_side_pot_count(self):
        """Test that repr contains side pot count."""
        pm = PotManager(["p1", "p2"])
        repr_str = repr(pm)
        assert "side_pots" in repr_str


class TestPotManagerEdgeCases:
    """Test edge cases and complex scenarios."""
    
    def test_large_pot_amounts(self):
        """Test with very large pot amounts."""
        pm = PotManager(["p1", "p2"])
        
        pm.add_to_pot("p1", 1_000_000)
        pm.add_to_pot("p2", 1_000_000)
        
        assert pm.get_pot_total() == 2_000_000
    
    def test_many_players(self):
        """Test with maximum number of players."""
        players = [f"p{i}" for i in range(8)]
        pm = PotManager(players)
        
        for i, player in enumerate(players):
            pm.add_to_pot(player, (i + 1) * 100)
        
        # Total: 100 + 200 + 300 + 400 + 500 + 600 + 700 + 800 = 3600
        assert pm.get_pot_total() == 3600
    
    def test_all_players_all_in(self):
        """Test scenario where all players go all-in."""
        pm = PotManager(["p1", "p2", "p3"])
        
        pm.add_to_pot("p1", 100)
        pm.set_all_in("p1", 0)
        
        pm.add_to_pot("p2", 200)
        pm.set_all_in("p2", 0)
        
        pm.add_to_pot("p3", 300)
        pm.set_all_in("p3", 0)
        
        pm.calculate_side_pots()
        
        # All players should be marked as all-in
        assert len(pm.all_in_amounts) == 3
    
    def test_chip_distribution_after_all_ins(self):
        """Test that chip amounts are preserved through all-in calculations."""
        pm = PotManager(["p1", "p2", "p3"])
        
        pm.add_to_pot("p1", 100)
        pm.set_all_in("p1", 0)
        
        pm.add_to_pot("p2", 200)
        
        pm.add_to_pot("p3", 300)
        
        pm.calculate_side_pots()
        
        # p1 should be marked all-in
        assert "p1" in pm.all_in_amounts
        assert pm.get_player_contribution("p1") == 100
        assert pm.get_player_contribution("p2") == 200
        assert pm.get_player_contribution("p3") == 300


class TestComplexScenarios:
    """Test complex real-world scenarios."""
    
    def test_three_way_pot_with_varying_all_ins(self):
        """Test realistic three-player scenario."""
        pm = PotManager(["alice", "bob", "charlie"])
        
        # Pre-flop
        pm.add_to_pot("alice", 50)
        pm.add_to_pot("bob", 100)
        pm.add_to_pot("charlie", 100)
        
        # Turn (alice goes all-in for 30 more)
        pm.add_to_pot("alice", 30)
        pm.set_all_in("alice", 0)
        
        # River (bob goes all-in for 200 more)
        pm.add_to_pot("bob", 200)
        pm.set_all_in("bob", 0)
        
        # Charlie calls all-in for 250
        pm.add_to_pot("charlie", 250)
        pm.set_all_in("charlie", 0)
        
        pm.calculate_side_pots()
        
        # All three should be marked all-in
        assert len(pm.all_in_amounts) == 3
        # Contributions should be tracked
        assert pm.get_player_contribution("alice") == 80
        assert pm.get_player_contribution("bob") == 300
        assert pm.get_player_contribution("charlie") == 350
    
    def test_uneven_contributions_heads_up(self):
        """Test heads-up game with uneven stacks."""
        pm = PotManager(["short_stack", "big_stack"])
        
        # Short stack goes all-in for 50
        pm.add_to_pot("short_stack", 50)
        pm.set_all_in("short_stack", 0)
        
        # Big stack calls and raises to 500
        pm.add_to_pot("big_stack", 500)
        
        pm.calculate_side_pots()
        
        # Should have marked short stack as all-in
        assert "short_stack" in pm.all_in_amounts
        # Contributions should be tracked
        assert pm.get_player_contribution("short_stack") == 50
        assert pm.get_player_contribution("big_stack") == 500
