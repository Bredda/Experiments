from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from experiments.agents.agent import Agent
from experiments.core.actions import Speak
from experiments.core.clock import SimulationClock
from experiments.core.event_log import EventLog
from experiments.core.events import (
    ActionProposed,
    ActionSelected,
    AgentJoined,
    AnyEvent,
    MessagePublished,
)
from experiments.core.ids import RunId, new_event_id
from experiments.core.types import RunConfig
from experiments.rooms.room import Room
from experiments.scheduler.base import Candidate, Scheduler


@dataclass
class Simulation:
    run_id: RunId
    room: Room
    agents: Sequence[Agent]
    scheduler: Scheduler
    config: RunConfig
    clock: SimulationClock = field(default_factory=SimulationClock)
    events: EventLog = field(default_factory=EventLog)

    def append(self, event: AnyEvent) -> None:
        self.events.append(event)

    def setup(self) -> None:
        for agent in self.agents:
            self.room.add(agent.id)

            self.append(
                AgentJoined(
                    id=new_event_id(),
                    timestamp=self.clock.now,
                    agent_id=agent.id,
                    room_id=self.room.id,
                    step=self.clock.step,
                )
            )



    def export_events(self, path: Path) -> None:
        self.events.write_jsonl(path)

    def step(self) -> AnyEvent | None:
        """
        Advance the clock and execute a single step of the simulation.
        
        Each agent observes the current state of the simulation and proposes an action.
        The scheduler selects one of the proposed actions, which is then executed.  

        1. Agents observe and propose
        2. Record proposals
        3. Scheduler may select an executable action
        4. Execute selected action, if any
        5. Advance simulation time
        6. Return the last meaningful event
        
        Returns:
            The event corresponding to the executed action.
        """
        
        candidates: list[Candidate] = []
        last_event: AnyEvent | None = None

        for agent in self.agents:
            room_view = self.room.view(
                agent.id,
                self.events.to_list(),
            )

            observation = agent.observe(
                step=self.clock.step,
                time=self.clock.now,
                room=room_view,
            )

            proposal = agent.propose(observation)

            event = ActionProposed(
                id=new_event_id(),
                timestamp=self.clock.now,
                step=self.clock.step,
                agent_id=agent.id,
                action=proposal.action,
            )
            
            self.append(event)
            last_event = event

            if isinstance(proposal.action, Speak):
                candidates.append(
                    Candidate(
                        agent_id=agent.id,
                        action=proposal.action,
                    )
                )

        if candidates:
            selected = self.scheduler.select(
                candidates,
                self.config.rng,
            )

            selected_event = ActionSelected(
                id=new_event_id(),
                timestamp=self.clock.now,
                step=self.clock.step,
                agent_id=selected.agent_id,
                action=selected.action,
            )

            self.events.append(selected_event)
            last_event = selected_event

            if isinstance(selected.action, Speak):
                published = MessagePublished(
                    id=new_event_id(),
                    timestamp=self.clock.now,
                    step=self.clock.step,
                    agent_id=selected.action.agent_id,
                    room_id=selected.action.room_id,
                    content=selected.action.content,
                )

                self.events.append(published)
                last_event = published

        self.clock.advance()

        return last_event