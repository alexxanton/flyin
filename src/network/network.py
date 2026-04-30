from src.entity import Hub, Edge, Drone
from typing import List, Dict, Any


class DroneNetwork:
    """Represents a network of drones."""
    def __init__(self) -> None:
        self._nb_drones = 0
        self._hubs: List[Hub] = []
        self._edges: List[Edge] = []
        self._drones: List[Drone] = []
        self._turn = 0

    def create_network(self, data: List[Dict[str, Any]]) -> None:
        """Add the entities for the drone network."""
        for line in data:
            if "type" in line:
                self._add_entity(line)
            else:
                self._nb_drones = line["nb_drones"]

        start_x, start_y = self._start_hub.pos
        self._drones = [
            Drone(start_x, start_y, self._start_hub)
            for _ in range(self._nb_drones)
        ]

    def drones_landed(self) -> bool:
        if not self._end_hub.has_capacity():
            return False

        return (
            all([drone._progress == 0 for drone in self._drones ])
            #if drone._speed == 2
        )

    def find_paths(self) -> None:
        self._turn += 1
        for drone in self._drones:
            drone.next_move()

        def inactive_drones() -> List[Drone]:
            return [drone for drone in self._drones if drone._progress == 0]

        drones = inactive_drones()
        qty = len(drones)
        prev_qty = qty + 1

        while drones and qty < prev_qty:
            drones = inactive_drones()
            qty = len(drones)
            for drone in drones:
                drone.next_move()
            prev_qty = qty
        print()

    def update_drones(self) -> None:
        for drone in self._drones:
            drone.update()

    def _get_hub_by_id(self, name_id: str) -> Hub:
        hub = next((
            h for h in self._hubs if h.name == name_id
        ), None)
        if not hub:
            raise ValueError(f"{name_id} not found")
        return hub

    def _add_entity(self, line: Dict[str, Any]) -> None:
        """Add an entity from the parsed line."""

        if "hub" in line["type"]:
            hub = Hub(*line["params"], **line["metadata"])
            self._hubs.append(hub)
            if "start" in line["type"]:
                self._start_hub: Hub = hub
            elif "end" in line["type"]:
                self._end_hub: Hub = hub
        elif line["type"] == "connection":
            from_hub, to_hub = [
                self._get_hub_by_id(hub) for hub in line["params"]
            ]
            edge = Edge(from_hub, to_hub, **line["metadata"])
            from_hub.add_edge(edge)
            self._edges.append(edge)
            #to_hub.add_edge(edge.flipped)

    @property
    def hubs(self) -> List[Hub]:
        return self._hubs

    @property
    def edges(self) -> List[Edge]:
        return self._edges

    @property
    def drones(self) -> List[Drone]:
        return self._drones

    @property
    def turn(self) -> int:
        return self._turn
