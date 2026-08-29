from __future__ import annotations

from dataclasses import dataclass, field
from random import Random

from .ids import RunId


@dataclass
class RunConfig:
    run_id: RunId
    seed: int = 42
    _rng: Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = Random(self.seed)

    @property
    def rng(self) -> Random:
        return self._rng