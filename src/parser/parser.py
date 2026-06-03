from lark import Lark, UnexpectedToken
from typing import List, Dict, Any, Union, cast
from .transformer import DroneTransformer
import sys


class Parser:
    DRONE_GRAMMAR = r"""
        start: nb_drones _nl* line+

        ?line: (hub_line | connection_line) _nl

        nb_drones: "nb_drones:" SIGNED_INT _nl
        hub_line: HUB_TYPE ":" name_coord metadata
        connection_line: "connection:" NAME "-" NAME metadata

        metadata: attributes?
        name_coord: NAME SIGNED_INT SIGNED_INT
        attributes: "[" pair (pair)* "]"
        pair: NAME "=" (NAME | SIGNED_INT)

        HUB_TYPE: "start_hub" | "end_hub" | "hub"
        NAME: /[a-zA-Z0-9_]+/
        COMMENT: /#[^\n]*/
        NEWLINE: /\r?\n+/
        _nl: (NEWLINE | (COMMENT NEWLINE))

        %import common.SIGNED_INT
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

        parser = Lark(
            self.DRONE_GRAMMAR, parser="lalr", transformer=DroneTransformer()
        )

        try:
            parsed_data = cast(
                List[Dict[str, Union[int, str]]], parser.parse(data)
            )
        except UnexpectedToken as e:
            sys.exit(self._format_error(e, data))
        except Exception as e:
            sys.exit(str(e))

        for item in parsed_data:
            print(item)

        return parsed_data
