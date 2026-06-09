_This project has been created as part of the 42 curriculum by aanton-a._

# Fly-in: Multi-Drone Network Routing Simulator

---

## Description

**Fly-in** is a turn-based simulation network router designed to navigate multiple drones from a starting hub to an end goal in the fewest possible turns. The project uses a complex network topology where zones have differing movement costs, capacities, and connection bandwidth constraints.

* **Goal:** Maximize throughput and minimize total simulation turns while strictly preventing deadlocks, routing collisions, or zone/link capacity overruns.
* **Overview:** The program parses a structural map file defining drone counts, node coordinates, zone properties (e.g., `priority`, `restricted`, `blocked`), and bidirectional connections. It then executes a turn-by-turn simulation, rendering the real-time movement of the drones.

---

### Features

* **Map Parser:** Validates map data syntax, coordinates, rules, and handles metadata.
* **Capacity-Aware Pathfinding:** Accounts for overlapping nodes and changes routes based on `max_drones` and `max_link_capacity`.
* **Multi-Turn Restricted Travel:** Accurately routes drones into 2-turn `restricted` transit states where they stay in flight on connection edges.
* **Conflict & Collision Prevention:** Prevents node over-allocation by checking what routes are less congested.

---

## Instructions

### Prerequisites

* Python 3.10+
* Linux / macOS
* `make` utility

### Installation

Install project dependencies (`flake8`, `mypy`, `lark` and `pygame`) with make:

```bash
make install

```

### Execution

To run the main simulation with a map file:

```bash
# General Usage
make run

# Specific Usage
python3 main.py <path_to_map_file>

# Or open a map menu
make maps

```

### Debugging & Quality Control

To invoke the built-in Python interactive debugger (`pdb`) or verify type safety and style constraints:

```bash
# Debug Mode
make debug

# Linting Checks (Flake8 & Mypy strict type checking)
make lint

```

### Cleaning Up

Remove temporary `__pycache__` directories and linting caches:

```bash
make clean

```

---

## Algorithm Choices & Implementation Strategy

* **Path Finding:** A modified `BFS` algorithm was implemented to discover all valid paths, tracking travel costs where `priority` zones = 1 turn, `restricted` zones = 2 turns, and `blocked` nodes are discarded instantly.
* **Scheduling & Traffic Control:** To resolve capacity constraints, drones evaluate what paths are less congested by checking what hubs have capacity for more drones. This allows simultaneous moves and lets drones strategically wait in place if paths are saturated.
* **Scheduling**: Drones decide to wait by comparing different routes and validating if by waiting the end goal will be reached earlier.

---
## Simulation Output Format

The program outputs step-by-step turn movements:

* Each line represents a turn.
* Drones matching a destination are outputted as `D<id>-<zone>`.
* Drones transit-bound to restricted zones are outputted as `D<id>-<connection>`.

```text
Turn 1: D1-roof1 D2-corridorA
Turn 2: D1-roof2 D2-tunnelB
Turn 3: D1-goal D2-goal
```

## Visual Representation

To enhance understanding of dense networks and multi-turn schedules, this implementation provides user-friendly visual feedback with `pygame`:

* **Graphical UI:** An interface with a map selection menu was implemented to easily select different maps.
* **Responsive Design:** The visual representation of the nodes and its connections always stays proportional to the window sizes.
* **Colorful Planets:** The hubs are represented as little planets with different shapes and colors to clearly represent what type of zone they are.

---

## Resources

### References & Documentation

* [Lark Documentation](https://lark-parser.readthedocs.io/en/stable/)
* [Pygame Documentation](https://www.pygame.org/docs/)

### AI Use Disclosure

In accordance with the 42 curriculum standards, AI tools were used during development for the following specific tasks:

| Task / Project Part | How AI Was Used |
| --- | --- |
| **Type Linting Verification** | Assisted in writing strict type signatures for abstract matrix structures to clear complex `mypy --strict` errors. |
| **Edge Case Testing** | Used to generate synthetic custom map configurations to test mathematical corner cases. |

> **Note:** All algorithmic routing logic, scheduling loops, and constraint evaluation hooks were written manually. No core logic was copy-pasted, satisfying the pedagogical standards of the 42 peer-evaluation system.

