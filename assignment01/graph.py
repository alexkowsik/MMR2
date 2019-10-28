# TODO: let out_edges/in_edges also return node values


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

    def add_node(self, id,value=0, breitenG=0,laengenG=0):      # id is an int identifying the node
        self.nodes.append((id, value, [],breitenG,laengenG))  # last 2 fields are breiten/laengengrad
        self.numOfNodes += 1

    def set_node_value(self, node_id, value):
        for index, node in enumerate(self.nodes):
            if node[0] == node_id:
                tmp = list(self.nodes[index])
                tmp[1] = value
                tmp = tuple(tmp)
                self.nodes[index] = tmp
                return

    def add_edge(self, edge, value=0):
        try:
            next(x for x in self.nodes if x[0] == edge[0])[2].append((edge[1],value))
            self.numOfEdges += 1
        except:
            pass

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
        for node in self.nodes[u[0]][2]:
            tmp_node = None
            for node2 in self.nodes:
                if node2[0] == node[0]:
                    tmp_node = node2
                    break
            edges.append((u, tmp_node, node[1]))  # (u, v, value of edge)
        return edges

    def in_edges(self, u):
        edges = []
        for i in range(self.numOfNodes):
            for edge in self.nodes[i][2]:
                if edge[0] == u:
                    edges.append((i, u, edge[1]))
        return edges

    def print_graph(self, i = 0):
        if i == 0:
            i = len(self.nodes)
        count = 0
        for node_list in self.nodes:
            print("node " , node_list[0] , ":" ,node_list)
            count+= 1
            if count == i:
                return

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
    g = GraphAsList()
    g.add_node(1)
    g.add_node(3)
    g.add_edge((1,3))
    g.print_graph()
    print(next(x for x in g.nodes if x[0] == 1))
