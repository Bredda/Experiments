from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from experiments.core.actions import Action, Speak, StaySilent
from experiments.core.events import AnyEvent, MessagePublished
from experiments.core.ids import AgentId, RoomId


@dataclass(frozen=True)
class Observation:
    agent_id: AgentId
    room_id: RoomId
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

    def observe(self, events: Sequence[AnyEvent]) -> Observation:
        return Observation(
            agent_id=self.id,
            room_id=self.room_id,
            events=events,
        )

    @abstractmethod
    def propose(self, observation: Observation) -> Action:
        raise NotImplementedError


class MentionedAgent(Agent):
    def propose(self, observation: Observation):
        messages = [
            event
            for event in observation.events
            if isinstance(event, MessagePublished)
        ]

        if not messages:
            return Speak(
                agent_id=self.id,
                room_id=self.room_id,
                content=f"{self.name}: je suis là.",
                urgency=0.2,
            )

        last_message = messages[-1]

        if (
            last_message.agent_id != self.id
            and self.name.lower() in last_message.content.lower()
        ):
            return Speak(
                agent_id=self.id,
                room_id=self.room_id,
                content=f"{self.name}: j'ai été mentionné.",
                urgency=0.9,
            )

        return StaySilent(agent_id=self.id)