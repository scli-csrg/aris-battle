"""Metrics used by acoustic ARIS battle experiments."""

from __future__ import annotations

import math
from typing import Iterable, Sequence, Tuple


def packet_reception_rate(jamming_gain_db: float, threshold_db: float, slope: float = 0.7) -> float:
    """Smooth PRR curve centered at the 50 percent outage threshold."""

    return 100.0 / (1.0 + math.exp(slope * (jamming_gain_db - threshold_db)))


def interpolate_threshold(rows: Sequence[dict], column: str, target: float = 50.0, x_key: str = "gain_db") -> float:
    """Linearly interpolate the x-value at which a metric reaches target."""

    ordered = sorted(rows, key=lambda row: row[x_key])
    for left, right in zip(ordered, ordered[1:]):
        y0 = float(left[column])
        y1 = float(right[column])
        if (y0 - target) == 0:
            return float(left[x_key])
        if (y0 - target) * (y1 - target) <= 0:
            x0 = float(left[x_key])
            x1 = float(right[x_key])
            if y1 == y0:
                return x0
            return x0 + (target - y0) * (x1 - x0) / (y1 - y0)
    raise ValueError(f"target {target} is outside the range of {column}")


def qpsk_symbols() -> Tuple[complex, complex, complex, complex]:
    return (1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j)


def nearest_qpsk(symbol: complex) -> complex:
    return min(qpsk_symbols(), key=lambda reference: abs(symbol - reference))


def symbol_error_rate(transmitted: Iterable[complex], received: Iterable[complex]) -> float:
    tx = list(transmitted)
    rx = list(received)
    if len(tx) != len(rx):
        raise ValueError("transmitted and received sequences must have the same length")
    if not tx:
        return 0.0
    errors = sum(nearest_qpsk(x) != nearest_qpsk(y) for x, y in zip(tx, rx))
    return 100.0 * errors / len(tx)


def detection_accuracy(true_positive: int, total_positive: int) -> float:
    if total_positive <= 0:
        raise ValueError("total_positive must be positive")
    return 100.0 * true_positive / total_positive


def configuration_energy_j(
    pilot_count: int,
    pilot_energy_j: float,
    control_bytes: int,
    propagation_delay_s: float,
    iterations: int,
    active_elements: int,
    tx_j_per_byte_s: float = 0.00035,
    compute_j_per_iteration_element: float = 0.0009,
    switch_j_per_element: float = 0.012,
) -> float:
    """Energy model for probing, compressed control exchange, compute, and switching."""

    probing = pilot_count * pilot_energy_j
    tx = tx_j_per_byte_s * control_bytes * max(propagation_delay_s, 0.0)
    compute = compute_j_per_iteration_element * iterations * active_elements
    switching = switch_j_per_element * active_elements
    return probing + tx + compute + switching

