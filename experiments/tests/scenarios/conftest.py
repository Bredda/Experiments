
from experiments.agents import MentionedAgent, Agent
from experiments.rooms.room import Room
from experiments.core.ids import AgentId, RoomId
import pytest

from experiments.scenarios.config import AgentConfig, RoomConfig, ScenarioConfig, SchedulerConfig

def make_agent(name: str, room_id = "1") -> Agent:
    return MentionedAgent(AgentId(name), name, RoomId(room_id))

def make_room(room_id = "1") -> Room:
    return Room(RoomId(room_id), "main")

@pytest.fixture
def basic_scenario() -> ScenarioConfig:
    return ScenarioConfig(
        name="basic-room",
        seed=42,
        agents= [
        AgentConfig("alice""mentioned", "mentioned"),
        AgentConfig("alice""mentioned", "mentioned"),
            AgentConfig("alice""mentioned", "mentioned")
        ],
        room=RoomConfig("main"),
        scheduler=SchedulerConfig("highest_urgency")
    )
