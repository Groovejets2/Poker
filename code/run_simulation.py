"""
Clinical testing entry point for the OpenClaw Poker simulator.

Runs five sessions that together exercise the full TEST-PLAN.md scenario list:
  Session 1 - Main session    : 500 hands, 6 mixed bots
  Session 2 - All-in stress   : 200 hands, 6 all-in bots (side pot logic)
  Session 3 - Random stress   : 500 hands, 6 random bots (chaos coverage)
  Session 4 - Survivor test   : persistent stacks, mixed bots, up to 2000 hands
  Session 5 - Heads-up        : 1000 hands, AggressorBot vs CallingStationBot

Each session writes a Markdown report to docs/tests/ and prints a pass/fail
summary to stdout.  Any invariant violation causes the overall run to exit 1.
"""

import sys
import os

# Ensure the code directory is on the path so all engine imports resolve.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bots.calling_station_bot import CallingStationBot
from bots.aggressor_bot import AggressorBot
from bots.passive_bot import PassiveBot
from bots.folder_bot import FolderBot
from bots.all_in_bot import AllInBot
from bots.random_bot import RandomBot
from simulator.game_runner import GameRunner, run_survivor_test
from simulator.logger import SimulationLogger


def main() -> int:
    """Run all clinical test sessions and return exit code (0 = all passed)."""
    total_violations = 0
    session_results = []

    # -------------------------------------------------------------------------
    # Session 1: Main 500-hand session with all six bot types
    # -------------------------------------------------------------------------
    bots_main = [
        CallingStationBot('CS'),
        AggressorBot('Agg'),
        PassiveBot('Pass'),
        FolderBot('Fold'),
        AllInBot('AllIn'),
        RandomBot('Random'),
    ]
    logger1 = SimulationLogger('Session 1 - Main Mixed')
    runner1 = GameRunner(bots_main, logger1)
    stats1 = runner1.run_session(500, 'session1-main-mixed', batch_size=100)
    viols1 = stats1.summary()['invariant_violations']
    total_violations += viols1
    session_results.append(('Session 1 - Main Mixed (500 hands)', viols1))

    # -------------------------------------------------------------------------
    # Session 2: All-in stress test - exercises side pot creation with equal
    # stacks all going all-in simultaneously.
    # -------------------------------------------------------------------------
    bots_allin = [AllInBot(f'AllIn{i}') for i in range(1, 7)]
    logger2 = SimulationLogger('Session 2 - All-In Stress')
    runner2 = GameRunner(bots_allin, logger2)
    stats2 = runner2.run_session(200, 'session2-allin-stress', batch_size=50)
    viols2 = stats2.summary()['invariant_violations']
    total_violations += viols2
    session_results.append(('Session 2 - All-In Stress (200 hands)', viols2))

    # -------------------------------------------------------------------------
    # Session 3: Random chaos - unusual action sequences not covered by
    # strategy-based bots (check-raises, re-raises, back-to-back all-ins).
    # -------------------------------------------------------------------------
    bots_random = [RandomBot(f'Rand{i}') for i in range(1, 7)]
    logger3 = SimulationLogger('Session 3 - Random Chaos')
    runner3 = GameRunner(bots_random, logger3)
    stats3 = runner3.run_session(500, 'session3-random-chaos', batch_size=100)
    viols3 = stats3.summary()['invariant_violations']
    total_violations += viols3
    session_results.append(('Session 3 - Random Chaos (500 hands)', viols3))

    # -------------------------------------------------------------------------
    # Session 4: Survivor test - persistent stacks, bots eliminated when
    # stack hits zero, ends when one player holds all chips.
    # -------------------------------------------------------------------------
    bots_survivor = [
        CallingStationBot('CS'),
        AggressorBot('Agg'),
        PassiveBot('Pass'),
        FolderBot('Fold'),
        AllInBot('AllIn'),
        RandomBot('Random'),
    ]
    logger4 = SimulationLogger('Session 4 - Survivor')
    stats4 = run_survivor_test(bots_survivor, logger4, max_hands=2000,
                               session_label='session4-survivor')
    viols4 = stats4.summary()['invariant_violations']
    total_violations += viols4
    session_results.append(('Session 4 - Survivor (up to 2000 hands)', viols4))

    # -------------------------------------------------------------------------
    # Session 5: Heads-up - isolates two specific strategies for 1000 hands.
    # -------------------------------------------------------------------------
    bots_hu = [
        AggressorBot('Agg'),
        CallingStationBot('CS'),
    ]
    logger5 = SimulationLogger('Session 5 - Heads-Up Agg vs CS')
    runner5 = GameRunner(bots_hu, logger5)
    stats5 = runner5.run_session(1000, 'session5-headsup-agg-vs-cs', batch_size=200)
    viols5 = stats5.summary()['invariant_violations']
    total_violations += viols5
    session_results.append(('Session 5 - Heads-Up Agg vs CS (1000 hands)', viols5))

    # -------------------------------------------------------------------------
    # Final summary
    # -------------------------------------------------------------------------
    print('\n' + '=' * 60)
    print('  CLINICAL TEST RUN COMPLETE')
    print('=' * 60)
    for name, viols in session_results:
        status = 'PASS' if viols == 0 else f'FAIL ({viols} violations)'
        print(f'  {name:<45} {status}')
    print()
    if total_violations == 0:
        print('  OVERALL RESULT: PASS - zero invariant violations')
        return 0
    else:
        print(f'  OVERALL RESULT: FAIL - {total_violations} invariant violation(s)')
        return 1


if __name__ == '__main__':
    sys.exit(main())
