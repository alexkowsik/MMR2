from priority_queue import PQueue
from graph import GraphAsList, GraphAsDict
import csv
from math import cos,sin,acos


def dist(u, v):     # u and v are nodes as in graphAsDict
    beta1 = u[2]
    lambda1 = u[3]
    beta2 = v[2]
    lambda2 = v[3]
    distance = 6378.388 * acos(sin(beta1) * sin(beta2) + cos(beta1) * cos(beta2) * cos(abs(lambda1 - lambda2)))
    return distance


def dijkstra_euk(g, s, t):
    G = PQueue()
    S = []
    p = {}      # dictionary (saves nodes at [0] and distances at [1])
    for key, value in g.nodes.items():
        p[key] = [None, float('inf')]
    p[s][1] = 0
    G.push(p, s)

    while G.get_length():
        u = G.items[0]
        S.append(u)
        G.pop_min()
        if u == t:
            break
        hu = dist(g.nodes[u], g.nodes[t])   # lower bound for distance between u and t
        adjacent_nodes = [x[0] for x in g.nodes[u][1] if x[0] not in S]
        for v in adjacent_nodes:
            e = [x[0] for x in g.nodes[v][1]].index(u)

            hv = dist(g.nodes[v], g.nodes[t])   # lower bound for distance between v and t
            l_uv = g.nodes[v][1][e][1]          # length of edge (u,v)
            l_su = p[u][1]                      # length of path (s,u)

            if v not in G.items:
                G.push(p, v)
                p[v] = [u, l_su + l_uv + hv - hu]
            elif l_su + l_uv + hv - hu < p[v][1]:

                p[v][1] = l_su + l_uv + hv - hu
                p[v][0] = u
    if p[t][1] == float('inf'):
        return []
    P = [t]
    u = t
    while u != s:
        P.append(p[u][0])
        u = p[u][0]
    return P





