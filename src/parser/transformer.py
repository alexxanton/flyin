from lark import Transformer
from typing import List, Dict, Tuple, Set, Any, Union


class DroneTransformer(Transformer):
    def __init__(self) -> None:
        self._nb_drones = 0
        self._hub_names: Set[str] = set()
        self._connections: Set[Tuple[str, str]] = set()
        self._valid_zones: Set[str] = {
            "normal", "blocked", "restricted", "priority"
        }
        self._valid_hub_meta: Set[str] = {
            "zone", "color", "max_drones"
        }

    def nb_drones(self, args: List[Any]) -> Dict[str, int]:
        val = int(args[0])
        if val < 0:
            raise ValueError("nb_drones must be a positive integer")
        self._nb_drones = val
        return {"nb_drones": val}

    def name_coord(self, args: List[Any]) -> Tuple[str, int, int]:
        name, x, y = str(args[0]), int(args[1]), int(args[2])
        if name in self._hub_names:
            raise ValueError(f"Duplicate zone name: {name}")
        self._hub_names.add(name)
        return name, x, y

    def hub_line(self, args: List[Any]) -> Dict[str, Any]:
        hub_type = str(args[0])
        meta = args[2]

        for key in meta.keys():
            if key not in self._valid_hub_meta:
                raise ValueError(f"Unknown key {key}")

        if "zone" in meta and meta["zone"] not in self._valid_zones:
            raise ValueError(f"Unknown zone {meta['zone']}")

        if "start" in hub_type or "end" in hub_type:
            if not "max_drones" in meta:
                meta["max_drones"] = self._nb_drones
            elif meta["max_drones"] != self._nb_drones:
                raise ValueError(
                    "{hub_type}: Max drones quantity doesn't match"
                )

        return {"type": hub_type, "params": args[1], "metadata": meta}

    def pair(self, args: List[Any]) -> Tuple[str, Union[int, str]]:
        return (
            str(args[0]), int(args[1]) if args[1].isnumeric() else str(args[1])
        )

    def metadata(self, args: List[Any]) -> Dict[str, Union[int, str]]:
        if not args:
            return {}
        return dict(args[0])

    def attributes(self, args: List[Any]) -> Dict[str, Any]:
        attrs = {}
        for k, v in args:
            attrs[k] = v
        return attrs

    def connection_line(self, args: List[Any]) -> Dict[str, Any]:
        from_hub, to_hub = str(args[0]), str(args[1])
        if from_hub not in self._hub_names or to_hub not in self._hub_names:
            raise ValueError()

        connection = (from_hub, to_hub)
        if connection in self._connections:
            raise ValueError(f"Repeated connection {connection}")
        self._connections.add(connection)

        return {
            "type": "connection",
            "params": connection,
            "metadata": args[2]
        }

    def start(self, args: List[Any]) -> List[Any]:
        return args
