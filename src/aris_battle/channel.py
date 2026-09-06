"""Underwater acoustic channel and ARIS contribution models."""

from __future__ import annotations

import cmath
import math
import random
from typing import Iterable, List, Sequence

from .config import AcousticEnvironment, Node, Surface, Vector3


def db_to_power(db_value: float) -> float:
    """Convert dB to linear power."""

    return 10.0 ** (db_value / 10.0)


def power_to_db(power_value: float, floor: float = 1e-15) -> float:
    """Convert linear power to dB with a small numerical floor."""

    return 10.0 * math.log10(max(power_value, floor))


def thorp_absorption_db_per_km(frequency_khz: float) -> float:
    """Thorp absorption coefficient for underwater acoustics in dB/km."""

    f2 = frequency_khz * frequency_khz
    return 0.11 * f2 / (1.0 + f2) + 44.0 * f2 / (4100.0 + f2) + 2.75e-4 * f2 + 0.003


def distance_m(a: Vector3, b: Vector3) -> float:
    """Euclidean distance between two 3D positions in meters."""

    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _path_phase(distance: float, env: AcousticEnvironment, time_s: float = 0.0) -> float:
    carrier_hz = env.frequency_khz * 1000.0
    delay = distance / env.sound_speed_mps
    return 2.0 * math.pi * carrier_hz * (delay + time_s)


def path_gain(distance: float, env: AcousticEnvironment) -> float:
    """Amplitude gain from spreading loss and frequency-dependent absorption."""

    d = max(distance, 1.0)
    d_km = d / 1000.0
    absorption_db = thorp_absorption_db_per_km(env.frequency_khz) * d_km
    absorption_amp = 10.0 ** (-absorption_db / 20.0)
    spreading_amp = d ** (-env.path_loss_exponent / 2.0)
    return absorption_amp * spreading_amp


def direct_channel(tx: Node, rx: Node, env: AcousticEnvironment, rng: random.Random | None = None, time_s: float = 0.0) -> complex:
    """Compute a direct acoustic channel with lightweight stochastic multipath."""

    d = distance_m(tx.position_m, rx.position_m)
    base = path_gain(d, env) * cmath.exp(1j * _path_phase(d, env, time_s))
    if rng is None or env.multipath_taps <= 1:
        return base

    multipath = 1.0 + 0.0j
    for tap in range(1, env.multipath_taps):
        reflection = env.bottom_reflection ** tap
        delay_jitter = rng.uniform(0.002, 0.08) * tap
        phase = _path_phase(d + env.sound_speed_mps * delay_jitter, env, time_s)
        amplitude = reflection / (tap + 1.0)
        multipath += amplitude * cmath.exp(1j * phase)
    return base * multipath


def element_positions(surface: Surface) -> List[Vector3]:
    """Place active ARIS elements on a compact rectangular grid."""

    count = surface.active_count
    cols = math.ceil(math.sqrt(count))
    rows = math.ceil(count / cols)
    cx, cy, cz = surface.center_m
    positions: List[Vector3] = []
    for idx in range(count):
        row = idx // cols
        col = idx % cols
        x = cx + (col - (cols - 1) / 2.0) * surface.spacing_m
        y = cy + (row - (rows - 1) / 2.0) * surface.spacing_m
        positions.append((x, y, cz))
    return positions


def aris_element_gains(
    tx: Node,
    rx: Node,
    surface: Surface,
    env: AcousticEnvironment,
    rng: random.Random | None = None,
) -> List[complex]:
    """Return the cascaded tx-element-rx gain for each active ARIS element."""

    gains: List[complex] = []
    for idx, pos in enumerate(element_positions(surface)):
        element = Node(f"{surface.name}-{idx}", pos)
        h = direct_channel(tx, element, env, rng)
        g = direct_channel(element, rx, env, rng)
        aperture_norm = math.sqrt(max(surface.active_count, 1))
        gains.append(h * g * aperture_norm)
    return gains


def aris_contribution(gains: Sequence[complex], coefficients: Sequence[int]) -> complex:
    """Apply binary reflection coefficients to ARIS element gains."""

    if len(gains) != len(coefficients):
        raise ValueError("gains and coefficients must have the same length")
    return sum(g * c for g, c in zip(gains, coefficients))


def effective_channel(
    direct: complex,
    gains_a: Sequence[complex],
    config_a: Sequence[int],
    gains_b: Sequence[complex],
    config_b: Sequence[int],
    mutual_coupling: complex = 0.0 + 0.0j,
) -> complex:
    """Combine direct, defender ARIS, adversary ARIS, and mutual coupling terms."""

    h_a = aris_contribution(gains_a, config_a)
    h_b = aris_contribution(gains_b, config_b)
    h_ab = mutual_coupling * h_a * h_b
    return direct + h_a + h_b + h_ab


def variance(values: Iterable[complex]) -> float:
    """Population variance of complex magnitudes around the complex mean."""

    items = list(values)
    if not items:
        return 0.0
    mean = sum(items) / len(items)
    return sum(abs(x - mean) ** 2 for x in items) / len(items)


def mutual_snr(gains_self: Sequence[complex], gains_other: Sequence[complex], direct_variance: float) -> float:
    """Mutual SNR used to reason about distinguishability of surface effects."""

    numerator = sum(abs(g) ** 2 for g in gains_self)
    denominator = sum(abs(g) ** 2 for g in gains_other) + direct_variance
    return numerator / max(denominator, 1e-15)

