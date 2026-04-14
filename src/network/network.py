from src.entity import Hub
from typing import List, Dict, Any


class DroneNetwork:
    def __init__(self, data: Dict[str, Any]) -> None:
        self._hubs: List[Hub]
