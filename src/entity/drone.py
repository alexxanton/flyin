from __future__ import annotations
from .entity import Entity
from .map_entities import Hub, Edge
from typing import List
from typing import TYPE_CHECKING


class Node:
    def __init__(self, prev: Node) -> None:
        self._prev = prev


class Drone(Entity):
    next_id = 1

    def __init__(self, x: int, y: int, hub: Hub) -> None:
        super().__init__(x, y)
        self._id = Drone.next_id
        Drone.next_id += 1
        self._hub = hub
        self._progress = 0
        self._hub.land_on()
        self._og_x = x
        self._og_y = y
        self._next_x = x
        self._next_y = y
        self._speed = 2
        self._reserved = None

    def _create_temp_hub(self, next_hub: Hub) -> Hub:
        self._reserved = next_hub
        x, y = self._hub.pos
        nx, ny = next_hub.pos
        half_x = (nx - x) * 50 / 100 + x
        half_y = (ny - y) * 50 / 100 + y
        temp_hub = Hub(f"{self._hub.name}/{next_hub.name}", half_x, half_y)
        edge = Edge(temp_hub, next_hub)
        temp_hub.add_edge(edge)
        return temp_hub

    def _fly_to_hub(self, next_hub: Hub) -> None:
        self._og_x, self._og_y = self._hub.pos
        #self._speed = 1 if next_hub.zone == "restricted" else 2
        if next_hub.zone == "restricted":
            if not self._reserved:
                next_hub.reserved = True
                next_hub = self._create_temp_hub(next_hub)
            else:
                self._reserved = None
                next_hub.reserved = False
        self._next_x, self._next_y = next_hub.pos
        self._hub.take_off()
        self._hub = next_hub
        next_hub.land_on()
        self._progress += 1
        print(f"D{self._id}-{next_hub.name}", end=" ")

    def _find_path(self) -> List[Hub]:
        def get_neighbors(hub: Hub) -> List[Hub]:
            edges: List[Edge] = sorted(hub.edges)
            nodes = [edge.hubs[1] for edge in edges]

        nodes: List[Hub] = get_neighbors(self._hub.edges)
        while nodes:
            node = nodes.pop(0)

            if node not in visited:
                nodes += get_neighbors(node)

            visited.append(node)

    def next_move(self) -> None:
        for edge in sorted(self._hub.edges):
            next_hub = edge.hubs[1]

            if next_hub.has_capacity() or next_hub.zone == "restricted":
                if next_hub.zone == "restricted" and next_hub.reserved:
                    if not self._reserved == next_hub:
                        continue
                self._fly_to_hub(next_hub)
                break

    def update(self) -> None:
        if self._progress > 0:
            self._progress += self._speed * 0.7
            x = (self._next_x - self._og_x) * self._progress / 100 + self._og_x
            y = (self._next_y - self._og_y) * self._progress / 100 + self._og_y
            self.pos = (x, y)
            if self._progress >= 100:
                self._progress = 0
                self.pos = self._hub.pos
