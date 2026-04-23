from .entity import Entity
from .map_entities import Hub


class Drone(Entity):
    def __init__(self, x: int, y: int, hub: Hub) -> None:
        super().__init__(x, y)
        self._hub: Hub = hub
        self._progress: int = 0
        self._hub.land_on()
        self._og_x = x
        self._og_y = y
        self._next_x = x
        self._next_y = y

    def _fly_to_hub(self, next_hub: Hub) -> None:
        self._hub.take_off()
        self._hub = next_hub
        next_hub.land_on()
        self._progress += 1

    def update(self) -> None:
        if self._progress > 0:
            self._progress += 0.1
            self._x = (self._next_x - self._og_x) / self._progress
            self._y = (self._next_y - self._og_y) / self._progress
            if self._progress > 100:
                self._progress = 0
            return

        for edge in self._hub.edges:
            next_hub: Hub = edge.hubs[1]
            self._next_x, self._next_y = next_hub.pos[0], next_hub.pos[1]

            if next_hub.has_capacity():
                self._fly_to_hub(next_hub)
                break
