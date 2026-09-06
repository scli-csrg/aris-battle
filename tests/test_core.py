"""Core tests for the acoustic ARIS battle simulator."""

from __future__ import annotations

import random
import unittest

from aris_battle.channel import thorp_absorption_db_per_km
from aris_battle.experiments import paper_results, paper_summary
from aris_battle.metrics import interpolate_threshold
from aris_battle.optimizers import beamforming_binary


class AcousticModelTests(unittest.TestCase):
    def test_thorp_absorption_increases_between_1_and_10_khz(self) -> None:
        self.assertGreater(thorp_absorption_db_per_km(10.0), thorp_absorption_db_per_km(1.0))

    def test_jamming_thresholds_match_manuscript_trace(self) -> None:
        rows = paper_results()["jamming_sweep"]
        self.assertAlmostEqual(interpolate_threshold(rows, "no_aris_prr"), 10.0, places=2)
        self.assertAlmostEqual(interpolate_threshold(rows, "defender_aris_prr"), 32.94, places=2)

    def test_summary_contains_edge_consensus_values(self) -> None:
        summary = paper_summary()
        self.assertEqual(summary["consensus_win_rate_percent"], 55.0)
        self.assertEqual(summary["consensus_convergence_time_s"], 8.5)

    def test_binary_beamforming_returns_valid_coefficients(self) -> None:
        rng = random.Random(7)
        gains = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(16)]
        config = beamforming_binary(0.2 + 0.1j, gains, maximize=True)
        self.assertEqual(len(config), 16)
        self.assertTrue(all(value in (-1, 1) for value in config))


if __name__ == "__main__":
    unittest.main()

