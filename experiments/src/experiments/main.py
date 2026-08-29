

from experiments.agents import MentionedAgent
from experiments.core.ids import new_agent_id, new_room_id, new_run_id
from experiments.core.types import RunConfig
from experiments.rooms.room import Room
from experiments.scheduler import HighestUrgencyScheduler
from experiments.simulation.runtime import Simulation

room = Room(
    id=new_room_id(),
    name="main",
)

agents = [
    MentionedAgent(new_agent_id(), "Alice", room.id),
    MentionedAgent(new_agent_id(), "Bob", room.id),
    MentionedAgent(new_agent_id(), "Charlie", room.id),
]

config = RunConfig(run_id=new_run_id(), seed=42)

simulation = Simulation(
    run_id=new_run_id(),
    room=room,
    agents=agents,
    scheduler=HighestUrgencyScheduler(),
    config=config
)

simulation.setup()


def run() -> int:
    for _ in range(10):
        event = simulation.step()
        print(event)
    simulation.export_events("runs/basic/run.jsonl")    
    return 0

