from src.parser import parse_data
from src.entity import Hub
from src.network import DroneNetwork
from src.renderer import Renderer
import sys


class Simulation:
    def start(self) -> None:
        if len(sys.argv) < 2:
            sys.exit("Config file not provided.")
        data = parse_data(sys.argv[1])
        renderer = Renderer(400, 300)
        network = DroneNetwork(data)
        while True:
            renderer.display()
            if renderer.handle_events() == "quit":
                break
