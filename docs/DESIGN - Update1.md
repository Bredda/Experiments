# experiments — Technical Design Update

## 1. Simulation Time and Silence

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

The three silent steps between Alice and Bob are part of the simulation trajectory.

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

---

## 2. Two Distinct Time Domains

The system distinguishes between **simulation time** and **wall-clock execution time**.

### Simulation time

Simulation time is controlled by `SimulationClock`.

It represents the temporal progression experienced by agents and the simulated environment.

```text
step 0 → t=0s
step 1 → t=1s
step 2 → t=2s
...
```

Simulation time is deterministic and independent from the machine clock.

### Wall-clock time

Wall-clock time represents the actual execution cost of the experiment.

Examples:

```text
LLM call       1.8s
Memory lookup  0.03s
Scheduler      0.001s
```

Wall-clock timing belongs to observability and performance analysis, not simulation semantics.

The two must never be conflated.

---

## 3. Simulation Step

A simulation step represents one unit of simulated time.

Conceptually:

```text
current state
    ↓
agents observe
    ↓
agents propose actions or remain silent
    ↓
scheduler evaluates available actions
    ↓
selected action may be executed
    ↓
events are recorded
    ↓
simulation time advances
```

If no action is selected:

```text
current state
    ↓
agents remain silent / no executable action
    ↓
time advances
    ↓
new state
```

This allows arbitrary periods of simulated inactivity.

---

## 4. Silence

Silence is a meaningful state rather than the absence of simulation.

An agent may explicitly choose:

```text
StaySilent
```

and the room may experience a step where no agent speaks.

This distinction is important:

```text
Agent silence
    An agent intentionally does not speak.

Room silence
    No message is produced during a simulation step.
```

A room may therefore have:

```text
3 agents
3 observations
3 silent decisions
0 published messages
1 tick
```

This is a valid and meaningful simulation outcome.

---

## 5. Time Advancement Events

The event model should distinguish between behavioral events and the passage of simulation time.

A future event stream may therefore look like:

```text
step 0
  agent.joined Alice
  agent.joined Bob
  agent.joined Charlie

step 1
  action.proposed Alice → Speak
  action.proposed Bob → Speak
  action.proposed Charlie → Speak
  action.selected Alice
  message.published Alice
  simulation.tick

step 2
  action.proposed Alice → StaySilent
  action.proposed Bob → StaySilent
  action.proposed Charlie → StaySilent
  simulation.tick

step 3
  action.proposed Alice → StaySilent
  action.proposed Bob → StaySilent
  action.proposed Charlie → StaySilent
  simulation.tick
```

Whether `simulation.tick` becomes an explicit persisted event or remains a derived property of the event stream is an implementation detail that can be decided later.

The semantic requirement is fixed:

> Every simulation step advances time and must be recoverable from the run history.

---

## 6. Why Time Matters Experimentally

The system should make temporal dynamics observable.

Potential measurements include:

```text
silence duration
time to first intervention
time to response
time between interventions
agent speaking frequency
agent waiting time
interruption latency
response latency
```

These measurements may later become inputs to agent policies or scheduler policies.

For example:

```text
silence duration = 0
    willingness to speak = low

silence duration = 5
    willingness to speak = higher

silence duration = 15
    willingness to speak = very high
```

The engine itself should not prescribe this behavior.

It only provides the temporal state required for such behaviors to be implemented and studied.

---

## 7. Reproducibility

A run is reproducible when the same:

```text
scenario configuration
+ initial state
+ seed
```

produce the same simulation trajectory.

Simulation time must therefore be independent of wall-clock time.

LLM calls may introduce provider-dependent non-determinism. The engine must nevertheless keep deterministic control over:

- simulation time;
- random choices;
- scheduling;
- state transitions;
- event ordering.

---

## 8. Revised Simulation Contract

The core simulation contract is therefore:

```text
observe
   ↓
propose
   ↓
arbitrate
   ↓
execute or remain inactive
   ↓
record events
   ↓
advance simulation time
```

Importantly:

> **Time advances even when nothing happens externally.**

This is a core property of the simulation model, not an implementation convenience.
