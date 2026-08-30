from pathlib import Path

import yaml

from .config import ScenarioConfig


def load_scenario(path: str | Path) -> ScenarioConfig:
    path = Path(path)

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return ScenarioConfig.model_validate(data)