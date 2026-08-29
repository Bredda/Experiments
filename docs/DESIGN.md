# experiments — Technical Design & MVP Roadmap

## 1. Purpose

`experiments` is an experimental environment for studying **multi-agent systems built around LLMs**.

The primary goal is not to provide a production-oriented agent framework. It is to make it easy to:

- define different multi-agent setups;
- run them reproducibly;
- observe what happened;
- inspect agent interactions and state;
- experiment with communication structures and decision policies;
- replay and compare runs.

The central research question is broader than “how do several LLMs debate?”:

> How do different agent architectures, communication rules, memory models, and interaction policies affect the behavior of a multi-agent system?

Conversation is one important interaction mechanism, but it should not be hard-coded as the fundamental abstraction.

---

# 2. Current Scope

The project currently consists of:

```text
experiments/
├── engine/                 # Python simulation engine
├── ui/                     # Next.js frontend
├── scenarios/              # experiment definitions
├── infra/                  # local observability infrastructure
└── README.md
```

The repository is intentionally split between:

- **Python** for the simulation engine;
- **TypeScript / Next.js** for the UI.

There is no shared runtime code between the two. Communication between them will happen through explicit contracts and APIs.

---

# 3. Architectural Principles

## 3.1 Simulation first

The simulation engine is the core of the project.

The UI, LLM providers, database, and observability stack must remain replaceable infrastructure around it.

The engine should be executable independently of the web application.

---

## 3.2 Events are the fundamental interaction record

The engine records what happens as events.

Examples:

```text
agent.joined
action.proposed
action.selected
message.published
```

An event represents a fact that happened in the simulation.

This provides the foundation for:

- debugging;
- replay;
- persistence;
- observability;
- experiment analysis.

---

## 3.3 State and history are separate concepts

The project distinguishes between:

```text
Event
    What happened?

State
    What is true now?

Trace
    How did the system get there / what instrumentation was produced?
```

The current implementation primarily covers the first of these.

Future versions should avoid making the event log a substitute for application state.

---

## 3.4 Agents propose actions

Agents do not directly control the simulation.

The conceptual execution flow is:

```text
World state
    ↓
Agent observes
    ↓
Agent proposes an action
    ↓
Scheduler selects an action
    ↓
Simulation executes the action
    ↓
Event is produced
    ↓
World state changes
```

This is deliberately different from a simple:

```text
agent A → agent B → agent C
```

execution model.

---

## 3.5 Scheduling is independent from agents

The scheduler determines which proposed action is executed.

This creates an explicit seam for experimentation.

Possible future schedulers include:

```text
RoundRobin
Random
Priority
WeightedRandom
Emergent / policy-based
```

The MVP does not need all of them.

---

# 4. Current Engine Structure

The current Python package is structured around the following concepts:

```text
engine/src/experiments/

├── core/
│   ├── actions.py
│   ├── events.py
│   ├── event_log.py
│   ├── clock.py
│   ├── ids.py
│   └── types.py
│
├── agents/
│   └── agent.py
│
├── rooms/
│   └── room.py
│
├── scheduler/
│   └── base.py
│
└── simulation/
    └── runtime.py
```

This structure is provisional and may evolve as the model becomes clearer.

---

# 5. Core Domain Model

## 5.1 Agent

An agent currently has:

- an ID;
- a name;
- a room;
- an observation step;
- an action proposal step.

Conceptually:

```python
observation = agent.observe(events)
action = agent.propose(observation)
```

LLM reasoning and memory are not yet part of the core execution path.

---

## 5.2 Room

A room currently represents group membership and topology.

Example:

```text
main
├── Alice
├── Bob
└── Charlie
```

Rooms are intentionally simple at this stage.

Future room features may include:

- visibility rules;
- private rooms;
- partial transcripts;
- room creation / destruction;
- agent movement;
- temporary isolation.

These are **not MVP requirements**.

---

## 5.3 Action

The current model includes simple actions such as:

```text
Speak
StaySilent
```

The exact action vocabulary is expected to grow later.

The important property is that actions are explicit objects rather than implicit side effects.

---

## 5.4 Event

Events are immutable records representing simulation facts.

Examples:

```text
AgentJoined
ActionProposed
ActionSelected
MessagePublished
```

Events include:

- event ID;
- simulation timestamp;
- simulation step;
- event-specific data.

---

## 5.5 Event Log

The engine currently maintains an in-memory event log and can export it as JSONL.

Example:

```json
{"type":"agent.joined", ...}
{"type":"action.proposed", ...}
{"type":"action.selected", ...}
{"type":"message.published", ...}
```

JSONL is currently the simplest useful persistence format and is sufficient for the MVP.

A database is not required yet.

---

# 6. Simulation Time

The engine has a `SimulationClock`.

Simulation time must not depend on wall-clock time.

This is important for reproducibility.

Conceptually:

