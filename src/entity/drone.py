from __future__ import annotations
from .entity import Entity
from .map_entities import Hub, Edge
from typing import List, Set, Optional
from collections import deque
import sys


class Node:
    """Node point for the pathfinding algorithm."""
    def __init__(self, hub: Hub, prev: Optional[Node]) -> None:
        """Initialize a node entity."""
        self._hub = hub
        self._prev = prev

    def get_path(self) -> List[Hub]:
        """Get the path leading to the first node and reverse it."""
        path: List[Hub] = [self._hub]
        node = self._prev
        while node:
            path.append(node._hub)
            node = node._prev
        return path[::-1]

    @property
    def hub(self) -> Hub:
        """Returns the hub associated with a node."""
        return self._hub


class Drone(Entity):
    """Drone entity with pathfinding capabilities."""
    next_id = 1

    def __init__(self, x: float, y: float, hub: Hub) -> None:
        """Initialize a drone entity."""
        super().__init__(x, y)
        self._id = Drone.next_id
        Drone.next_id += 1
        self._hub = hub
        self._progress = 0.0
        self._hub.land_on()
        self._og_x = x
        self._og_y = y
        self._next_x = x
        self._next_y = y
        self._speed = 2
        self._reserved_hub: Optional[Hub] = None
        self._copy = False

    def _create_temp_hub(self, next_hub: Hub) -> Hub:
        """
        Create a temporary hub to store the middle position between hubs.
        """
        x, y = self._hub.pos
        nx, ny = next_hub.pos
        half_x = (nx - x) * 50 / 100 + x
        half_y = (ny - y) * 50 / 100 + y
        temp_hub = Hub(f"{self._hub.name}/{next_hub.name}", half_x, half_y)
        edge = Edge(temp_hub, next_hub)
        temp_hub.add_edge(edge)
        return temp_hub

    def _fly_to_hub(self, next_hub: Hub, future=None) -> None:
        """Travel to the next hub."""
        already_landed = False
        self._og_x, self._og_y = self._hub.pos
        if next_hub.zone == "restricted":
            if (
                not self._reserved_hub
                and (next_hub.has_capacity() or next_hub.available)
            ):
                if next_hub.available and not next_hub.has_capacity():
                    next_hub.available = False
                    if not next_hub.has_capacity():
                        next_hub.extra_capacity += 1
                next_hub.land_on()
                next_hub.is_reserved = True
                self._reserved_hub = next_hub
                next_hub = self._create_temp_hub(next_hub)
            else:
                self._reserved_hub = None
                next_hub.is_reserved = False
                already_landed = True
                next_hub.available = False
                if future and future(self, next_hub):
                    next_hub.available = True
        self._next_x, self._next_y = next_hub.pos
        self._hub.take_off()
        if self._hub.extra_capacity > 0 and not self._reserved_hub:
            self._hub.extra_capacity -= 1
        self._hub = next_hub
        if not already_landed:
            next_hub.land_on()
        self._progress += 1
        if not self._copy:
            print(f"D{self._id}-{next_hub.name}", end=" ")

    def _find_path(self) -> List[Hub]:
        """Execute the pathfinding algorithm."""
        def get_neighbors(node: Node) -> List[Node]:
            """Get hubs that connect with the current hub."""
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
        """Execute the next move whether it has to move or wait."""
        hubs = self._find_path()

        if len(hubs) < 1:
            return

        next_hub = hubs[1]

        if (
            not next_hub.has_capacity()
            and not self._reserved_hub
            and not next_hub.available
        ):
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
        """Returns the progress of the trajectory between two hubs."""
        return self._progress

    @property
    def id(self) -> int:
        """Returns the drone ID."""
        return self._id

    @property
    def hub(self) -> Hub:
        """Returns the hub where the drone is positioned at."""
        return self._hub
