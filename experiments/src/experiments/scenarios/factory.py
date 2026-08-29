from __future__ import annotations

from experiments.agents.agent import Agent, MentionedAgent
from experiments.core.ids import AgentId, RoomId


AGENT_BEHAVIORS = {
    "mentioned": MentionedAgent,
}


def build_agent(
    agent_id: str,
    behavior: str,
    room_id: RoomId,
) -> Agent:
    try:
        agent_class = AGENT_BEHAVIORS[behavior]
    except KeyError as exc:
        raise ValueError(
            f"Unknown agent behavior: {behavior}"
        ) from exc

    return agent_class(
        AgentId(agent_id),
        agent_id,
        room_id,
    )