from .entity import Entity


class Drone(Entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
