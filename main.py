from lark import Lark, Transformer

data = """
    nb_drones: 5
    #a
    start_hub: hub 0 0 [color=green]
    end_hub: goal 10 10 [color=yellow]
    hub: roof1 3 4 [zone=restricted color=red]
    hub: roof2 6 2 [zone=normal color=blue]
    hub: corridorA 4 3 [zone=priority color=green max_drones=2]
    hub: tunnelB 7 4 [zone=normal color=red]
    hub: obstacleX 5 5 [zone=blocked color=gray]
    connection: hub-roof1
    connection: hub-corridorA
    connection: roof1-roof2
    connection: roof2-goal
    connection: corridorA-tunnelB [max_link_capacity=2]
    connection: tunnelB-goal
"""

drone_grammar = r"""
    start: line+

    ?line: nb_drones | hub_line | connection_line

    nb_drones: "nb_drones:" INT
    hub_line: HUB_TYPE ":" NAME INT INT [attributes]
    connection_line: "connection:" NAME "-" NAME [attributes]

    attributes: "[" pair (pair)* "]"
    pair: NAME "=" (NAME | INT)

    HUB_TYPE: "start_hub" | "end_hub" | "hub"
    NAME: /[a-zA-Z0-9_]+/
    COMMENT: /#[^\n]*/

    %import common.INT
    %import common.WS
    %ignore COMMENT
    %ignore WS
"""

class DroneTransformer(Transformer):
    def start(self, items): return items
    def nb_drones(self, s): return ("drones", int(s[0]))
    def pair(self, p): return (str(p[0]), int(p[1]) if p[1].isdigit() else str(p[1]))
    def attributes(self, a): return dict(a)
    def hub_line(self, h): return {"type": "hub", "label": h[0], "id": h[1], "pos": (h[2], h[3]), "attr": h[4] or {}}
    def connection_line(self, c): return {"type": "conn", "from": c[0], "to": c[1], "attr": c[2] or {}}

parser = Lark(drone_grammar, parser='lalr', transformer=DroneTransformer())
try:
    parsed_data = parser.parse(data)
except Exception as e:
    print(e)
    exit()

for item in parsed_data:
    print(item)
