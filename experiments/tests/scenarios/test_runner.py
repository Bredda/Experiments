import json
from pathlib import Path

from experiments.scenarios import load_scenario, run_scenario


def test_scenario_run_creates_artifacts(tmp_path):
    fixture_path = Path(__file__).parent / "fixtures" / "basic.yml"
    scenario = load_scenario(fixture_path)

    output = run_scenario(
        scenario,
        output_root=tmp_path,
    )

    assert (output / "config.json").exists()
    assert (output / "events.jsonl").exists()

def _normalize_events(content: str) -> list[dict]:
    events = [
        json.loads(line)
        for line in content.splitlines()
        if line.strip()
    ]

    for event in events:
        event.pop("id", None)

    return events

def test_same_scenario_same_seed(tmp_path):
    fixture_path = Path(__file__).parent / "fixtures" / "basic.yml"
    scenario = load_scenario(fixture_path)

    first = run_scenario(
        scenario,
        output_root=tmp_path / "first",
    )

    second = run_scenario(
        scenario,
        output_root=tmp_path / "second",
    )

    first_events = _normalize_events(
        (first / "events.jsonl").read_text()
    )
    second_events = _normalize_events(
        (second / "events.jsonl").read_text()
    )

    assert first_events == second_events