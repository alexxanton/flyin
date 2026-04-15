from src.entity import Hub, Connection
from typing import List, Dict, Any


class DroneNetwork:
    """Represents a network of drones."""
    def __init__(self) -> None:
        self._nb_drones: int = 0
        self._hubs: List[Hub] = []
        self._connections: List[Connection] = []

    def create_network(self, data: List[Dict[str, Any]]) -> None:
        for line in data:
            if "type" in line:
                self._add_entity(line)
            else:
                self._nb_drones = line["nb_drones"]

    def _add_entity(self, line: Dict[str, Any]) -> None:
        if "hub" in line["type"]:
            self._hubs.append(Hub(*line["params"], **line["metadata"]))
        elif line["type"] == "connection":
            from_hub, to_hub = line["params"]
            self._connections.append(Connection(**line["metadata"]))
