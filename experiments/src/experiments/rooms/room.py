from __future__ import annotations

from dataclasses import dataclass, field

from experiments.core.ids import AgentId, RoomId


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