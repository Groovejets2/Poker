"""Abstract base class for all poker bot strategies."""

from abc import ABC, abstractmethod
from typing import Tuple

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from poker_engine import ActionType


class BaseBot(ABC):
    """
    Abstract base class for all bot strategies.

    Subclasses must implement get_action(), which receives a game state
    snapshot and returns an (ActionType, amount) tuple.
    """

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        """
        Decide on a poker action given the current game state.

        Args:
            snapshot: Game state dict from DealerEngine.request_action().
                      Keys: player_id, game_phase, your_cards, your_stack,
                      your_bet_this_round, community_cards,
                      current_bet_to_call, pot_total, active_players.

        Returns:
            Tuple of (ActionType, amount).
            amount is 0 for CHECK, FOLD, CALL.
            amount is the bet size for BET.
            amount is the raise increment for RAISE.
            amount is the remaining stack for ALL_IN.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
