"""Folder bot - folds all but premium hands (A, K, Q in hole cards)."""

from typing import Tuple
from .base_bot import BaseBot

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from poker_engine import ActionType

# Ranks considered premium enough to play
PREMIUM_RANKS = {'A', 'K', 'Q'}


class FolderBot(BaseBot):
    """
    Folds unless at least one hole card is an Ace, King, or Queen.
    When holding a premium card, calls or checks - never raises.
    Tests short-stack and blind-stealing edge cases by folding frequently.

    Card strings from the engine snapshot are in "rank of suit" format,
    e.g. "A of hearts", "10 of clubs".
    """

    def get_action(self, snapshot: dict) -> Tuple[ActionType, int]:
        cards = snapshot.get('your_cards', [])
        to_call = snapshot.get('current_bet_to_call', 0)
        stack = snapshot.get('your_stack', 0)

        # Parse rank from "A of hearts" -> "A"
        ranks = {card.split(' of ')[0] for card in cards}
        has_premium = bool(ranks & PREMIUM_RANKS)

        if not has_premium:
            return (ActionType.FOLD, 0)

        if to_call <= 0:
            return (ActionType.CHECK, 0)

        if to_call >= stack:
            return (ActionType.ALL_IN, stack)

        return (ActionType.CALL, to_call)
