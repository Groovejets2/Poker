"""Statistics tracking for clinical test sessions."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class HandResult:
    """Result of a single hand."""
    hand_number: int
    winners: Dict[str, int]       # player_id -> chips won
    pot_total: int
    players_folded: int
    went_to_showdown: bool
    invariant_violations: List[str]


@dataclass
class SessionStatistics:
    """Aggregated statistics across a full test session."""
    bot_names: List[str]
    hands_played: int = 0
    hands_went_to_showdown: int = 0
    total_pots: int = 0
    largest_pot: int = 0
    invariant_violations: int = 0
    wins: Dict[str, int] = field(default_factory=dict)
    chips_won: Dict[str, int] = field(default_factory=dict)
    hand_results: List[HandResult] = field(default_factory=list)

    def __post_init__(self) -> None:
        for name in self.bot_names:
            self.wins.setdefault(name, 0)
            self.chips_won.setdefault(name, 0)

    def record_hand(self, result: HandResult) -> None:
        """Update statistics with the result of one hand."""
        self.hands_played += 1
        self.total_pots += result.pot_total
        self.largest_pot = max(self.largest_pot, result.pot_total)
        self.invariant_violations += len(result.invariant_violations)

        if result.went_to_showdown:
            self.hands_went_to_showdown += 1

        for player_id, chips in result.winners.items():
            if chips > 0:
                self.wins[player_id] = self.wins.get(player_id, 0) + 1
                self.chips_won[player_id] = self.chips_won.get(player_id, 0) + chips

        self.hand_results.append(result)

    def summary(self) -> dict:
        """Return a summary dict for logging and reporting."""
        avg_pot = self.total_pots / self.hands_played if self.hands_played > 0 else 0
        showdown_pct = (
            (self.hands_went_to_showdown / self.hands_played * 100)
            if self.hands_played > 0 else 0
        )
        return {
            'hands_played': self.hands_played,
            'hands_to_showdown': self.hands_went_to_showdown,
            'showdown_rate': f"{showdown_pct:.1f}%",
            'average_pot': round(avg_pot, 1),
            'largest_pot': self.largest_pot,
            'invariant_violations': self.invariant_violations,
            'wins_per_player': dict(
                sorted(self.wins.items(), key=lambda x: x[1], reverse=True)
            ),
            'chips_won_per_player': dict(
                sorted(self.chips_won.items(), key=lambda x: x[1], reverse=True)
            ),
        }
