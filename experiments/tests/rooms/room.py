from experiments.core.ids import AgentId, RoomId
from experiments.rooms.room import Room
from experiments.simulation.runtime import Simulation
import pytest


def test_room_view_contains_visible_events(silent_simulation: Simulation) -> None:
    simulation = silent_simulation
    simulation.setup()

    agent = simulation.agents[0]

    view = simulation.room.view(
        agent.id,
        simulation.events.to_list(),
    )

    assert view.room_id == simulation.room.id
    assert list(view.visible_events) == simulation.events.to_list()

def test_non_member_cannot_get_room_view() -> None:
    room = Room(
        id=RoomId("main"),
        name="main",
    )

    with pytest.raises(ValueError):
        room.view(
            AgentId("outsider"),
            [],
        )