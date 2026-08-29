from collections.abc import Sequence
from random import Random

from .base import Candidate, Scheduler


class HighestUrgencyScheduler(Scheduler):
    def select(
        self,
        candidates: Sequence[Candidate],
        rng: Random,
    ) -> Candidate:
        if not candidates:
            raise ValueError("No candidates")

        return max(
            candidates,
            key=lambda candidate: getattr(
                candidate.action,
                "urgency",
                0.0,
            ),
        )