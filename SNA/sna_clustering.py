# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from itertools import combinations
import operator
import community


path = ""
data = pd.read_csv(path + '../Web_Crawler/Topic_data.csv',error_bad_lines=False,header=None,sep=",",delimiter='\n')     # pandas 라이브러리를 이용해서 SNA 분석 csv 파일 불러오기

node = []

for i in data.values:
    for j in i[0].split(',')[1:]:

        node.append(j)
node = list(set(node))

l=[]
for i in data.values:
    l.append(i[0].split(',')[1:])
edge = [(i[0],j) for i in l for j in i[1:]]

G = nx.Graph()
G.add_nodes_from(node)
G.add_edges_from(edge)

print nx.number_of_nodes(G)
print nx.number_of_edges(G)

partition = community.best_partition(G)

#drawing
for i in set(partition.values()):
   print "Community", i
   members = list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == i]
   print members

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos,alpha=0.5)

plt.show()
