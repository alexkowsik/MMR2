from graph import GraphAsList
from math import sin,cos,pi,acos

g = GraphAsList()
with open("maps/nodes.csv",newline="") as file:    #open file
    reader = csv.reader(file,delimiter=",")
    for row in reader:                                  #returns rows
        g.add_node(int(row[0]),0 ,float(row[2]),float(row[1]))        #row[0]: node,[1]:breitengrad,[2]:laengengrad

counter = 0
rowCount = 0
#iterators sind rotz
with open("maps/edges.csv", newline="") as file:  # open file
    lis = [line.split() for line in file]
    lis = [row[0].split(',') for row in lis]
    while rowCount < len(lis)-1:
        #manual insertion of edges.
        tmp = g.nodes[counter]
        beta1 = tmp[3]
        lambda1 = tmp[4]
        tmp = next(x for x in g.nodes if x[0] == int(lis[rowCount][1])) #next findet den node, zu dem die kante geht
        beta2 = tmp[3]
        lambda2 = tmp[4]
        dist = 6378.388 * acos(sin(beta1) * sin(beta2) + cos(beta1) * cos(beta2) * cos(abs(lambda1 - lambda2)))
        g.nodes[counter][2].append((int(lis[rowCount][1]),dist))
        if lis[rowCount+1][0] != lis[rowCount][0]:
            counter += 1
        rowCount +=1
        if rowCount % 10000 == 0:
            print(rowCount/1600.0,"%")
    #add the last edge
    tmp = g.nodes[counter]
    beta1 = tmp[3]
    lambda1 = tmp[4]
    tmp = next(x for x in g.nodes if x[0] == int(lis[rowCount][1]))
    beta2 = tmp[3]
    lambda2 = tmp[4]
    dist = 6378.388 * acos(sin(beta1) * sin(beta2) + cos(beta1) * cos(beta2) * cos(abs(lambda1 - lambda2)))
    g.nodes[counter][2].append((int(row[1]), dist))

#generic approach for inserting the edges (indepoendent of data layout)
# with open("maps/edges.csv", newline="") as file:  # open file
#     reader = csv.reader(file, delimiter=",")
#     for row in reader:
#         try:
#             tmp = next(x for x in g.nodes if x[0] == int(row[0]))
#             beta1 = tmp[3]
#             lambda1 = tmp[4]
#             tmp = next(x for x in g.nodes if x[0] == int(row[1]))
#             beta2 = tmp[3]
#             lambda2 = tmp[4]
#             dist = 6378.388 * acos(sin(beta1) * sin(beta2) + cos(beta1) * cos(beta2) * cos(abs(lambda1 - lambda2)))
#             g.add_edge((int(row[0]), int(row[1])), dist)
#
#         except:
#             pass

#optimized approach with knowledge of data layout

