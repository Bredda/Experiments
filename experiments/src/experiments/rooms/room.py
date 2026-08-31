from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from experiments.core.events import AnyEvent
from experiments.core.ids import AgentId, RoomId


@dataclass(frozen=True)
class RoomView:
    room_id: RoomId
    visible_events: Sequence[AnyEvent]


@dataclass
class Room:
    id: RoomId
    name: str
    members: set[AgentId] = field(default_factory=set)

    def add(self, agent_id: AgentId) -> None:
        self.members.add(agent_id)

    def remove(self, agent_id: AgentId) -> None:
        self.members.discard(agent_id)

    def contains(self, agent_id: AgentId) -> bool:
        return agent_id in self.members

    def view(
        self,
        agent_id: AgentId,
        events: Sequence[AnyEvent],
    ) -> RoomView:
        if not self.contains(agent_id):
            raise ValueError(
                f"Agent {agent_id} is not a member of room {self.id}"
            )

        return RoomView(
            room_id=self.id,
            visible_events=events,
        )