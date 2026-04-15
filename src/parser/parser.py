from lark import Lark
from typing import List, Dict, Tuple, Set, Any, Union
from .transformer import DroneTransformer
import sys


drone_grammar = r"""
    start: nb_drones _nl* line+

    ?line: hub_line | connection_line

    nb_drones: "nb_drones:" INT
    hub_line: HUB_TYPE ":" name_coord metadata
    connection_line: "connection:" NAME "-" NAME metadata

    metadata: attributes?
    name_coord: NAME INT INT
    attributes: "[" pair (pair)* "]"
    pair: NAME "=" (NAME | INT)

    HUB_TYPE: "start_hub" | "end_hub" | "hub"
    NAME: /[a-zA-Z0-9_]+/
    COMMENT: /#[^\n]*/
    NEWLINE: /\r?\n+/
    _nl: (NEWLINE | COMMENT)

    %import common.INT
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

    parser = Lark(drone_grammar, parser="lalr", transformer=DroneTransformer())
    try:
        parsed_data = parser.parse(data)
    except Exception as e:
        #raise
        sys.exit(str(e))

    for item in parsed_data:
        print(item)

    return parsed_data
