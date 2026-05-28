from src.entity import Hub, Edge, Drone
from typing import List, Dict, Any, Optional
from copy import deepcopy


class DroneNetwork:
    """Represents a network of drones."""
    def __init__(self) -> None:
        """Initialize the drone network."""
        self._nb_drones = 0
        self._hubs: List[Hub] = []
        self._edges: List[Edge] = []
        self._drones: List[Drone] = []
        self._turn = 0
        self._copy = False

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

    def end_reached(self) -> bool:
        """Return whether all drones have reached the end or not."""
        return not self._end_hub.has_capacity()

    def drones_landed(self) -> bool:
        """Checks if all the drones have reached their objective."""
        return all([drone.progress == 0 for drone in self._drones])

    def find_paths(self) -> None:
        """Make all the drones find the path to the end goal."""
        og_cpy = deepcopy(self)
        og_cpy._copy = True

        def _future(drone: Drone, hub: Hub) -> bool:
            cpy = deepcopy(og_cpy)
            for d in cpy._drones:
                d._copy = True

            next_hub = next((h for h in cpy._hubs if h.name == hub.name), None)
            cpy_drone = next((d for d in cpy._drones if d.id == drone.id), None)
            for x in range(2):
                cpy.find_paths()
                while not cpy.drones_landed():
                    cpy.update_drones()

            #print(next_hub.name, next_hub._drones_landed)
            if not next_hub or not cpy_drone:
                return False
            return cpy_drone.hub.name != next_hub.name

        self._turn += 1

        def inactive_drones() -> List[Drone]:
            """Return a list of inactive drones."""
            return [drone for drone in self._drones if drone.progress == 0]

        drones = inactive_drones()
        qty = len(drones)
        prev_qty = qty + 1

        while drones and qty < prev_qty:
            drones = inactive_drones()
            qty = len(drones)
            for drone in drones:
                drone.next_move(_future if not self._copy else None)
            prev_qty = qty
        if not self._copy:
            print()

    def update_drones(self) -> None:
        """Update all the drones."""
        for drone in self._drones:
            drone.update()

    def _get_hub_by_id(self, name_id: str) -> Hub:
        """Return a hub by its ID."""
        hub = next((
            h for h in self._hubs if h.name == name_id
        ), None)
        if not hub:
            raise ValueError(f"{name_id} not found")
        return hub

    def _add_entity(self, line: Dict[str, Any]) -> None:
        """Add an entity from the parsed line."""

        if "hub" in line["type"]:
            params = *line["params"], line["type"]
            hub = Hub(*params, **line["metadata"])
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
            to_hub.add_edge(edge.flipped)

    @property
    def hubs(self) -> List[Hub]:
        """Returns the network hubs."""
        return self._hubs

    @property
    def edges(self) -> List[Edge]:
        """Returns the network edges."""
        return self._edges

    @property
    def drones(self) -> List[Drone]:
        """Returns the network drones."""
        return self._drones

    @property
    def turn(self) -> int:
        """Returns the current turn."""
        return self._turn
