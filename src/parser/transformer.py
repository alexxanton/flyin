from lark import Transformer, v_args
from lark.tree import Meta
from typing import List, Dict, Tuple, Set, Any, Union


class ParseError(Exception):
    def __init__(self, msg: str, line: int) -> None:
        self._msg = f"Error at line {line}: {msg}"
        super().__init__(self._msg)


@v_args(meta=True)
class DroneTransformer(Transformer):
    """Parser transformer for the drone network."""
    def __init__(self) -> None:
        """Initialize the transformer."""
        self._nb_drones = 0
        self._hub_names: Set[str] = set()
        self._hub_positions: Set[Tuple[int, int]] = set()
        self._connections: Set[Tuple[str, str]] = set()
        self._start_found = False
        self._end_found = False
        self._valid_zones: Set[str] = {
            "normal", "blocked", "restricted", "priority"
        }
        self._valid_hub_meta: Set[str] = {
            "zone", "color", "max_drones"
        }

    def nb_drones(self, pmeta: Meta, args: List[Any]) -> Dict[str, int]:
        """Defines how to return nb_drones."""
        val = int(args[0])
        if val < 0:
            raise ParseError(
                "nb_drones must be a positive integer", pmeta.line
            )
        self._nb_drones = val
        return {"nb_drones": val}

    def name_coord(self, pmeta: Meta, args: List[Any]) -> Tuple[str, int, int]:
        """Defines how to return name_coord."""
        name, x, y = str(args[0]), int(args[1]), int(args[2])
        if name in self._hub_names:
            raise ParseError(f"Duplicate zone name: {name}", pmeta.line)
        if (x, y) in self._hub_positions:
            raise ParseError(f"Duplicate zone position: {name}", pmeta.line)
        self._hub_names.add(name)
        self._hub_positions.add((x, y))
        return name, x, -y

    def hub_line(self, pmeta: Meta, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return hub_line."""
        hub_type = str(args[0])
        meta = args[2]

        for key in meta.keys():
            if key not in self._valid_hub_meta:
                raise ParseError(f"Unknown key {key}", pmeta.line)

        if "zone" in meta and meta["zone"] not in self._valid_zones:
            raise ParseError(f"Unknown zone {meta['zone']}", pmeta.line)

        if "max_drones" in meta and meta["max_drones"] < 1:
            raise ParseError("max_drones can't be smaller than 1", pmeta.line)

        if "start" in hub_type or "end" in hub_type:
            if "max_drones" not in meta:
                meta["max_drones"] = self._nb_drones
            elif meta["max_drones"] != self._nb_drones:
                raise ParseError(
                    "{hub_type}: Max drones quantity doesn't match",
                    pmeta.line
                )
            if hub_type == "start_hub":
                if self._start_found:
                    raise ParseError("start_hub is duplicated", pmeta.line)
                self._start_found = True
            if hub_type == "end_hub":
                if self._end_found:
                    raise ParseError("end_hub is duplicated", pmeta.line)
                self._end_found = True

        return {"type": hub_type, "params": args[1], "metadata": meta}

    def hub_options(self, pmeta: Meta, args: List[Any]) -> Any:
        """Defines how to return hub_options."""
        return args[0]

    def color_pair(self, pmeta: Meta, args: List[Any]) -> Tuple[str, str]:
        """Defines how to return color_pair."""
        return (str(args[0]), str(args[1]))

    def zone_pair(self, pmeta: Meta, args: List[Any]) -> Tuple[str, str]:
        """Defines how to return zone_pair."""
        return (str(args[0]), str(args[1]))

    def max_pair(self, pmeta: Meta, args: List[Any]) -> Tuple[str, int]:
        """Defines how to return max_pair."""
        return (str(args[0]), int(args[1]))

    def connection_pair(self, pmeta: Meta, args: List[Any]) -> Tuple[str, int]:
        """Defines how to return connection_pair."""
        return (str(args[0]), int(args[1]))

    def hub_metadata(
        self, pmeta: Meta, args: List[Any]
    ) -> Dict[str, Union[int, str]]:
        """Defines how to return hub_metadata."""
        if not args:
            return {}
        return dict(args[0])

    def conn_metadata(
        self, pmeta: Meta, args: List[Any]
    ) -> Dict[str, Union[int, str]]:
        """Defines how to return conn_metadata."""
        if not args:
            return {}
        return dict(args[0])

    def hub_attr(self, pmeta: Meta, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return hub_attr."""
        seen = set()

        for key, value in args:
            if key in seen:
                raise ParseError(f"Duplicate attribute: {key}", pmeta.line)
            seen.add(key)

        attrs = {}
        for k, v in args:
            attrs[k] = v
        return attrs

    def connection_attr(self, pmeta: Meta, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return connection_attr."""
        attrs = {}
        for k, v in args:
            attrs[k] = v
        return attrs

    def hub_attributes(self, pmeta: Meta, args: List[Any]) -> Any:
        """Defines how to return hub_attributes."""
        return args[0]

    def conn_attributes(self, pmeta: Meta, args: List[Any]) -> Any:
        """Defines how to return conn_attributes."""
        return args[0]

    def connection_line(self, pmeta: Meta, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return connection_line."""
        from_hub, to_hub = str(args[0]), str(args[1])
        for hub in [from_hub, to_hub]:
            if hub not in self._hub_names:
                raise ParseError(f"Unkown hub name: {hub}", pmeta.line)

        connection = (from_hub, to_hub)
        if connection in self._connections:
            raise ParseError(f"Repeated connection {connection}", pmeta.line)
        self._connections.add(connection)
        self._connections.add(connection[::-1])
        meta = args[2]
        if "max_link_capacity" in meta and meta["max_link_capacity"] < 1:
            raise ParseError(
                "max_link_capacity can't be smaller than 1", pmeta.line
            )

        return {
            "type": "connection",
            "params": connection,
            "metadata": meta
        }

    def start(self, pmeta: Meta, args: List[Any]) -> List[Any]:
        """Defines how to return start."""
        return args

    def line(self, pmeta: Meta, args: List[Any]) -> Dict[str, Any]:
        """Defines how to return line."""
        return dict(args[0])
