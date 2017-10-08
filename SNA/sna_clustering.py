# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
from itertools import combinations
import operator
import community


class SNA():
    def __init__(self):
        path = ""
        data = pd.read_csv(path + '../../worldoss:ocean/Web_Crawler/test1.csv', error_bad_lines=False, header=None,
                           sep=",", delimiter='\n')  # pandas 라이브러리를 이용해서 SNA 분석 csv 파일 불러오기
        # Creating node list
        node = []
        for i in data.values:
            for j in i[0].split(',')[1:]:
                node.append(j)

        node = list(set(node))

        # Creating edge list
        self.edges = []

        for i in data.values:
            l = i[0].split(',')[1:]
            for j in range(len(l)):
                for k in range(j + 1, len(l)):
                    self.edges.append((l[j], l[k]))

        self.G = nx.Graph()
        self.G.add_nodes_from(node)
        self.G.add_edges_from(self.edges)

        print nx.number_of_nodes(self.G)
        print nx.number_of_edges(self.G)

    def centrality(self):
        with open('community_test.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cluster = row[1:]
                edges = []
                print cluster
                for i in self.edges:
                    for j in cluster:
                        if i[0] == j:
                            for k in cluster:
                                if i[1] == k:
                                    edges.append(i)
                        if i[1] == j:
                            for k in cluster:
                                if i[0] == k:
                                    edges.append(i)

                C = nx.Graph()
                C.add_nodes_from(cluster)
                C.add_edges_from(edges)

                node_count=nx.number_of_nodes(C)
                edge_count=nx.number_of_edges(C)

                cent = self.degree_centrality_custom(C)
                print cent
                with open('centrality_1.csv','a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Community '+row[0],'Node: '+str(node_count),'Edge: '+str(edge_count)])
                    for i,j in cent.items():
                        writer.writerow([i,j])
                print 'Finished Community'+row[0]

    def clustering(self):
        partition = community.best_partition(self.G)
        with open('community.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            for community_num in set(partition.values()):
                print "Community", community_num
                members = list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == community_num]
                print members
                writer.writerow([community_num]+members)

    def degree_centrality_custom(self,G):
        centrality = {}
        s = 1.0
        centrality = dict((n, d * s) for n, d in G.degree())
        return centrality

sna = SNA()
# sna.clustering()
sna.centrality()

# #drawing
# size = float(len(set(partition.values())))
# pos = nx.spring_layout(G)
# count = 0.
# for com in set(partition.values()) :
#     count = count + 1.
#     list_nodes = [nodes for nodes in partition.keys()
#                                 if partition[nodes] == com]
#     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 1,
#                                 node_color = str(count / size))
#

# nx.draw_networkx_edges(G,pos,alpha=0.5)

# plt.show()
