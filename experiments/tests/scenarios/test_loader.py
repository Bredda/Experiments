from experiments.scenarios import load_scenario

def test_load_basic_scenario():
    # Todo: mock fs
    scenario = load_scenario("scenarios/basic.yml")

    assert scenario.name == "basic-room"
    assert scenario.seed == 42
    assert len(scenario.agents) == 3
    assert scenario.scheduler.type == "highest_urgency"