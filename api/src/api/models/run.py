from experiments.scenarios.config import ScenarioConfig
from pydantic import BaseModel


class Run(BaseModel):
    run_id: str
    scenario: ScenarioConfig
