from .hub import Hub
from typing import List


class Connection:
    def __init__(self) -> None:
        self._from_hubs: List[Hub] = []
        self._to_hubs: List[Hub] = []
