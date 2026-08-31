from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from experiments.core.actions import ActionProposal
from experiments.core.events import AnyEvent
from experiments.core.ids import AgentId, RoomId
from experiments.rooms.room import RoomView

@dataclass(frozen=True)
class Observation:
    agent_id: AgentId
    room: RoomView
    step: int
    time: datetime


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
        room: RoomView,
    ) -> Observation:
        return Observation(
            agent_id=self.id,
            room=room,
            step=step,
            time=time,
        )

    @abstractmethod
    def propose(
        self,
        observation: Observation,
    ) -> ActionProposal:
        raise NotImplementedError