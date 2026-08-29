
import pytest

from experiments.agents import MentionedAgent, SilentAgent
from experiments.core.ids import new_agent_id, new_room_id, new_run_id
from experiments.core.types import RunConfig
from experiments.rooms.room import Room
from experiments.scheduler import HighestUrgencyScheduler
from experiments.simulation.runtime import Simulation


# Creating the common function for input
@pytest.fixture
def mentioned_simulation() -> Simulation:
    room = Room(
        id=new_room_id(),
        name="main",
    )

    agents = [
        MentionedAgent(new_agent_id(), "Alice", room.id),
        MentionedAgent(new_agent_id(), "Bob", room.id),
        MentionedAgent(new_agent_id(), "Charlie", room.id),
    ]

    return Simulation(
        run_id=new_run_id(),
        room=room,
        agents=agents,
        scheduler=HighestUrgencyScheduler(),
        config=RunConfig(run_id=new_run_id(), seed=42),
    )

@pytest.fixture
def silent_simulation() -> Simulation:
    room = Room(
        id=new_room_id(),
        name="main",
    )

    agents = [
        SilentAgent(new_agent_id(), "Alice", room.id),
        SilentAgent(new_agent_id(), "Bob", room.id),
        SilentAgent(new_agent_id(), "Charlie", room.id),
    ]

    return Simulation(
        run_id=new_run_id(),
        room=room,
        agents=agents,
        scheduler=HighestUrgencyScheduler(),
        config=RunConfig(run_id=new_run_id(), seed=42),
    )