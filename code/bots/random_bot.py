"""Random bot - chooses a random valid action each turn."""

import random
from typing import Tuple
from .base_bot import BaseBot

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poker_engine import ActionType

BET_AMOUNT = 40  # Fixed bet size when choosing to bet


class RandomBot(BaseBot):
    """
    Picks a random legal action on every decision point.
    Produces unusual game states not covered by strategy-based bots.
    Exercises rare action sequences such as multiple re-raises,
    check-raise scenarios, and back-to-back all-ins.
    """

    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        to_call = snapshot.get('current_bet_to_call', 0)
        stack = snapshot.get('your_stack', 0)

        if stack <= 0:
            return (ActionType.FOLD, 0)

        if to_call <= 0:
            # No bet to face: check, bet, or go all-in
            choice = random.randint(0, 2)
            if choice == 0:
                return (ActionType.CHECK, 0)
            elif choice == 1:
                bet = min(BET_AMOUNT, stack)
                return (ActionType.BET, bet) if bet > 0 else (ActionType.CHECK, 0)
            else:
                return (ActionType.ALL_IN, stack)
        else:
            # Facing a bet: fold, call, or go all-in
            choice = random.randint(0, 2)
            if choice == 0:
                return (ActionType.FOLD, 0)
            elif choice == 1:
                if to_call >= stack:
                    return (ActionType.ALL_IN, stack)
                return (ActionType.CALL, to_call)
            else:
                return (ActionType.ALL_IN, stack)
