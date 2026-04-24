from .entity import Entity
from .map_entities import Hub


class Drone(Entity):
    def __init__(self, x: int, y: int, hub: Hub) -> None:
        super().__init__(x, y)
        self._hub: Hub = hub
        self._progress: float = 0
        self._hub.land_on()
        self._og_x = x
        self._og_y = y
        self._next_x = x
        self._next_y = y
        self._speed: int = 0

    def _fly_to_hub(self, next_hub: Hub) -> None:
        self._og_x, self._og_y = self._hub.pos
        self._next_x, self._next_y = next_hub.pos
        self._speed = 1 if next_hub.zone == "restricted" else 2
        self._hub.take_off()
        self._hub = next_hub
        next_hub.land_on()
        self._progress += 1

    def update(self) -> None:
        if self._progress > 0:
            self._progress += self._speed * 0.7
            x = (self._next_x - self._og_x) * self._progress / 100 + self._og_x
            y = (self._next_y - self._og_y) * self._progress / 100 + self._og_y
            self.pos = (x, y)
            if self._progress >= 100:
                self._progress = 0
                self.pos = self._hub.pos
            return

        for edge in self._hub.edges:
            next_hub: Hub = edge.hubs[1]

            if next_hub.has_capacity():
                self._fly_to_hub(next_hub)
                break
