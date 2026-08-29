from __future__ import annotations

from typing import NewType
from uuid import uuid4

AgentId = NewType("AgentId", str)
RoomId = NewType("RoomId", str)
EventId = NewType("EventId", str)
RunId = NewType("RunId", str)


def new_agent_id() -> AgentId:
    return AgentId(str(uuid4()))


def new_room_id() -> RoomId:
    return RoomId(str(uuid4()))


def new_event_id() -> EventId:
    return EventId(str(uuid4()))


def new_run_id() -> RunId:
    return RunId(str(uuid4()))