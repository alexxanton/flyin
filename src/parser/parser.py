from lark import Lark, UnexpectedToken
from typing import List, Dict, Any, Union, cast
from .transformer import DroneTransformer
import sys
import re


class Parser:
    DRONE_GRAMMAR = r"""
        start: _nl* nb_drones _nl* line+

        ?line: (hub_line | connection_line) _nl

        nb_drones: "nb_drones:" SIGNED_INT _nl
        hub_line: HUB_TYPE ":" name_coord metadata
        connection_line: "connection:" NAME "-" NAME metadata

        metadata: attributes?
        name_coord: NAME SIGNED_INT SIGNED_INT
        attributes: (hub_attr | connection_attr)

        hub_attr: "[" hub_pair+ "]"
        connection_attr: "[" connection_pair+ "]"
        hub_pair: (hub_str_pair | hub_int_pair)

        hub_str_pair: HUB_META_STR "=" NAME
        hub_int_pair: HUB_META_INT "=" INT
        connection_pair: CONNECTION_META "=" INT

        HUB_TYPE: "start_hub" | "end_hub" | "hub"
        HUB_META_STR: "zone" | "color"
        HUB_META_INT: "max_drones"
        CONNECTION_META: "max_link_capacity"

        ZONE: "normal" | "restricted" | "priority" | "blocked"
        NAME: /[a-zA-Z0-9_]+/
        COMMENT: /#[^\n]*/
        NEWLINE: /\r?\n+/
        _nl: (NEWLINE | COMMENT)

        %import common.SIGNED_INT
        %import common.INT
        %import common.WS_INLINE
        %ignore COMMENT
        %ignore WS_INLINE
    """

    def _format_error(self, e: UnexpectedToken, text: str) -> str:
        """Format the error message to make it user-friendly."""
        TOKEN_HINTS = {
            "SIGNED_INT": "a number",
            "NAME": "hub name",
            "EQUAL": "=",
        }

        expected = ", ".join(sorted(e.expected)) if e.expected else ""

        return (
            f"\nSyntax error at line {e.line}, column {e.column}:\n"
            f"{text.splitlines()[e.line - 1]}\n"
            f"{'^':>{e.column}}\n"
            f"Expected: {TOKEN_HINTS.get(expected, e.expected)}\n"
            f"Found: {e.token.value!r}\n"
        )

    def parse_data(self, file: str) -> List[Dict[str, Any]]:
        """Parse data from file."""
        data = ""
        try:
            with open(file, "r") as f:
                data = f.read()
        except OSError as e:
            sys.exit(str(e))

        lines = data.splitlines()
        formatted_lines = []
        for line in lines:
            line = re.sub(r"^\s+", "", line)
            line = re.sub(r"\s+", " ", line)
            if line.startswith("#"):
                line = ""
            formatted_lines.append(line)
        data = "\n".join(formatted_lines) + "\n"
        print(data)

        parser = Lark(
            self.DRONE_GRAMMAR,
            parser="lalr",
            propagate_positions=True,
        )

        try:
            tree = parser.parse(data)
            transformer = DroneTransformer()
            d = transformer.transform(tree)
            parsed_data = cast(
                List[Dict[str, Union[int, str]]], d
            )
        except UnexpectedToken as e:
            sys.exit(self._format_error(e, data))
        except Exception as e:
            sys.exit(str(e))
            #raise

        for item in parsed_data:
            print(item)

        return parsed_data
