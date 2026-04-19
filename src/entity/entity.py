from typing import Tuple


class Entity:
    """Represents an entity positioned in the drone network."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize entity with its position."""
        self._x: int = x
        self._y: int = y

    @property
    def pos(self) -> Tuple[int, int]:
        """Return the entity position."""
        return (self._x, self._y)
