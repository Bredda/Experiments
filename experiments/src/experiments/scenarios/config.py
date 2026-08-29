from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AgentConfig:
    id: str
    behavior: str


@dataclass(frozen=True)
class RoomConfig:
    id: str
    members: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SchedulerConfig:
    type: str


@dataclass(frozen=True)
class ScenarioConfig:
    name: str
    seed: int
    agents: list[AgentConfig]
    room: RoomConfig
    scheduler: SchedulerConfig
    steps: int = 10