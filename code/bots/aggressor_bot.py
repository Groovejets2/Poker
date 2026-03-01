"""Aggressor bot - bets and raises on every opportunity."""

from typing import Tuple
from .base_bot import BaseBot

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poker_engine import ActionType

BET_AMOUNT = 40    # 2x big blind opening bet
RAISE_INCREMENT = 20   # minimum raise increment (= big blind)


class AggressorBot(BaseBot):
    """
    Bets when no one has bet. Raises when facing a bet.
    Goes all-in when stack is too small for a full raise.
    Tests RAISE action sequencing, re-raise logic, and
    pot-building across all betting rounds.
    """

    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        to_call = snapshot.get('current_bet_to_call', 0)
        stack = snapshot.get('your_stack', 0)
        my_bet = snapshot.get('your_bet_this_round', 0)

        if stack <= 0:
            return (ActionType.FOLD, 0)

        if to_call > 0:
            # Facing a bet or raise.
            # RAISE amount = chips to add on top of current_bet.
            # Validator: player.current_bet + amount >= max_bet + min_raise
            # Since to_call = max_bet - player.current_bet:
            #   amount >= to_call + RAISE_INCREMENT
            raise_amount = to_call + RAISE_INCREMENT
            if raise_amount >= stack:
                return (ActionType.ALL_IN, stack)
            return (ActionType.RAISE, raise_amount)
        elif my_bet > 0:
            # to_call == 0 but we already have chips in (e.g., BB option pre-flop).
            # BET is invalid here (max_bet > 0); use RAISE instead.
            raise_amount = min(BET_AMOUNT, stack)
            if raise_amount <= 0:
                return (ActionType.CHECK, 0)
            if raise_amount >= stack:
                return (ActionType.ALL_IN, stack)
            return (ActionType.RAISE, raise_amount)
        else:
            # No bet in the round at all - open with a BET.
            bet = min(BET_AMOUNT, stack)
            if bet <= 0:
                return (ActionType.CHECK, 0)
            return (ActionType.BET, bet)
