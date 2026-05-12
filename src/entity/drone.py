from __future__ import annotations
from .entity import Entity
from .map_entities import Hub, Edge
from typing import List, Set
from collections import deque
import sys


class Node:
    def __init__(self, hub: Hub, prev: Node) -> None:
        self._hub = hub
        self._prev = prev

    def get_path(self) -> List[Hub]:
        path: List[Hub] = [self._hub]
        node = self._prev
        while node:
            path.append(node._hub)
            node = node._prev
        return path[::-1]

    @property
    def hub(self) -> Hub:
        return self._hub


class Drone(Entity):
    next_id = 1

    def __init__(self, x: int, y: int, hub: Hub) -> None:
        """Initialize a drone entity."""
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
        self._reserved_hub = None

    def _create_temp_hub(self, next_hub: Hub) -> Hub:
        """
        Create a temporary hub to store the position of the middle between hubs.
        """
        x, y = self._hub.pos
        nx, ny = next_hub.pos
        half_x = (nx - x) * 50 / 100 + x
        half_y = (ny - y) * 50 / 100 + y
        temp_hub = Hub(f"{self._hub.name}/{next_hub.name}", half_x, half_y)
        edge = Edge(temp_hub, next_hub)
        temp_hub.add_edge(edge)
        return temp_hub

    def _fly_to_hub(self, next_hub: Hub, future = None) -> None:
        already_landed = False
        self._og_x, self._og_y = self._hub.pos
        if next_hub.zone == "restricted":
            if not self._reserved_hub and (next_hub.has_capacity() or next_hub.available):
                next_hub.land_on()
                if next_hub.available:
                    print("done")
                    next_hub.available = False
                next_hub.is_reserved = True
                self._reserved_hub = next_hub
                next_hub = self._create_temp_hub(next_hub)
            else:
                self._reserved_hub = None
                next_hub.is_reserved = False
                already_landed = True
                if future and future(next_hub):
                    next_hub.available = True
                    print("will")
        self._next_x, self._next_y = next_hub.pos
        self._hub.take_off()
        self._hub = next_hub
        if not already_landed:
            next_hub.land_on()
        self._progress += 1
        print(f"D{self._id}-{next_hub.name}", end=" ")

    def _find_path(self) -> List[Hub]:
        def get_neighbors(node: Node):
            edges = sorted(node._hub.edges)
            return [Node(edge.hubs[1], node) for edge in edges]

        visited: Set[Hub] = set()
        start = Node(self._hub, None)

        queue = deque(get_neighbors(start))

        if start.hub.hub_type == "end_hub":
            return []

        while queue:
            node = queue.popleft()

            if node.hub in visited or node.hub.zone == "blocked":
                continue

            if node.hub.hub_type == "end_hub":
                return node.get_path()

            visited.add(node.hub)
            queue.extend(get_neighbors(node))

        if node.hub.hub_type != "end_hub":
            sys.exit("Unsolvable map!")

        return []

    def next_move(self, future) -> None:
        hubs = self._find_path()
        #print(self._id, [h.name for h in hubs])

        if len(hubs) < 1:
            return

        next_hub = hubs[1]

        if not next_hub.has_capacity() and not self._reserved_hub and not next_hub.available:
            return

        if next_hub.zone == "restricted":
            if next_hub.is_reserved or next_hub.available:
                if self._reserved_hub == next_hub or next_hub.available:
                    self._fly_to_hub(next_hub, future)
                    return

        try:
            self._fly_to_hub(next_hub)
        except ValueError as e:
            print(e)

    def update(self) -> None:
        """Update the drone position."""
        if self._progress > 0:
            self._progress += self._speed * 0.7
            x = (self._next_x - self._og_x) * self._progress / 100 + self._og_x
            y = (self._next_y - self._og_y) * self._progress / 100 + self._og_y
            self.pos = (x, y)
            if self._progress >= 100:
                self._progress = 0
                self.pos = self._hub.pos

    @property
    def progress(self) -> float:
        return self._progress
