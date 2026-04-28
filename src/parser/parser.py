from lark import Lark
from typing import List, Dict, Any, Union
from .transformer import DroneTransformer
import sys


drone_grammar = r"""
    start: nb_drones _nl* line+

    ?line: hub_line | connection_line

    nb_drones: "nb_drones:" SIGNED_INT
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
    _nl: (NEWLINE | COMMENT)

    %import common.SIGNED_INT
    %import common.WS
    %ignore COMMENT
    %ignore WS
"""


def parse_data(file: str) -> List[Dict[str, Any]]:
    data = ""
    try:
        with open(file, "r") as f:
            data = f.read()
    except OSError as e:
        sys.exit(str(e))

    parser = Lark(
        drone_grammar, parser="lalr", transformer=DroneTransformer()
    )

    try:
        parsed_data: List[Dict[str, Union[int, str]]] = parser.parse(data)
    except Exception as e:
        sys.exit(str(e))

    for item in parsed_data:
        print(item)

    return parsed_data
