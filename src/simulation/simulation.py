from src.parser import parse_data
from src.entity import Hub
from src.network import DroneNetwork
from src.renderer import Renderer
import sys


class Simulation:
    def start(self) -> None:
        renderer = Renderer(800, 600)
        file = renderer.choose_file()
        data = parse_data(file)
        network = DroneNetwork()
        network.create_network(data)

        renderer.start(network)
        while True:
            renderer.display()
            if renderer.handle_events() == "quit":
                break
