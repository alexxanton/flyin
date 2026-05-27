from typing import Tuple


class Entity:
    """Represents an entity positioned in the drone network."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize entity with its position."""
        self._x = x
        self._y = y

    @property
    def pos(self) -> Tuple[float, float]:
        """Return the entity position."""
        return (self._x, self._y)

    @pos.setter
    def pos(self, new_pos: Tuple[float, float]) -> None:
        """Assign a new position."""
        x, y = new_pos
        self._x = x
        self._y = y
