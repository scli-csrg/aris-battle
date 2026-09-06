"""Optimization algorithms for binary acoustic ARIS configurations."""

from __future__ import annotations

import math
import random
from typing import Callable, Dict, Iterable, List, Sequence, Tuple

Configuration = List[int]
Objective = Callable[[Sequence[int]], float]


def random_configuration(elements: int, rng: random.Random) -> Configuration:
    """Draw a binary phase configuration."""

    return [rng.choice((-1, 1)) for _ in range(elements)]


def objective_better(candidate: float, incumbent: float, maximize: bool) -> bool:
    return candidate > incumbent if maximize else candidate < incumbent


def element_flip_search(
    initial: Sequence[int],
    objective: Objective,
    maximize: bool = True,
    max_passes: int = 4,
) -> Tuple[Configuration, float]:
    """Local search that accepts improving one-element flips."""

    config = list(initial)
    best = objective(config)
    for _ in range(max_passes):
        improved = False
        for idx in range(len(config)):
            trial = list(config)
            trial[idx] *= -1
            value = objective(trial)
            if objective_better(value, best, maximize):
                config, best, improved = trial, value, True
        if not improved:
            break
    return config, best


def greedy_random_search(
    elements: int,
    objective: Objective,
    rng: random.Random,
    maximize: bool = True,
    iterations: int = 128,
    flip_fraction: float = 0.08,
) -> Tuple[Configuration, float]:
    """Greedy stochastic search over binary phase vectors."""

    current = random_configuration(elements, rng)
    current_value = objective(current)
    best, best_value = list(current), current_value
    flips = max(1, int(elements * flip_fraction))

    for _ in range(iterations):
        trial = list(current)
        for idx in rng.sample(range(elements), flips):
            trial[idx] *= -1
        value = objective(trial)
        if objective_better(value, current_value, maximize):
            current, current_value = trial, value
        if objective_better(value, best_value, maximize):
            best, best_value = list(trial), value
    return best, best_value


def beamforming_binary(base: complex, gains: Sequence[complex], maximize: bool = True) -> Configuration:
    """Binary alignment heuristic for maximizing or suppressing channel power."""

    config: Configuration = []
    running = base
    for gain in gains:
        plus = abs(running + gain) ** 2
        minus = abs(running - gain) ** 2
        choose_plus = plus >= minus if maximize else plus < minus
        coeff = 1 if choose_plus else -1
        config.append(coeff)
        running += coeff * gain
    return config


def consensus_sign_update(
    current: Sequence[int],
    neighbor_gradients: Sequence[Sequence[float]],
    neighbor_weights: Sequence[float],
    freshness: Sequence[float],
    eta: float = 1.0,
) -> Configuration:
    """Freshness-gated sign update for distributed ARIS control."""

    if not neighbor_gradients:
        return list(current)
    if not (len(neighbor_gradients) == len(neighbor_weights) == len(freshness)):
        raise ValueError("gradient, weight, and freshness lists must align")

    updated: Configuration = []
    for idx, value in enumerate(current):
        step = 0.0
        for grad, weight, fresh in zip(neighbor_gradients, neighbor_weights, freshness):
            step += weight * fresh * grad[idx]
        raw = value - eta * step
        updated.append(1 if raw >= 0.0 else -1)
    return updated


def hamming_distance(a: Sequence[int], b: Sequence[int]) -> int:
    if len(a) != len(b):
        raise ValueError("configurations must have the same length")
    return sum(x != y for x, y in zip(a, b))


def bayesian_hamming_search(
    elements: int,
    objective: Objective,
    rng: random.Random,
    maximize: bool = True,
    iterations: int = 64,
    candidates_per_iteration: int = 32,
    length_scale: float = 24.0,
    kappa: float = 0.75,
) -> Tuple[Configuration, float]:
    """Sample-efficient search using a Hamming-kernel UCB surrogate.

    This is intentionally dependency-free. It captures the paper's use of a
    surface-code similarity model without requiring a full Gaussian-process
    library.
    """

    observations: List[Tuple[Configuration, float]] = []
    for _ in range(min(4, max(1, iterations))):
        cfg = random_configuration(elements, rng)
        observations.append((cfg, objective(cfg)))

    best_cfg, best_value = observations[0]
    for cfg, value in observations[1:]:
        if objective_better(value, best_value, maximize):
            best_cfg, best_value = cfg, value

    for _ in range(max(0, iterations - len(observations))):
        scored: List[Tuple[float, Configuration]] = []
        for _ in range(candidates_per_iteration):
            candidate = random_configuration(elements, rng)
            mean, uncertainty = _surrogate_predict(candidate, observations, length_scale)
            score = mean + kappa * uncertainty if maximize else mean - kappa * uncertainty
            scored.append((score, candidate))
        scored.sort(key=lambda item: item[0], reverse=maximize)
        chosen = scored[0][1]
        value = objective(chosen)
        observations.append((chosen, value))
        if objective_better(value, best_value, maximize):
            best_cfg, best_value = chosen, value
    return list(best_cfg), best_value


def _surrogate_predict(
    candidate: Sequence[int],
    observations: Iterable[Tuple[Sequence[int], float]],
    length_scale: float,
) -> Tuple[float, float]:
    weighted_sum = 0.0
    weight_total = 0.0
    values: List[float] = []
    for cfg, value in observations:
        dist = hamming_distance(candidate, cfg)
        weight = math.exp(-dist / max(length_scale, 1e-9))
        weighted_sum += weight * value
        weight_total += weight
        values.append(value)
    mean = weighted_sum / max(weight_total, 1e-15)
    spread = max(values) - min(values) if values else 1.0
    density = min(weight_total / max(len(values), 1), 1.0)
    uncertainty = spread * (1.0 - density)
    return mean, uncertainty

