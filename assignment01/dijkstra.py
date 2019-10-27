from MMR2.assignment01.priority_queue import PQueue
from MMR2.assignment01.graph import GraphAsMatrix, GraphAsList

graph = GraphAsList()  # create graph

s = None  # start node (u, value)
t = None  # end node (u, value)

G = PQueue()
S = list()
p = PQueue()
d = PQueue()  # push nodes with float("inf") values?

G.push(s[0], s[1])
d.push(s, 0)

while G.get_length():
    u = G.pop_min()
    S.append(u)

    if u == t:
        break

    out_edges = graph.out_edges(u)

    for edge in out_edges:
        if edge[1] == u:
            break
        if not edge[0] in G:
            G.push(edge[0])
            # ...