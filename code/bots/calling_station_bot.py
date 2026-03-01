"""Calling Station bot - always calls, never folds or raises."""

from typing import Tuple
from .base_bot import BaseBot

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poker_engine import ActionType


class CallingStationBot(BaseBot):
    """
    Calls any bet regardless of size. Checks when no bet to call.
    Never folds, never raises. Forces multi-way pots to showdown
    and exercises hand evaluation on every hand played.
    """

    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        to_call = snapshot.get('current_bet_to_call', 0)
        stack = snapshot.get('your_stack', 0)

        if to_call <= 0:
            return (ActionType.CHECK, 0)

        if to_call >= stack:
            return (ActionType.ALL_IN, stack)

        return (ActionType.CALL, to_call)
