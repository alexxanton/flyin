from src.parser import parse_data
from src.entity import Hub, Drone
from src.network import DroneNetwork
from src.renderer import Renderer
import sys


class Simulation:
    def __init__(self) -> None:
        self._renderer = Renderer()

    def _run_simulation(self) -> None:
        file = self._renderer.choose_file()
        data = parse_data(file)
        network = DroneNetwork()
        network.create_network(data)

        self._renderer.start(network)
        while True:
            if not network.drones_landed():
                network.update_drones()
            else:
                network.find_paths()
            self._renderer.display()
            if self._renderer.handle_events() == "quit":
                break

    def start(self) -> None:
        while True:
            Drone.next_id = 1
            self._run_simulation()
