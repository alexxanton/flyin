from src.entity import Hub, Edge, Drone
from typing import List, Dict, Any


class DroneNetwork:
    """Represents a network of drones."""
    def __init__(self) -> None:
        self._nb_drones: int = 0
        self._hubs: List[Hub] = []
        self._edges: List[Edge] = []
        self._drones: List[Drone] = []

    def create_network(self, data: List[Dict[str, Any]]) -> None:
        """Add the entities for the drone network."""
        for line in data:
            if "type" in line:
                self._add_entity(line)
            else:
                self._nb_drones = line["nb_drones"]

        self._drones = [Drone(0, 0) for _ in range(self._nb_drones)]

    def _add_entity(self, line: Dict[str, Any]) -> None:
        """Add an entity from the parsed line."""
        def get_hub_by_id(name_id: str) -> Hub:
            return next((
                hub for hub in self._hubs if hub.name == name_id
            ), None)

        if "hub" in line["type"]:
            self._hubs.append(Hub(*line["params"], **line["metadata"]))
        elif line["type"] == "connection":
            from_hub, to_hub = [get_hub_by_id(hub) for hub in line["params"]]
            self._edges.append(Edge(from_hub, to_hub, **line["metadata"]))

    @property
    def hubs(self) -> List[Hub]:
        return self._hubs

    @property
    def edges(self) -> List[Edge]:
        return self._edges

    @property
    def drones(self) -> List[Drone]:
        return self._drones
