from experiments.core.events import ActionSelected, MessagePublished
from experiments.simulation.runtime import Simulation


def test_setup_adds_all_agents_to_room(mentioned_simulation: Simulation) -> None:
    simulation = mentioned_simulation

    simulation.setup()

    assert simulation.room.members == {
        agent.id for agent in simulation.agents
    }
    assert len(simulation.events) == 3
    assert simulation.clock.step == 0


def test_step_advances_time_and_publishes_one_message(mentioned_simulation: Simulation) -> None:
    simulation = mentioned_simulation
    simulation.setup()

    simulation.step()

    events = simulation.events.to_list()

    selected = [
        event
        for event in events
        if isinstance(event, ActionSelected)
    ]

    published = [
        event
        for event in events
        if isinstance(event, MessagePublished)
    ]

    assert len(selected) == 1
    assert len(published) == 1
    assert simulation.clock.step == 1



def test_silent_step_still_advances_time(silent_simulation: Simulation) -> None:
    simulation = silent_simulation

    simulation.setup()

    before = len(simulation.events)

    result = simulation.step()

    after = simulation.events.to_list()

    assert simulation.clock.step == 1
    assert len(after) == before + len(simulation.agents)
    assert result is not None

    assert all(
        event.type == "action.proposed"
        for event in after[before:]
    )