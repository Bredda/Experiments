
from pathlib import Path

from experiments.scenarios import load_scenario


def test_load_basic_scenario():
    # Todo: mock fs
    fixture_path = Path(__file__).parent / "fixtures" / "basic.yml"
    scenario = load_scenario(fixture_path)

    assert scenario.name == "basic-room"
    assert scenario.seed == 42
    assert len(scenario.agents) == 3
    assert scenario.scheduler.type == "highest_urgency"