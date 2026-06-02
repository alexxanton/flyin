from src.parser import Parser
from src.entity import Drone
from src.network import DroneNetwork
from src.renderer import Renderer


class Simulation:
    """Simulation orchestrator."""
    def __init__(self) -> None:
        """Initialize the simulation."""
        self._renderer = Renderer()

    def _run_simulation(self) -> None:
        """Run the simulation."""
        file = self._renderer.choose_file()
        parser = Parser()
        data = parser.parse_data(file)
        network = DroneNetwork()
        network.create_network(data)

        self._renderer.start(network)
        while True:
            if not network.drones_landed() or network.end_reached():
                network.update_drones()
            else:
                network.find_paths()
            self._renderer.display()
            if self._renderer.handle_events() == "quit":
                break

    def start(self) -> None:
        """Start the simulation."""
        while True:
            Drone.next_id = 1
            self._run_simulation()
