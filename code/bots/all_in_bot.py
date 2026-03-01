"""All-In bot - goes all-in on every action."""

from typing import Tuple
from .base_bot import BaseBot

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poker_engine import ActionType


class AllInBot(BaseBot):
    """
    Goes all-in on every decision. Exercises side pot creation,
    multi-player all-in resolution, and stack elimination logic
    across all possible stack-size combinations.
    """

    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        stack = snapshot.get('your_stack', 0)

        if stack <= 0:
            # Stack already committed - check or fold depending on state
            to_call = snapshot.get('current_bet_to_call', 0)
            return (ActionType.CHECK, 0) if to_call == 0 else (ActionType.FOLD, 0)

        return (ActionType.ALL_IN, stack)
