from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import UUID

from experiments.core.events import AnyEvent


def _serialize(value: Any) -> Any:
    if isinstance(value, UUID):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, Enum):
        return value.value

    if is_dataclass(value) and not isinstance(value, type):
        return {
            field.name: _serialize(getattr(value, field.name))
            for field in fields(value)
        }

    if isinstance(value, dict):
        return {
            str(key): _serialize(val)
            for key, val in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [_serialize(item) for item in value]

    return value

class EventLog:
    def __init__(self) -> None:
        self._events: list[AnyEvent] = []

    def append(self, event: AnyEvent) -> None:
        self._events.append(event)

    def extend(self, events: Iterable[AnyEvent]) -> None:
        self._events.extend(events)

    def __iter__(self):
        return iter(self._events)

    def __len__(self) -> int:
        return len(self._events)

    def __getitem__(self, index: int) -> AnyEvent:
        return self._events[index]

    def to_list(self) -> list[AnyEvent]:
        return list(self._events)

    def write_jsonl(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            for event in self._events:
                payload = _serialize(event)
                payload["type"] = event.type
                file.write(json.dumps(payload) + "\n")