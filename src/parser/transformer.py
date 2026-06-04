from lark import Transformer
from typing import List, Dict, Tuple, Set, Any, Union


class DroneTransformer(Transformer):
    """Parser transformer for the drone network."""
    def __init__(self) -> None:
        """Initialize the transformer."""
        self._nb_drones = 0
        self._hub_names: Set[str] = set()
        self._hub_positions: Set[int] = set()
        self._connections: Set[Tuple[str, str]] = set()
        self._valid_zones: Set[str] = {
            "normal", "blocked", "restricted", "priority"
        }
        self._valid_hub_meta: Set[str] = {
            "zone", "color", "max_drones"
        }

    def nb_drones(self, args: List[Any]) -> Dict[str, int]:
        """Defines how to return nb_drones."""
        val = int(args[0])
        if val < 0:
            raise ValueError("nb_drones must be a positive integer")
        self._nb_drones = val
        return {"nb_drones": val}

    def name_coord(self, args: List[Any]) -> Tuple[str, int, int]:
        """Defines how to return name_coord."""
        name, x, y = str(args[0]), int(args[1]), int(args[2])
        if name in self._hub_names:
            raise ValueError(f"Duplicate zone name: {name}")
        self._hub_names.add(name)
        return name, x, -y

    def hub_line(self, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return hub_line."""
        hub_type = str(args[0])
        meta = args[2]

        for key in meta.keys():
            if key not in self._valid_hub_meta:
                raise ValueError(f"Unknown key {key}")

        if "zone" in meta and meta["zone"] not in self._valid_zones:
            raise ValueError(f"Unknown zone {meta['zone']}")

        if "max_drones" in meta and meta["max_drones"] < 1:
            raise ValueError("max_drones can't be smaller than 1")

        if "start" in hub_type or "end" in hub_type:
            if "max_drones" not in meta:
                meta["max_drones"] = self._nb_drones
            elif meta["max_drones"] != self._nb_drones:
                raise ValueError(
                    "{hub_type}: Max drones quantity doesn't match"
                )

        return {"type": hub_type, "params": args[1], "metadata": meta}

    def hub_pair(self, args: List[Any]) -> Tuple[str, Union[int, str]]:
        """Defines how to return pair."""
        return args[0]

    def hub_str_pair(self, args: List[Any]) -> Tuple[str, Union[int, str]]:
        """Defines how to return pair."""
        return (str(args[0]), str(args[1]))

    def hub_int_pair(self, args: List[Any]) -> Tuple[str, Union[int, str]]:
        """Defines how to return pair."""
        return (str(args[0]), int(args[1]))

    def connection_pair(self, args: List[Any]) -> Tuple[str, Union[int, str]]:
        """Defines how to return pair."""
        return (str(args[0]), int(args[1]))

    def metadata(self, args: List[Any]) -> Dict[str, Union[int, str]]:
        """Defines how to return metadata."""
        if not args:
            return {}
        return dict(args[0])

    def hub_attr(self, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return attributes."""
        attrs = {}
        for k, v in args:
            attrs[k] = v
        return attrs

    def connection_attr(self, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return attributes."""
        attrs = {}
        for k, v in args:
            attrs[k] = v
        return attrs

    def attributes(self, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return attributes."""
        return args[0]

    def connection_line(self, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return connection_line."""
        from_hub, to_hub = str(args[0]), str(args[1])
        for hub in [from_hub, to_hub]:
            if hub not in self._hub_names:
                raise ValueError(f"Unkown hub name: {hub}")

        connection = (from_hub, to_hub)
        if connection in self._connections:
            raise ValueError(f"Repeated connection {connection}")
        self._connections.add(connection)
        meta = args[2]
        if "max_link_capacity" in meta and meta["max_link_capacity"] < 1:
            raise ValueError("max_link_capacity can't be smaller than 1")

        return {
            "type": "connection",
            "params": connection,
            "metadata": meta
        }

    def start(self, args: List[Any]) -> List[Any]:
        """Defines how to return start."""
        return args

    def line(self, args: List[Any]) -> Dict[str, Any]:
        return dict(args[0])
