from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from .config import ScenarioConfig
from .factory import build_run




def run_scenario(
    scenario: ScenarioConfig,
    output_root: str | Path = "runs",
) -> Path:

    if len(scenario.rooms) != 1:
        raise ValueError(
            "The current simulation engine supports exactly one room")
    
    run_id, simulation = build_run(scenario)

    simulation.setup()

    for _ in range(scenario.steps):
        simulation.step()

    output_dir = Path(output_root) / str(run_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    simulation.export_events(
        output_dir / "events.jsonl",
    )

    with (output_dir / "config.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        output = {
            "run_id": run_id,
            "scenario": (scenario.model_dump())
        }
        json.dump(
            output,
            file,
            indent=2,
        )

    return output_dir