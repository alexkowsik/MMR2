from priority_queue import PQueue
from graph import GraphAsList, GraphAsDict
import csv
from math import cos,sin,acos
def dijkstra(g, s, t):
    a = (g.nodes[247680031])
    b = (g.nodes[29547031])
    c = (g.nodes[296242292])
    d = (g.nodes[29547031])
    G = PQueue()
    S = []
    p = {}
    for key, value in g.nodes.items():
        p[key] = [None,float('inf')]
    p[s][1] = 0
    G.push(p,s)

    while G.get_length():
        u = G.items[0]
        S.append(u)
        G.pop_min()
        if u == t:
            break
        edges = [x[0] for x in g.nodes[u][1] if x[0] not in S]
        for v in edges:
            e = [x[0] for x in g.nodes[v][1]].index(u)
            if v not in G.items:
                G.push(p,v)

                p[v] = [u ,p[u][1] + g.nodes[v][1][e][1]]
            elif p[u][1]+ g.nodes[v][1][e][1] < p[v][1]:

                p[v][1] = p[u][1]+ g.nodes[v][1][e][1]
                p[v][0] = u
    if p[t][1] == float('inf'):
        return []
    P =[t]
    u = t
    while u != s:
        P.append(p[u][0])
        u = p[u][0]
    return P

