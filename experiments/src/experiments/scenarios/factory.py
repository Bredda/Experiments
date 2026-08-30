from __future__ import annotations

from experiments.agents import Agent, MentionedAgent
from experiments.core.ids import AgentId, RoomId, new_run_id
from experiments.core.types import RunConfig
from experiments.rooms.room import Room
from experiments.scheduler.highest_urgency import HighestUrgencyScheduler
from experiments.simulation.runtime import Simulation

from .config import ScenarioConfig

AGENT_BEHAVIORS: dict[str, type[Agent]] = {
    "mentioned": MentionedAgent,
}

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

def build_agent(
    agent_id: str,
    behavior: str,
    room_id: RoomId,
) -> Agent:
    try:
        agent_class = AGENT_BEHAVIORS[behavior]
    except KeyError as exc:
        raise ValueError(
            f"Unknown agent behavior: {behavior}"
        ) from exc

    return agent_class(
        AgentId(agent_id),
        agent_id,
        room_id,
    )

def build_run(scenario: ScenarioConfig):
    run_id = new_run_id()
    room_config = scenario.rooms[0]

    room_id = RoomId(room_config.id)

    room = Room(
        id=room_id,
        name=room_config.id,
    )

    agents = [
        build_agent(
            agent_id=agent.id,
            behavior=agent.behavior,
            room_id=room_id,
        )
        for agent in scenario.agents
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

    return run_id, simulation