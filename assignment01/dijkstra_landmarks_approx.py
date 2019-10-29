from priority_queue import PQueue
from graph import GraphAsList, GraphAsDict
import csv
from math import cos,sin,acos
import timeit


def compute_landmark_distances(g, landmarks):
    l = []      # list of dictionarys where key is a node and value is the distance between the node and the landmark with the same index in landmarks as the dict in l
    for ID in landmarks:
        s = ID
        G = PQueue()
        S = []
        p = {}      # dictionary (saves nodes at [0] and distances at [1])
        t = None    # dijkstra with empty destination calculates distance to every node from start

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

                    p[v] = [u ,p[u][1] + g.nodes[v][1][e][1]]   # p[v] = [prev node (u), distance from s to u + distance from u to v]
                elif p[u][1]+ g.nodes[v][1][e][1] < p[v][1]:    # if path with u-v is shorter than privious path to v: replace p[v]

                    p[v][1] = p[u][1]+ g.nodes[v][1][e][1]
                    p[v][0] = u
        l.append(p)
    return l


def get_landmark_heueristic(u, t, l):   # takes node_IDs u and t for current and destination and a landmarklist l (dicts), returns a lower bound for node u
    if not l:
        print('no landmarks in landmark list!')
    h = []
    for L in l:
        d_uL = L[u]
        d_tL = L[t]
        temp = d_uL - d_tL
        if temp >= 0:
            h.append(temp)
    if h:
        return max(h)
    else:
        print('all distances negative, returning 0')
        return 0


def dijkstra_landmarks(g, s, t, landmarks):
    print('processing landmarks...')
    l = compute_landmark_distances(g, landmarks)
    print('done!')

    start = timeit.default_timer()
    for ID in landmarks:
        l.append(g.nodes[ID])
    G = PQueue()
    S = []
    p = {}

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
        hu = get_landmark_heueristic(u, t, l)   # lower bound for distance between u and t
        adjacent_nodes = [x[0] for x in g.nodes[u][1] if x[0] not in S]
        for v in adjacent_nodes:
            e = [x[0] for x in g.nodes[v][1]].index(u)

            hv = get_landmark_heueristic(v, t, l)   # lower bound for distance between v and t
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
    stop = timeit.default_timer()
    print('runtime for dijkstra_landmarks():', (start - stop) * -1, 'seconds')
    return P

