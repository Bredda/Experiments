from __future__ import annotations

from pathlib import Path

import yaml

from .config import (
    AgentConfig,
    RoomConfig,
    ScenarioConfig,
    SchedulerConfig,
)


def load_scenario(path: str | Path) -> ScenarioConfig:
    path = Path(path)

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError("Scenario root must be a mapping")

    agents = [
        AgentConfig(
            id=agent["id"],
            behavior=agent["behavior"],
        )
        for agent in data["agents"]
    ]

    room_data = data["room"]

    room = RoomConfig(
        id=room_data["id"],
        members=room_data.get(
            "members",
            [agent.id for agent in agents],
        ),
    )

    scheduler = SchedulerConfig(
        type=data["scheduler"]["type"],
    )

    return ScenarioConfig(
        name=data["name"],
        seed=data["seed"],
        agents=agents,
        room=room,
        scheduler=scheduler,
        steps=data.get("steps", 10),
    )