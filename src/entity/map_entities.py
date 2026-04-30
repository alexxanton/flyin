from __future__ import annotations
from .entity import Entity
from typing import List, Tuple


class Edge:
    def __init__(
        self, from_hub: Hub, to_hub: Hub, max_link_capacity: int = 1
    ) -> None:
        self._max_link_capacity = max_link_capacity
        self._from_hub = from_hub
        self._to_hub = to_hub

    @property
    def hubs(self) -> Tuple[Hub, Hub]:
        return (self._from_hub, self._to_hub)

    @property
    def flipped(self) -> Edge:
        return Edge(self._to_hub, self._from_hub, self._max_link_capacity)

    def __lt__(self, other: Edge) -> bool:
        values = {
            "priority": 0,
            "normal": 1,
            "restricted": 2,
            "blocked": 3
        }
        return values[self._to_hub.zone] < values[other._to_hub.zone]


class Hub(Entity):
    """Represents a hub for the drones where they have to travel to."""
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone: str = "normal",
        color: str = "none",
        max_drones: int = 1
    ) -> None:
        super().__init__(x, y)
        self._name = name
        self._edges: List[Edge] = []
        self._drones_landed = 0
        self._zone = zone
        self._color = color
        self._max_drones = max_drones
        self._reserved = False

    @property
    def color(self) -> str:
        return self._color

    @property
    def name(self) -> str:
        return self._name

    @property
    def zone(self) -> str:
        return self._zone

    @property
    def max_drones(self) -> int:
        return self._max_drones

    @property
    def edges(self) -> List[Edge]:
        return self._edges

    @property
    def reserved(self) -> bool:
        return self._reserved

    @reserved.setter
    def reserved(self, b: bool) -> None:
        self._reserved = b

    def add_edge(self, edge: Edge) -> None:
        self._edges.append(edge)

    def take_off(self) -> None:
        if self._drones_landed <= 0:
            raise ValueError("Can't take off if there are no drones")
        self._drones_landed -= 1

    def land_on(self) -> None:
        if self._drones_landed >= self._max_drones:
            raise ValueError("Max drone capacity exceeded")
        self._drones_landed += 1

    def has_capacity(self) -> bool:
        return self._drones_landed < self._max_drones
