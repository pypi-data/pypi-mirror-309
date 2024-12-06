from typing import TypeVar, Generic, cast
from collections import deque, OrderedDict

T = TypeVar("T")


class Node:
    def __repr__(self):
        return f"Node(data={repr(self.data)}, connections={len(self.connections)}, visited={self.visited})"

    def __init__(self, obj: object):
        self.data = obj
        self.connections = OrderedDict()
        self.visited = False
        self.linked_by: Node | None = None

    def __hash__(self) -> int:
        return hash((self.data))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented

        return other.data == self.data and other.connections == other.connections

    def connect(self, other: "Node"):
        self.connections[other] = True

    def disconnect(self, other: "Node"):
        del self.connections[other]

    def is_connected(self, other: "Node") -> bool:
        return other in self.connections

    def bfs(self, value: object) -> list["Node"]:
        result = []
        if self.data == value:
            result.append(self)
            return result

        self.visited = True
        q = deque(self.connections)

        while q:
            this = q.popleft()
            if this.visited:
                continue
            if this.data == value:
                while this is not None:
                    result.append(this)
                    this = this.linked_by
                break
            else:
                this.visited = True
                for neighbor in this.connections:
                    if not neighbor.visited:
                        # infinite loop
                        neighbor.linked_by = this
                        q.append(neighbor)

        if len(result) == 0:
            return result
        else:
            return [self] + list(reversed(result))

    def dfs(self, value: object) -> list["Node"]:
        def impl(this: "Node", result: list[Node]):
            if this.visited:
                return

            this.visited = True
            if this.data == value:
                walker: Node | None = this
                while walker:
                    result.append(walker)
                    walker = walker.linked_by
                return result

            for item in this.connections:
                if item is not this and not item.visited:
                    item.linked_by = this
                    impl(item, result)

        if self.data == value:
            return [self]
        else:
            r = []
            impl(self, r)
            return r

    def reset(self):
        self.visited = False
        self.linked_by = None


import re

line_sep = re.compile(r"\r?\n")
con_sep = re.compile(r",\s*")
comment = re.compile(r"\s*#.*?\n")


class Graph(Generic[T]):
    @classmethod
    def fromgraphstr(cls: type["Graph[str]"], s: str) -> "Graph[str]":
        s = comment.sub("\n", s)
        lines = line_sep.split(s)
        if lines[0][0] == "!":
            directive = lines.pop(0)
            if directive == "!nodir":
                directed = False
            elif directive == "!dir":
                directed = True
            else:
                directed = False
        else:
            directed = False

        g = cls(directed=directed)
        to_connect = []
        for line in (i for i in lines if i):
            line = line.strip()
            i = line.index(":")
            if line[0] == "!":
                raise ValueError("Cannot have !directive that is not the first line")
            if line[i] == line[-1]:
                # node with no connections; bail
                g.add(line[:i])
            else:
                name, connections = line[:i].strip(), line[i + 1 :].strip()
                g.add(name)
                if len(connections) > 0:
                    for con in con_sep.split(connections):
                        # cannot connect nodes until all nodes are added
                        to_connect.append((name, con))

        # once all nodes are added do the connections
        for start, end in to_connect:
            g.connect(start, end)

        return g

    def __str__(self):
        return ", ".join(
            f"Graph[{i}[{len(i.connections)} conns.]]" for i in self.nodes.values()
        )

    def reset(self):
        for node in self.nodes.values():
            node.reset()

    def __init__(
        self, *values: T, connections: dict[T, T] | None = None, directed: bool = True
    ):
        self.nodes: dict[T, Node] = {}
        self.directed = directed

        for value in values:
            self.add(value)

        if connections:
            for start, end in connections.items():
                self.connect(start, end)

    def add(self, value: T):
        self.nodes[value] = Node(value)

    def has(self, value: T) -> bool:
        return value in self.nodes

    def dfs(self, start: T, value: T) -> list[T]:
        if start not in self.nodes:
            raise ValueError("No such starting node") from None

        r = [cast(T, i.data) for i in self.nodes[start].dfs(value)]
        self.reset()
        return r

    def bfs(self, start: T, value: T) -> list[T]:
        if start not in self.nodes:
            raise ValueError("No such starting node") from None

        r = [cast(T, i.data) for i in self.nodes[start].bfs(value)]
        self.reset()
        return r

    def disconnect(self, v1: T, v2: T) -> bool:
        try:
            n1 = self.nodes[v1]
            n2 = self.nodes[v2]
        except KeyError:
            raise ValueError("No such value to connect") from None

        if not n1.is_connected(n2):
            return False

        n1.disconnect(n2)
        return True

    def connect(self, value1: T, value2: T) -> bool:
        try:
            n1 = self.nodes[value1]
            n2 = self.nodes[value2]
        except KeyError:
            raise ValueError("No such value to connect") from None

        if n1.is_connected(n2):
            return False

        n1.connect(n2)
        if not self.directed:
            n2.connect(n1)
        return True

    def is_connected(self, value1: T, value2: T) -> bool:
        try:
            n1 = self.nodes[value1]
            n2 = self.nodes[value2]
        except KeyError:
            raise ValueError("No such value to connect") from None

        return n1.is_connected(n2)


with open("test/simple.gsf") as f:
    g = Graph.fromgraphstr(f.read())

print(g.bfs("a", "e"))
print(g.dfs("a", "e"))
