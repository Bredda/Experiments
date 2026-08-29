from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .actions import Action
from .ids import AgentId, EventId, RoomId


@dataclass(frozen=True)
class Event:
    id: EventId
    timestamp: datetime
    step: int


@dataclass(frozen=True)
class AgentJoined(Event):
    agent_id: AgentId
    room_id: RoomId

    @property
    def type(self) -> Literal["agent.joined"]:
        return "agent.joined"


@dataclass(frozen=True)
class MessagePublished(Event):
    agent_id: AgentId
    room_id: RoomId
    content: str

    @property
    def type(self) -> Literal["message.published"]:
        return "message.published"


@dataclass(frozen=True)
class ActionProposed(Event):
    agent_id: AgentId
    action: Action

    @property
    def type(self) -> Literal["action.proposed"]:
        return "action.proposed"


@dataclass(frozen=True)
class ActionSelected(Event):
    agent_id: AgentId
    action: Action

    @property
    def type(self) -> Literal["action.selected"]:
        return "action.selected"


AnyEvent = (
    AgentJoined
    | MessagePublished
    | ActionProposed
    | ActionSelected
)