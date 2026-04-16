from .hub import Hub
from typing import List


class Connection:
    def __init__(self, max_link_capacity: int = 1) -> None:
        self._from_hubs: List[Hub] = []
        self._to_hubs: List[Hub] = []
        self._max_link_capacity = max_link_capacity
