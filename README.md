_This project has been created as part of the 42 curriculum by aanton-a._

# Fly-in: Multi-Drone Network Routing Simulator

---

## Description

**Fly-in** is a discrete, turn-based simulation network router designed to navigate multiple drones from a starting hub to an end goal in the fewest possible turns. The project models a complex network topology where zones have differing movement costs, capacities, and connection bandwidth constraints.

* **Goal:** Maximize throughput and minimize total simulation turns while strictly preventing deadlocks, routing collisions, or zone/link capacity overruns.
* **Overview:** The program parses a structural map file defining drone counts, node coordinates, zone properties (e.g., `priority`, `restricted`, `blocked`), and bidirectional connections. It then calculates simultaneous paths and executes a turn-by-turn simulation loop, rendering the real-time movement of the drones.

---

## Features

* **Deterministic Map Parser:** Fully validates map data syntax, coordinates, single source/sink rules, and handles explicit/default metadata brackets.
* **Capacity-Aware Pathfinding:** Accounts for overlapping nodes and throttles routes based on `max_drones` and `max_link_capacity`.
* **Multi-Turn Restricted Travel:** Accurately routes drones into 2-turn `restricted` transit states where they sit "in flight" on connection edges.
* **Conflict & Collision Prevention:** Prevents node over-allocation by utilizing transactional capacity release (drones exiting a zone free up space for incoming drones on the exact same turn).

---

## Instructions

### Prerequisites

* Python 3.10+
* Linux / macOS
* `make` utility

### Installation

Install project dependencies (such as `flake8`, `mypy`, or any visual rendering libraries) via the package manager of your choice using our configured Makefile automation:

```bash
make install

```

### Execution

To run the main simulation with a map file:

```bash
# General Usage
python3 main.py <path_to_map_file>

# Or via Makefile wrapper
make run MAP=<path_to_map_file>

```

### Debugging & Quality Control

To invoke the built-in Python interactive debugger (`pdb`) or verify type safety and style constraints:

```bash
# Debug Mode
make debug MAP=<path_to_map_file>

# Linting Checks (Flake8 & Mypy strict type checking)
make lint
make lint-strict

```

### Cleaning Up

Remove temporary `__pycache__` directories and linting caches:

```bash
make clean

```

---

## Simulation Output Format

The program outputs step-by-step turn movements matching the 42 specifications:

* Each line represents a discrete turn.
* Drones matching a destination are outputted as `D<id>-<zone>`.
* Drones transit-bound to restricted zones are outputted as `D<id>-<connection>`.

```text
Turn 1: D1-roof1 D2-corridorA
Turn 2: D1-roof2 D2-tunnelB
Turn 3: D1-goal D2-goal

```

---

## Algorithm Choices & Implementation Strategy

*(Note to Learner: Customize this section to reflect your actual algorithm code during your project defense.)*

* **Path Generation:** [e.g., We implemented a modified BFS / Dijkstra's algorithm / A* Search to discover all valid spatial paths, tracking travel costs where `priority` zones = 1 turn, `restricted` zones = 2 turns, and `blocked` nodes are pruned instantly.]
* **Scheduling & Traffic Control:** [e.g., To resolve capacity constraints, a reservation table/token bucket mechanism tracks zone occupancy over discrete time turns $T, T+1, T+2$... This allows simultaneous moves and lets drones strategically "wait in place" if paths are saturated.]
* **Time & Space Complexity:** * Pathfinding: $\mathcal{O}(V + E \log V)$
* **Scheduling**: $\mathcal{O}(D \cdot P \cdot T)$ where $D$ is the number of drones and $P$ is path length.

* **Optimization:** [e.g., Paths are cached at boot, and dynamic reallocation triggers only when a structural deadlock is predicted.]

---

## Visual Representation

To enhance understanding of dense networks and multi-turn schedules, this implementation provides user-friendly visual feedback via:

* **Colored Terminal Output:** Utilizing ANSI escape codes, zones are highlighted dynamically to show stress levels (e.g., **Red** for maxed capacity, **Green** for priority lanes, and **Yellow flashing indicators** for drones traveling mid-transit inside restricted connections).
* **[Optional Graphical UI]:** [If you built a Tkinter/Pygame/Custom UI, describe how it animates nodes, displays real-time capacity fractions, and visualizes drone delivery progress.]

---

## Performance Benchmarks

Our implementation targets and tracks performance against the curriculum records:

| Map Difficulty | Subject Target | Our Results | Status |
| --- | --- | --- | --- |
| **Easy Maps** (Simple Fork / Basic Cap) | $\le 6 \text{ -- } 8$ Turns | `X` Turns | [Passed/Optimal] |
| **Medium Maps** (Dead End / Loop Puzzle) | $\le 12 \text{ -- } 15$ Turns | `X` Turns | [Passed/Optimal] |
| **Hard Maps** (Maze / Capacity Hell) | $\le 30 \text{ -- } 35$ Turns | `X` Turns | [Passed/Optimal] |
| **Challenger Map** (The Impossible Dream) | Reference: $45$ Turns | `X` Turns | [Attempted/Beaten] |

---

## Resources

### References & Documentation

* [Python Built-In Debugger (pdb) Documentation](https://docs.python.org/3/library/pdb.html)
* [Mypy Static Typing Documentation](https://mypy.readthedocs.io/)
* [Network Routing & Flow Optimization Algorithms](https://en.wikipedia.org/wiki/Flow_network)

### AI Use Disclosure

In accordance with the 42 curriculum standards, AI tools were leveraged during development for the following specific engineering tasks:

| Task / Project Part | How AI Was Used |
| --- | --- |
| **Parser Architecture** | Generated regular expressions to safely isolate the optional bracketed metadata elements `[...]` without splitting inner key/value pairs. |
| **Type Linting Verification** | Assisted in writing strict type signatures for abstract matrix structures to clear complex `mypy --strict` errors. |
| **Edge Case Brainstorming** | Used to generate synthetic custom map configurations to test mathematical corner cases (e.g., simultaneous entrance limits). |

> **Note:** All algorithmic routing logic, scheduling loops, and constraint evaluation hooks were written manually. No core logic was copy-pasted, satisfying the pedagogical standards of the 42 peer-evaluation system.

