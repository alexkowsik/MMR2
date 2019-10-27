
class GraphAsMatrix:
    def __init__(self):
        self.graph = [[0]]
        self.nodeValues = [0]
        self.numOfNodes = 1
        self.numOfEdges = 0

    def add_node(self, value=0):
        self.numOfNodes += 1
        
        for row in self.graph:
            row.append(0)
        self.graph.append([0] * self.numOfNodes)
        self.nodeValues.append(value)

    def set_node_value(self, u, value):
        self.nodeValues[u] = value

    def node_value(self, u):
        return self.nodeValues[u]

    def add_edge(self, edge, value=0):
        self.numOfEdges += 1
        self.graph[edge[0]][edge[1]] = value

    def set_edge_value(self, e, value):
        self.graph[e[0]][e[1]] = value

    def edge_value(self, e):
        return self.graph[e[0]][e[1]]

    def num_nodes(self):
        return self.numOfNodes

    # TODO: rewrite
    def num_edges(self):
        return self.numOfEdges

    @staticmethod
    def from_node(e):
        return e[0]

    @staticmethod
    def to_node(e):
        return e[1]

    def out_edges(self, u):
        edges = []
        for index, element in enumerate(self.graph[u]):
            if element == 1:
                edges.append((u, index))
        return edges

    def in_edges(self, u):
        edges = []
        for i in range(self.numOfNodes - 1):
            if self.graph[i][u] == 1:
                edges.append((i, u))
        return edges

    def print_graph(self):
        for row in self.graph:
            print(row)

    # currently returns only one direction
    def nodes_connected(self, u, v):
        if self.graph[u][v] == 1:
            return u, v
        elif self.graph[v][u] == 1:
            return v, u
        else:
            return None


class GraphAsList:

    # nodes holds all outgoing edges and looks like this:
    # 1. node 1 value, [(edge node, edge value), (edge node, edge value), ...]
    # 2. node 2 value, [...]
    # ...

    def __init__(self):
        self.nodes = []
        self.numOfNodes = 0
        self.numOfEdges = 0

    def add_node(self, value=0):
        self.nodes.append((value, []))
        self.numOfNodes += 1

    def add_edge(self, edge, value=0):
        self.nodes[edge[0]][1].append((edge[1], value))
        self.numOfEdges += 1

    def num_nodes(self):
        return self.numOfNodes

    def num_edges(self):
        return self.numOfEdges

    @staticmethod
    def from_node(e):
        return e[0]

    @staticmethod
    def to_node(e):
        return e[1]

    def out_edges(self, u):
        edges = []
        for node in self.nodes[u][1]:
            edges.append((u, node[0], node[1]))  # (u, v, value of edge)
        return edges

    def in_edges(self, u):
        edges = []
        for i in range(self.numOfNodes):
            for edge in self.nodes[i][1]:
                if edge[0] == u:
                    edges.append((i, u, edge[1]))
        return edges

    def print_graph(self):
        for node_list in self.nodes:
            print(node_list)

    # currently returns only one connection
    def nodes_connected(self, u, v):
        for edge in self.nodes[u][1]:
            if edge[0] == v:
                return u, v
        for edge in self.nodes[v][1]:
            if edge[0] == u:
                return v, u
        return None


if __name__ == '__main__':
    g = GraphAsMatrix()
    g.add_node()
    g.add_node()
    g.add_edge((0, 2))
    g.add_edge((0, 1))
    g.add_edge((1, 2))
    g.print_graph()

    print()
