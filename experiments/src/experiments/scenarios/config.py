from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AgentConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    behavior: str


class RoomConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    members: list[str] = Field(default_factory=list)


class SchedulerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: str


class ScenarioConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    seed: int
    agents: list[AgentConfig]
    rooms: list[RoomConfig]
    scheduler: SchedulerConfig
    steps: int = Field(default=10, ge=0)

    @model_validator(mode="after")
    def validate_memberships(self) -> "ScenarioConfig":
        agent_ids = {agent.id for agent in self.agents}

        for room in self.rooms:
            unknown_members = set(room.members) - agent_ids

            if unknown_members:
                raise ValueError(
                    f"Room '{room.id}' references unknown agents: "
                    f"{sorted(unknown_members)}"
                )

        return self