from __future__ import annotations

from dataclasses import dataclass

from experiments.core.ids import AgentId, RoomId


@dataclass(frozen=True)
class Speak:
    """
    Structure holding Speak action data

    Attributes:
        agent_id: The ID of the agent speaking
        room_id: The ID of the room where the speech occurs
        content: The content of the speech
        urgency: A float representing the urgency of the speech, defaulting to 0.5
    """

    agent_id: AgentId
    room_id: RoomId
    content: str
    urgency: float = 0.5
    relevance: float = 0.5
    social_cost: float = 0.0
    @property
    def score(self) -> float:
        return (
            self.urgency
            + self.relevance
            - self.social_cost
        )
    
@dataclass(frozen=True)
class StaySilent:
    """
    Structure holding StaySilent action data

    Attributes:
        agent_id: The ID of the agent staying silent
    """
    agent_id: AgentId


Action = Speak | StaySilent