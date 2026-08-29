from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass
class SimulationClock:
    start: datetime = field(
        default_factory=lambda: datetime(2026, 1, 1, tzinfo=UTC)
    )
    step_size: timedelta = timedelta(seconds=1)
    _step: int = field(default=0, init=False)

    @property
    def now(self) -> datetime:
        return self.start + (self.step_size * self._step)

    @property
    def step(self) -> int:
        return self._step

    def advance(self) -> datetime:
        self._step += 1
        return self.now

    def reset(self) -> None:
        self._step = 0