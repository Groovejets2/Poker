"""Logging and report writing for clinical test sessions."""

import os
from datetime import datetime
from typing import Dict, List


class SimulationLogger:
    """
    Logs hand results to stdout during a session and writes a Markdown
    report to docs/tests/ on completion.
    """

    def __init__(self, session_name: str, output_dir: str = None) -> None:
        self.session_name = session_name
        self.output_dir = output_dir or os.path.normpath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'tests')
        )
        self.log_lines: List[str] = []
        self.start_time = datetime.now()

    def log(self, message: str) -> None:
        """Print and store a log line."""
        self.log_lines.append(message)
        print(message)

    def log_hand(
        self,
        hand_num: int,
        winners: Dict[str, int],
        pot: int,
        violations: List[str],
    ) -> None:
        """Log the result of a single hand."""
        winner_str = ', '.join(
            f"{k}+{v}" for k, v in winners.items() if v > 0
        )
        if violations:
            status = f"[VIOLATION] {'; '.join(violations)}"
        else:
            status = "OK"
        self.log(f"  Hand {hand_num:4d}: pot={pot:5d}  [{winner_str}]  {status}")

    def log_batch(self, batch_num: int, hands_done: int, stats: dict) -> None:
        """Log a summary after each batch of hands."""
        self.log(f"\n--- Batch {batch_num} complete ({hands_done} hands total) ---")
        self.log(f"    Violations so far : {stats['invariant_violations']}")
        self.log(f"    Average pot       : {stats['average_pot']}")
        self.log(f"    Showdown rate     : {stats['showdown_rate']}")

    def log_section(self, title: str) -> None:
        """Log a section header."""
        self.log(f"\n{'=' * 60}")
        self.log(f"  {title}")
        self.log(f"{'=' * 60}")

    def log_summary(self, summary: dict) -> None:
        """Log the final session summary."""
        self.log(f"\n  Result              : {'PASS' if summary['invariant_violations'] == 0 else 'FAIL'}")
        self.log(f"  Hands played        : {summary['hands_played']}")
        self.log(f"  Showdown rate       : {summary['showdown_rate']}")
        self.log(f"  Average pot         : {summary['average_pot']}")
        self.log(f"  Largest pot         : {summary['largest_pot']}")
        self.log(f"  Invariant violations: {summary['invariant_violations']}")
        self.log(f"\n  Wins per player:")
        for player, wins in summary['wins_per_player'].items():
            chips = summary['chips_won_per_player'].get(player, 0)
            self.log(f"    {player:<25} {wins:4d} wins  {chips:8d} chips")

    def write_report(self, summary: dict, session_label: str) -> str:
        """
        Write a Markdown report to docs/tests/ and return the file path.
        """
        timestamp = self.start_time.strftime('%Y-%m-%d')
        filename = f"{timestamp}_clinical-test-results_{session_label}_v1.0.md"
        filepath = os.path.normpath(os.path.join(self.output_dir, filename))

        result_status = 'PASS' if summary['invariant_violations'] == 0 else 'FAIL'

        lines = [
            f"# Clinical Test Results - {self.session_name}",
            f"",
            f"**Session:** {self.session_name}",
            f"**Date:** {timestamp}",
            f"**Result:** {result_status}",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Hands played | {summary['hands_played']} |",
            f"| Showdown rate | {summary['showdown_rate']} |",
            f"| Average pot | {summary['average_pot']} chips |",
            f"| Largest pot | {summary['largest_pot']} chips |",
            f"| Invariant violations | {summary['invariant_violations']} |",
            f"",
            f"## Results by Player",
            f"",
            f"| Player | Wins | Chips Won |",
            f"|--------|------|-----------|",
        ]

        for player, wins in summary['wins_per_player'].items():
            chips = summary['chips_won_per_player'].get(player, 0)
            lines.append(f"| {player} | {wins} | {chips} |")

        violation_note = (
            'None detected.'
            if summary['invariant_violations'] == 0
            else f"{summary['invariant_violations']} violation(s) detected - review log output."
        )

        lines += [
            f"",
            f"## Invariant Check",
            f"",
            f"{violation_note}",
            f"",
            f"---",
            f"",
            f"**Document Created:** {timestamp} GMT+13",
            f"**Version:** 1.0",
            f"**Status:** {'APPROVED' if result_status == 'PASS' else 'REVIEW REQUIRED'}",
        ]

        os.makedirs(self.output_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return filepath
