"""Scenario configuration objects for acoustic ARIS battles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

Vector3 = Tuple[float, float, float]


@dataclass(frozen=True)
class AcousticEnvironment:
    """Underwater acoustic propagation settings."""

    frequency_khz: float = 10.0
    bandwidth_khz: float = 5.0
    sound_speed_mps: float = 1500.0
    water_depth_m: float = 100.0
    path_loss_exponent: float = 1.7
    multipath_taps: int = 6
    ambient_noise_std: float = 0.015
    bottom_reflection: float = 0.4


@dataclass(frozen=True)
class Node:
    """Named underwater or surface network node."""

    name: str
    position_m: Vector3


@dataclass(frozen=True)
class Surface:
    """Planar binary-phase acoustic reconfigurable intelligent surface."""

    name: str
    center_m: Vector3
    elements: int = 128
    spacing_m: float = 0.075
    active_elements: int | None = None

    @property
    def active_count(self) -> int:
        return self.elements if self.active_elements is None else min(self.elements, self.active_elements)


@dataclass(frozen=True)
class BattleScenario:
    """Nominal Alice/Bob/Eve/ARIS battle geometry."""

    environment: AcousticEnvironment
    alice: Node
    bob: Node
    eve: Node
    aris_a: Surface
    aris_b: Surface
    seed: int = 2026


def default_scenario(seed: int = 2026) -> BattleScenario:
    """Return the nominal scenario used by the manuscript case studies."""

    env = AcousticEnvironment()
    return BattleScenario(
        environment=env,
        alice=Node("Alice", (0.0, 0.0, 60.0)),
        bob=Node("Bob", (600.0, 120.0, 15.0)),
        eve=Node("Eve", (520.0, -130.0, 55.0)),
        aris_a=Surface("ARIS-A", (310.0, 55.0, 38.0), elements=128, spacing_m=0.075),
        aris_b=Surface("ARIS-B", (330.0, -60.0, 50.0), elements=128, spacing_m=0.075),
        seed=seed,
    )

