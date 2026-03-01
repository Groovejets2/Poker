"""Passive bot - checks or calls small bets, folds large bets."""

from typing import Tuple
from .base_bot import BaseBot

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poker_engine import ActionType

# Fold if the bet to call exceeds this fraction of the remaining stack
FOLD_THRESHOLD = 0.30


class PassiveBot(BaseBot):
    """
    Always checks when possible. Calls bets up to 30% of remaining stack.
    Folds when facing larger bets. Never raises or bets.
    Tests check-through rounds and uncontested pots where no one drives
    the action.
    """

    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        to_call = snapshot.get('current_bet_to_call', 0)
        stack = snapshot.get('your_stack', 0)

        if to_call <= 0:
            return (ActionType.CHECK, 0)

        if stack > 0 and (to_call / stack) > FOLD_THRESHOLD:
            return (ActionType.FOLD, 0)

        if to_call >= stack:
            return (ActionType.ALL_IN, stack)

        return (ActionType.CALL, to_call)
