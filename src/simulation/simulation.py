from src.parser import parse_data
from src.entity import Hub
from src.network import DroneNetwork
from src.renderer import Renderer
import sys


class Simulation:
    def __init__(self) -> None:
        self._renderer = Renderer(800, 600)

    def _run_simulation(self) -> None:
        file = self._renderer.choose_file()
        data = parse_data(file)
        network = DroneNetwork()
        network.create_network(data)

        self._renderer.start(network)
        while True:
            self._renderer.display()
            if self._renderer.handle_events() == "quit":
                break

    def start(self) -> None:
        while True:
            self._run_simulation()
