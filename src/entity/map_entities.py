from __future__ import annotations
from .entity import Entity
from typing import List, Tuple


class Edge:
    """Represents a connection between two hubs."""
    def __init__(
        self, from_hub: Hub, to_hub: Hub, max_link_capacity: int = 1
    ) -> None:
        """Initialize an edge entity."""
        self._max_link_capacity = max_link_capacity
        self._from_hub = from_hub
        self._to_hub = to_hub
        self._drones = 0

    @property
    def hubs(self) -> Tuple[Hub, Hub]:
        """Returns the edge hubs."""
        return (self._from_hub, self._to_hub)

    @property
    def flipped(self) -> Edge:
        """Returns the edge but reversed."""
        return Edge(self._to_hub, self._from_hub, self._max_link_capacity)

    @property
    def drones(self) -> int:
        """Returns the drones traveling within the edge."""
        return self._drones

    @drones.setter
    def drones(self, value: int) -> None:
        """Setter for drones."""
        self._drones = value

    def has_capacity(self) -> bool:
        """Returns if the edge has capacity."""
        return self._drones < self._max_link_capacity

    def __lt__(self, other: Edge) -> bool:
        """Defines how to interpret the `less than` operator."""
        values = {
            "priority": 0,
            "normal": 1,
            "restricted": 2,
            "blocked": 3
        }
        value = values[self._to_hub.zone] - (self._to_hub._drones_landed == 0)
        value -= self.has_capacity() * 2
        return value < values[other._to_hub.zone]


class Hub(Entity):
    """Represents a hub for the drones to travel to."""
    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        hub_type: str = "normal",
        zone: str = "normal",
        color: str = "none",
        max_drones: int = 1
    ) -> None:
        """Initialize a hub entity."""
        super().__init__(x, y)
        self._name = name
        self._edges: List[Edge] = []
        self._drones_landed = 0
        self._zone = zone
        self._color = color
        self._max_drones = max_drones
        self._is_reserved = False
        self._hub_type = hub_type
        self._available = False
        self._extra_capacity = 0

    @property
    def color(self) -> str:
        """Returns the hub color."""
        return self._color

    @property
    def name(self) -> str:
        """Returns the hub name."""
        return self._name

    @property
    def zone(self) -> str:
        """Returns the hub zone."""
        return self._zone

    @property
    def drones_landed(self) -> int:
        """Returns the quantity of drones landed on a hub."""
        return self._drones_landed - self._extra_capacity

    @property
    def max_drones(self) -> int:
        """Returns the hub capacity."""
        return self._max_drones

    @property
    def edges(self) -> List[Edge]:
        """Returns the hub edges."""
        return self._edges

    @property
    def hub_type(self) -> str:
        """Returns the hub type."""
        return self._hub_type

    @property
    def is_reserved(self) -> bool:
        """Returns if the hub is reserved."""
        return self._is_reserved

    @is_reserved.setter
    def is_reserved(self, b: bool) -> None:
        """Setter for is_reserved."""
        self._is_reserved = b

    @property
    def extra_capacity(self) -> int:
        """Returns the hub extra capacity."""
        return self._extra_capacity

    @extra_capacity.setter
    def extra_capacity(self, value: int) -> None:
        """Setter for extra_capacity."""
        self._extra_capacity = value

    @property
    def available(self) -> bool:
        """Returns the hub availability."""
        return self._available

    @available.setter
    def available(self, value: bool) -> None:
        """Setter for available."""
        self._available = value

    def add_edge(self, edge: Edge) -> None:
        """Add an edge to a hub."""
        self._edges.append(edge)

    def take_off(self) -> None:
        """Represents a drone taking off from a hub."""
        if self._drones_landed <= 0:
            raise ValueError(
                f"{self._name}: Can't take off if there are no drones"
            )
        self._drones_landed -= 1

    def land_on(self) -> None:
        """Represents a drone landing on a hub."""
        if self._drones_landed >= (self._max_drones + self._extra_capacity):
            raise ValueError(f"{self._name}: Max drone capacity exceeded")
        self._drones_landed += 1

    def has_capacity(self) -> bool:
        """Returns if the hub has capacity."""
        return self._drones_landed < (self._max_drones + self._extra_capacity)
