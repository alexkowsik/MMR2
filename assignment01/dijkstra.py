from MMR2.assignment01.priority_queue import PQueue
from MMR2.assignment01.graph import GraphAsList


def dijkstra(graph, s, t):
    G = PQueue()
    S = list()
    p = [None] * graph.numOfNodes

    t = list(t)
    s = list(s)
    s[1] = 0  # d_u is now in value of u

    G.push(s)

    while G.get_length():
        u = list(G.pop_min())
        S.append(u)

        if u == t:
            break

        out_edges = graph.out_edges(u)

        for edge in out_edges:

            # convert all tuples to lists because tuples are immutable
            edge = list(edge)
            tmp = edge[0]
            tmp = list(tmp)
            edge[0] = tmp
            tmp = edge[1]
            tmp = list(tmp)
            edge[1] = tmp

            if edge[1] in S:
                break
            if not G.__contains__(edge[1]):
                edge[1][1] = edge[0][1] + edge[2]  # value of v = value of u + weight of edge
                G.push(edge[1])
                p[edge[1][0]] = (edge[0][0], edge[1][0])
            elif edge[0][1] + edge[2] < edge[1][1]:
                G.decrease_key(edge[1], edge[0][1] + edge[2])
                p[edge[1][0]] = (edge[0][0], edge[1][0])

    if t[1] == float("inf"):
        return False

    P = list()
    u = t[0]

    while u != s[0]:
        P.append(p[u])
        u = p[u][0]

    return P


g = GraphAsList()
g.add_node(0)
g.add_node(1)
g.add_node(2)

g.add_edge((0, 1), 1)
g.add_edge((1, 2), 2)
g.add_edge((0, 2), 1)

path = dijkstra(g, g.nodes[0], g.nodes[2])

print(path)
