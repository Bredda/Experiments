from collections.abc import Sequence
from random import Random

from .base import Candidate, Scheduler


class WeightedRandomScheduler(Scheduler):
    def select(
        self,
        candidates: Sequence[Candidate],
        rng: Random,
    ) -> Candidate:
        if not candidates:
            raise ValueError("No candidates")

        weights = [
            max(
                0.0,
                float(getattr(candidate.action, "urgency", 0.0)),
            )
            for candidate in candidates
        ]

        total = sum(weights)

        if total <= 0:
            return rng.choice(list(candidates))

        return rng.choices(
            list(candidates),
            weights=weights,
            k=1,
        )[0]