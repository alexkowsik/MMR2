from graph import GraphAsList
import csv


g = GraphAsList()
with open("maps/test_nodes.csv",newline="") as file:    #open file
    reader = csv.reader(file,delimiter=",")
    for row in reader:                                  #returns rows
        g.add_node(int(row[0]),0 ,int(row[1]),int(row[2]))                #row[0]: node,[1]:breitengrad,[2]:laengengrad

with open("maps/test_edges.csv", newline="") as file:  # open file
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        g.add_edge( (int(row[0]),int(row[1])) )

g.print_graph()