```text
step 0 → t = 0s
step 1 → t = 1s
step 2 → t = 2s
...
```

Real timestamps may still be added later for operational tracing, but simulation semantics should rely on the simulation clock.

## 6.1. Simulation Time and Silence

Simulation time is a first-class part of the simulation model.

A simulation step always advances simulation time, regardless of whether an agent performs an externally visible action.

This is intentional: periods of inactivity are meaningful social states and must be observable and measurable.

Example:

```text
t=0   agents enter the room

t=1   Alice speaks

t=2   silence

t=3   silence

t=4   silence

t=5   Bob speaks
```

They may represent:

- hesitation;
- lack of interest;
- uncertainty;
- social inhibition;
- waiting for others to act;
- increasing pressure to speak;
- fatigue;
- deliberation;
- deadlock.

The engine must therefore never equate:

```text
no action
```

with:

```text
no simulation progress
```

# 7. Reproducibility

Runs should be driven by an explicit configuration containing at least:

```text
run_id
seed
scenario configuration
```

Randomness must be scoped to the simulation run rather than relying on global random state.

The target property is:

```text
same configuration
+ same seed
+ same initial state
= same simulation trajectory
```

This is particularly important once stochastic scheduling and LLM-driven behavior are introduced.

Note that true LLM reproducibility may remain provider/model dependent. The engine should still make its own deterministic components reproducible.

---

# 8. LLM Abstraction

The `llm` package is currently only a placeholder.

The intended abstraction is approximately:

```python
class LLM(Protocol):
    async def generate(request: LLMRequest) -> LLMResponse:
        ...
```

The simulation engine should not directly depend on a specific provider.

Potential providers include:

```text
OpenAI
Anthropic
OpenRouter
Ollama
vLLM
mock/local deterministic implementation
```

The MVP should use a mock implementation first and add a real provider only after the simulation architecture is stable.

---

# 9. Memory Abstraction

Memory is also currently only a placeholder.

The intended boundary is:

```python
class MemoryStore(Protocol):
    async def add(...): ...
    async def search(...): ...
```

The engine should depend on this abstraction, not on a specific memory product.

Potential implementations may later include:

```text
in-memory
Postgres
vector store
Mem0
custom experimental memory
```

Memory is not required for the first simulation milestone.

---

# 10. Observability

The repository already contains local OpenTelemetry / Grafana infrastructure inherited from the Turborepo example.

This infrastructure is useful and will be retained, but its original Turborepo-specific dashboarding is no longer relevant.

The target architecture is:

```text
Engine
   │
   │ OpenTelemetry
   ▼
OTel Collector
   ├── metrics backend
   └── trace backend
```

The application itself should emit telemetry independently of whichever UI/backend is used to inspect it.

Observability should eventually cover:

```text
experiment
run
agent
room
scheduler
LLM call
memory operation
event
```

However, full tracing is not required for the first MVP.

---

# 11. UI

The UI is a separate Next.js application.

The purpose of the UI is primarily **inspection and experimentation**, rather than serving as the execution engine.

The first UI should expose:

```text
Experiment
    ↓
Run
    ↓
Timeline
    ↓
Event details
```

Later, the UI can evolve into a full simulation workspace with:

- room visualization;
- agent inspector;
- memory inspection;
- state inspection;
- scheduler visualization;
- replay controls;
- experiment configuration;
- run comparison.

The MVP should avoid building this entire interface up front.

---

# 12. Scenario Configuration

Experiments should eventually be declarative.

Example:

```yaml
name: basic-consensus

seed: 42

agents:
  - id: alice
    behavior: talkative

  - id: bob
    behavior: quiet

  - id: charlie
    behavior: reactive

rooms:
  - id: main
    members:
      - alice
      - bob
      - charlie

scheduler:
  type: weighted_random

steps: 20
```

The exact schema is not frozen yet.

The important principle is that an experiment should be defined independently of the UI and runnable from the command line.

---

# 13. MVP Definition

The MVP is intentionally much smaller than the long-term vision.

## MVP goal

Demonstrate a complete experimental loop:

```text
scenario
   ↓
simulation
   ↓
agents propose actions
   ↓
scheduler selects
   ↓
events recorded
   ↓
run exported
   ↓
UI displays and replays run
```

## MVP requirements

### Engine

- deterministic simulation clock;
- deterministic random seed;
- `Agent`;
- `Room`;
- `Action`;
- `Event`;
- `EventLog`;
- `Simulation`;
- at least two scheduler implementations;
- mock agents;
- JSONL run export.

### CLI

A scenario should be runnable with a command such as:

```bash
uv run experiments run scenarios/basic.yaml
```

The command should produce an identifiable run artifact.

### UI

The UI should be able to:

1. list runs;
2. open a run;
3. display its event timeline;
4. inspect an individual event;
5. replay a run step by step.

