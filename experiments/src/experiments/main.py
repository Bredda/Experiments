

import sys
from pathlib import Path

from experiments.agents import MentionedAgent
from experiments.core.ids import new_agent_id, new_room_id, new_run_id
from experiments.core.types import RunConfig
from experiments.rooms.room import Room
from experiments.scenarios import load_scenario, run_scenario
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
    if len(sys.argv) != 3 or sys.argv[1] != "run":
        print("Usage: experiments run <scenario.yaml>")
        return 1
    cwd = Path.cwd()
    root = cwd.parent
    print(root.absolute())
    scenario_path = Path(root, sys.argv[2])
    output_path = Path(root, "runs")
    scenario = load_scenario(scenario_path)
    output_dir = run_scenario(scenario, output_path)

    print(f"Run written to {output_dir}")

    return 0

