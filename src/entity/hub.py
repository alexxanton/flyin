from __future__ import annotations
from typing import List
from .entity import Entity
from .drone import Drone


class Hub(Entity):
    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__(x, y)
        self._name: str = name
        self._connected_from: List[Hub] = []
        self._connected_to: List[Hub] = []
        self._drones: List[Drone] = []
