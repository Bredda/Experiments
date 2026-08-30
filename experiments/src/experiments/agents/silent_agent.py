from experiments.agents.agent import Agent, Observation
from experiments.core.actions import ActionProposal, StaySilent


class SilentAgent(Agent):
    def propose(self, observation: Observation) -> ActionProposal:
        return ActionProposal(
                action=StaySilent(agent_id=self.id)
            )