from experiments.agents.agent import Agent, Observation
from experiments.core.actions import Action, StaySilent


class SilentAgent(Agent):
    def propose(self, observation: Observation) -> Action:
        return StaySilent(agent_id=self.id)