### No database requirement

The MVP can use filesystem-based run artifacts:

```text
runs/
└── <run-id>/
    ├── config.json
    └── events.jsonl
```

---

# 14. MVP Roadmap

## Phase 0 — Current foundation

Status: **in progress / mostly complete**

Already implemented:

- Python engine package;
- agents;
- rooms;
- actions;
- events;
- event log;
- JSONL export;
- simulation clock;
- basic scheduler;
- deterministic RNG foundation.

---

## Phase 1 — Stabilize the engine

Goal:

> Make the current simulation model clean, deterministic, and testable.

Tasks:

- finalize event model;
- finalize simulation clock;
- finalize run configuration;
- add unit tests for core objects;
- add deterministic run tests;
- clean up package boundaries;
- improve CLI output.

Deliverable:

```text
same scenario + same seed
→ identical event sequence
```

---

## Phase 2 — Minimal experimentation layer

Goal:

> Make experiments configurable without modifying Python code.

Tasks:

- introduce scenario schema;
- load YAML/JSON configuration;
- define agents through configuration;
- define rooms through configuration;
- select scheduler through configuration;
- write run metadata alongside events.

Deliverable:

```bash
uv run experiments run scenarios/basic.yaml
```

---

## Phase 3 — First UI

Goal:

> Make a run inspectable without reading JSONL manually.

Tasks:

- basic API layer;
- run listing;
- run detail endpoint;
- event timeline;
- event inspector;
- step-through replay.

Deliverable:

```text
Run #42
────────────────────────
00  agent.joined
01  agent.joined
02  action.proposed
03  action.selected
04  message.published
...
```

---

## Phase 4 — Real LLM integration

Goal:

> Replace mock agent policies with real model-backed policies.

Tasks:

- implement LLM abstraction;
- add one provider;
- implement prompt/request tracing;
- make model configuration declarative;
- preserve mock provider for tests.

Deliverable:

```text
Agent
  ↓
LLM
  ↓
structured action proposal
  ↓
scheduler
```

The first LLM integration should deliberately be simple.

---

## Phase 5 — Conversation experiments

Goal:

> Test the central hypothesis that interaction should not be constrained by round-robin turns.

Introduce:

- speaker selection policies;
- selective participation;
- silence;
- repeated speakers;
- basic interruption;
- configurable communication policies.

The MVP does not need sophisticated “emergent conversation”.

The first useful comparison is simply:

```text
RoundRobin
vs
PolicyBased
```

with measurable differences in the resulting event stream.

---

## Phase 6 — Observability

Goal:

> Make a run deeply inspectable.

Add OpenTelemetry instrumentation around:

```text
simulation step
agent execution
scheduler execution
LLM call
memory access
event creation
```

Expose metrics such as:

```text
event count
agent activity
scheduler latency
LLM latency
token usage
cost
```

---

## Phase 7 — Memory and richer interaction spaces

Only after the previous layers are stable:

- persistent memory;
- private rooms;
- selective visibility;
- agent isolation;
- shared artifacts;
- agent movement;
- richer state inspection.

---

# 15. Post-MVP Architecture

The longer-term architecture can evolve toward:

```text
                        experiments UI
                              │
                         API / stream
                              │
                              ▼
                     Simulation Engine
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
         World              Agents            Scheduler
          │                   │                   │
        Rooms              Memory              Policies
                              │
                             LLM
                              │
                         Event Stream
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
       Run Store          Telemetry             Analysis
          │                   │
          ▼                   ▼
       Replay              Grafana/etc.
```

At this stage, persistence, distributed execution, workflow orchestration, and sophisticated observability can be introduced based on actual requirements rather than assumptions.

---

# 16. Explicit Non-Goals for the MVP

The following should **not** be treated as MVP requirements:

- Temporal;
- Redis;
- Postgres;
- Phoenix;
- Mem0;
- distributed workers;
- multi-node simulation;
- sophisticated cognitive architectures;
- autonomous room creation;
- coalition formation;
- advanced interruption models;
- complex agent memory;
- production deployment;
- complete observability platform.

These remain possible future extensions.

---

# 17. Success Criteria

The MVP is successful when the following workflow is possible:

```text
1. Create a scenario.
2. Run it with a seed.
3. Produce a run artifact.
4. Open the run in the UI.
5. Inspect the complete event timeline.
6. Replay the run.
7. Change one experimental parameter.
8. Run it again.
9. Compare the two trajectories.
```

The system should make this workflow easier than manually stitching together prompts and scripts.

---

# 18. Guiding Principle

`experiments` should optimize for **experimental freedom**, not framework completeness.

The architecture should therefore remain:

- small;
- explicit;
- deterministic where possible;
- event-oriented;
- provider-independent;
- easy to inspect;
- easy to modify.

Complexity should be introduced only when an experiment demonstrates that the simpler model is insufficient.
