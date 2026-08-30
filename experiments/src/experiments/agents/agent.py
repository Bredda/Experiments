from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from experiments.core.actions import ActionProposal
from experiments.core.events import AnyEvent
from experiments.core.ids import AgentId, RoomId


@dataclass(frozen=True)
class Observation:
    agent_id: AgentId
    room_id: RoomId
    step: int
    time: datetime
    events: Sequence[AnyEvent]


class Agent(ABC):
    def __init__(
        self,
        agent_id: AgentId,
        name: str,
        room_id: RoomId,
    ) -> None:
        self.id = agent_id
        self.name = name
        self.room_id = room_id

    def observe(
        self,
        *,
        step: int,
        time: datetime,
        events: Sequence[AnyEvent],
    ) -> Observation:
        return Observation(
            agent_id=self.id,
            room_id=self.room_id,
            step=step,
            time=time,
            events=events,
        )

    @abstractmethod
    def propose(
        self,
        observation: Observation,
    ) -> ActionProposal:
        raise NotImplementedError