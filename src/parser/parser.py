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
        hub_line: HUB_TYPE ":" name_coord hub_metadata
        connection_line: "connection:" NAME "-" NAME conn_metadata

        hub_metadata: hub_attributes?
        conn_metadata: conn_attributes?
        name_coord: NAME SIGNED_INT SIGNED_INT
        hub_attributes: hub_attr
        conn_attributes: connection_attr

        hub_attr: "[" hub_options+ "]"
        connection_attr: "[" connection_pair "]"
        hub_options: (color_pair | max_pair | zone_pair)

        color_pair: COLOR "=" WORD
        max_pair: MAX_DRONES "=" INT
        zone_pair: ZONE "=" ZONES
        connection_pair: MAX_LINK "=" INT

        HUB_TYPE: "start_hub" | "end_hub" | "hub"
        ZONE: "zone"
        COLOR: "color"
        MAX_DRONES: "max_drones"
        MAX_LINK: "max_link_capacity"

        ZONES: "normal" | "restricted" | "priority" | "blocked"
        NAME: /[a-zA-Z0-9_]+/
        COMMENT: /#[^\n]*/
        NEWLINE: /\r?\n+/
        _nl: (NEWLINE | COMMENT)

        %import common.SIGNED_INT
        %import common.INT
        %import common.WORD
        %import common.WS_INLINE
        %ignore COMMENT
        %ignore WS_INLINE
    """

    def _format_error(self, e: UnexpectedToken, text: str) -> str:
        """Format the error message to make it user-friendly."""
        TOKEN_HINTS = {
            "__ANON_0": "nb_drones",
            "SIGNED_INT": "a number",
            "INT": "a positive number",
            "NAME": "hub name",
            "EQUAL": "=",
            "COLON": ":",
            "LSQB": "[",
            "RSQB": "]",
            "ZONE": "zone",
            "COLOR": "color",
            "MAX_DRONES": "max_drones",
            "MAX_LINK": "max_link_capacity",
            "ZONES": "normal | restricted | priority | blocked",
            "HUB_TYPE": "start_hub | end_hub | hub"
        }

        expected = "\n  " + "\n  ".join([
            f"{TOKEN_HINTS.get(e, e)!r}" for e in sorted(e.expected)
        ])

        return (
            f"\nSyntax error at line {e.line}:\n"
            f"{text.splitlines()[e.line - 1]}\n"
            f"{'^':>{e.column}}\n"
            f"Expected: {expected}\n"
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
