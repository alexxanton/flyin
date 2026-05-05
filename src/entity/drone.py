from __future__ import annotations
from .entity import Entity
from .map_entities import Hub, Edge
from typing import List


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
        self._reserved = None

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

    def _fly_to_hub(self, next_hub: Hub) -> None:
        self._og_x, self._og_y = self._hub.pos
        if next_hub.zone == "restricted":
            if not self._reserved:
                next_hub.reserved = True
                self._reserved = next_hub
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

    def _find_path(self) -> List[Node]:
        def get_neighbors(node: Node) -> List[Node]:
            edges: List[Edge] = sorted(node._hub.edges)
            nodes = [Node(edge.hubs[1], node) for edge in edges]
            return nodes

        visited = []
        start = Node(self._hub, None)
        nodes: List[Node] = get_neighbors(start)
        while nodes:
            node = nodes.pop(0)

            if node not in visited:
                nodes += get_neighbors(node)

            if node._hub.hub_type == "end_hub":
                return node.get_path()

            visited.append(node)

        return []

    def next_move(self) -> None:
        hubs = self._find_path()
        #print(self._id, [h.name for h in hubs])

        if len(hubs) < 1:
            return

        next_hub = hubs[1]

        if not next_hub.has_capacity():
            return

        if next_hub.zone == "restricted":
            if next_hub.reserved:
                if self._reserved == next_hub:
                    self._fly_to_hub(next_hub)
                    return

        try:
            self._fly_to_hub(next_hub)
        except ValueError as e:
            print(e)


    def update(self) -> None:
        if self._progress > 0:
            self._progress += self._speed * 0.7
            x = (self._next_x - self._og_x) * self._progress / 100 + self._og_x
            y = (self._next_y - self._og_y) * self._progress / 100 + self._og_y
            self.pos = (x, y)
            if self._progress >= 100:
                self._progress = 0
                self.pos = self._hub.pos
