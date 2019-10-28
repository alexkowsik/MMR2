from MMR2.assignment01.priority_queue import PQueue


def dijkstra(graph):
    s = None  # start node (id, value, BG, LG)
    t = None  # end node (id, value, BG, LG)

    G = PQueue()
    S = list()
    p = [None] * graph.numOfNodes
    #d = [float("inf")] * graph.numOfNodes

    s[1] = 0  # d_u is now in value of u
    G.push(s)

    while G.get_length():
        u = G.pop_min()
        S.append(u)

        if u == t:
            break

        out_edges = graph.out_edges(u)

        for edge in out_edges:
            if edge[1] in S:
                break
            if not edge[1] in G:
                edge[1][1] = edge[0][1] + edge[2]  # value of v = value of u + weight of edge
                G.push(edge[1])
                p[edge[1][0]] = edge
            elif edge[0][1] + edge[2] < edge[1][1]:
                edge[1][1] = edge[0][1] + edge[2]
                p[edge[1][0]] = edge

    if t[1] == float("inf"):
        return False

    P = list()
    u = t

    while u != s:
        P.append(p[u[0]])
        u = p[u[0]][0]
