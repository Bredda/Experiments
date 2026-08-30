from pydantic import BaseModel

from experiments.scenarios.config import ScenarioConfig

class Run(BaseModel):
    run_id: str
    scenario: ScenarioConfig
