from __future__ import annotations
from .drone import Drone
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
        self._name: str = name
        self._edges: List[Edge] = []
        self._drones: List[Drone] = []
        self._zone: str = zone
        self._color: str = color
        self._max_drones: int = max_drones

    @property
    def color(self) -> str:
        return self._color

    @property
    def name(self) -> str:
        return self._name
