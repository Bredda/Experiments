from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from experiments.agents import Agent
from experiments.core.ids import RoomId, new_run_id
from experiments.core.types import RunConfig
from experiments.rooms.room import Room
from experiments.scheduler import HighestUrgencyScheduler
from experiments.simulation.runtime import Simulation

from .config import ScenarioConfig
from .factory import build_agent

SCHEDULERS = {
    "highest_urgency": HighestUrgencyScheduler,
}


def build_scheduler(scenario: ScenarioConfig):
    try:
        scheduler_class = SCHEDULERS[scenario.scheduler.type]
    except KeyError as exc:
        raise ValueError(
            f"Unknown scheduler: {scenario.scheduler.type}"
        ) from exc

    return scheduler_class()


def run_scenario(
    scenario: ScenarioConfig,
    output_root: str | Path = "runs",
) -> Path:
    run_id = new_run_id()

    room_id = RoomId(scenario.room.id)

    room = Room(
        id=room_id,
        name=scenario.room.id,
    )

    agents: list[Agent] = [
        build_agent(
            agent_id=config.id,
            behavior=config.behavior,
            room_id=room_id,
        )
        for config in scenario.agents
    ]

    simulation = Simulation(
        run_id=run_id,
        room=room,
        agents=agents,
        scheduler=build_scheduler(scenario),
        config=RunConfig(
            run_id=run_id,
            seed=scenario.seed,
        ),
    )

    simulation.setup()

    for _ in range(scenario.steps):
        simulation.step()

    output_dir = Path(output_root) / str(run_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    simulation.export_events(
        output_dir / "events.jsonl",
    )

    with (output_dir / "config.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        output = {
            "run_id": run_id,
            "scenario": asdict(scenario)
        }
        json.dump(
            output,
            file,
            indent=2,
        )

    return output_dir