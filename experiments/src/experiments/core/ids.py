from __future__ import annotations

from typing import NewType
from uuid import UUID, uuid4

AgentId = NewType("AgentId", UUID)
RoomId = NewType("RoomId", UUID)
EventId = NewType("EventId", UUID)
RunId = NewType("RunId", UUID)


def new_agent_id() -> AgentId:
    return AgentId(uuid4())


def new_room_id() -> RoomId:
    return RoomId(uuid4())


def new_event_id() -> EventId:
    return EventId(uuid4())


def new_run_id() -> RunId:
    return RunId(uuid4())