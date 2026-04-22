from .entity import Entity
from .map_entities import Hub


class Drone(Entity):
    def __init__(self, x: int, y: int, hub: Hub) -> None:
        super().__init__(x, y)
        self._hub: Hub = hub
