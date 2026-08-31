from __future__ import annotations

from experiments.core.actions import ActionProposal, Speak, StaySilent
from experiments.core.events import MessagePublished

from .agent import Agent, Observation


class MentionedAgent(Agent):
    def propose(
        self,
        observation: Observation,
    ) -> ActionProposal:
        messages = [
            event
            for event in observation.room.visible_events
            if isinstance(event, MessagePublished)
        ]

        if not messages:
            return ActionProposal(
                action=Speak(
                    agent_id=self.id,
                    room_id=self.room_id,
                    content=f"{self.name}: je suis là.",
                    urgency=0.2,
                )
            )

        last_message = messages[-1]

        if (
            last_message.agent_id != self.id
            and self.name.lower() in last_message.content.lower()
        ):
            return ActionProposal(
                action=Speak(
                    agent_id=self.id,
                    room_id=self.room_id,
                    content=f"{self.name}: j'ai été mentionné.",
                    urgency=0.9,
                )
            )

        return ActionProposal(
            action=StaySilent(agent_id=self.id),
        )