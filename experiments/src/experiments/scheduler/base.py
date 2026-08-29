from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from random import Random

from experiments.core.actions import Action
from experiments.core.ids import AgentId


@dataclass(frozen=True)
class Candidate:
    agent_id: AgentId
    action: Action


class Scheduler(ABC):
    @abstractmethod
    def select(
        self,
        candidates: Sequence[Candidate],
        rng: Random,
    ) -> Candidate:
        raise NotImplementedError

