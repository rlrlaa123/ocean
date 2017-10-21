# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import community
import pprint
import operator
import datetime
from nltk.corpus import stopwords
import re

class SNA():
    def __init__(self):
        self.classification = {
            # 'System SW':['Operating system', 'Embedded / Real Time operating system', 'Mobile operating system', 'PCServer operating system', 'Data management', 'DBMS', 'Data integration', 'Big Data Management', 'Data analysis', 'Storage', 'File system', 'Backing up your data', 'Storage archiving', 'SW Engineering tool', 'a programming language', 'Test quality qualification', 'SW Development Tool', 'Virtualization', 'Hypervisor for serverPC', 'Embedded Hypervisor', 'Resource virtualization', 'Virtualizing Applications', 'System security', 'Certified.', 'Access control', 'Intrusion detection / defence'],
            # 'Middleware':['Distributed system SW', 'Web application server', 'Unified Integration Solution', 'Real-time data processing', 'Distributed parallel processing', 'TP monitor', 'IT Resource Management', 'System management', 'SW Run SW', 'Network management', 'Manage IT Service Operations', 'Service platform', 'IoT platform', 'Cloud Services Platform', 'UI / UX framework', 'CDN', 'Network security', 'Network access control', 'Secure communication', 'Contradicting prevention / incident response', 'Security management'],
            # 'Application SW':[ 'Image processing', 'Image recognition / analysis', 'Video codec / streaming', 'Image-writing / editing / synthesis', 'CGCCS', '3D scanning / print', 'Modelling / animation / rendering', 'Virtual Reality / Augmented Reality', 'Holographic / Stereoscopy 3D', 'Virtual simulation', 'Content distribution', 'Content Protection', 'Content management', 'Content distribution', 'Natural language processing', 'Informationsequence response', 'Decision support', 'Language analysis / conversion', 'Conversational processing', 'Voice processing', 'Voice recognition', 'speech synthesis', 'Acoustic processing', 'Enterprise SW', 'Office wear', 'ERP', 'SCM', 'BI', 'CRM'],
            'Social-based industry': ['Construction', 'U-City', 'Farming', 'horticulture', 'livestock',
                                      'national-defense', 'Weapon', 'city', 'medical', 'Hospital', 'U-health'],
            'Service SW': ['Game', 'Public', 'disasters', 'disaster', 'living', 'Criminal', 'Medical welfare',
                           'Industrial', 'Environmental energy', 'Educational', 'Logistics', 'SCM', 'SCP', 'SCE',
                           'Shipping', 'Container-Carrier', 'Bulk-Carrier', 'Harbor', 'flight', 'Airport', 'Airline',
                           'Social-media', 'E-commerce'],
            'Manufacturing SW': ['Fashion clothes', 'Manufacturing', 'Avionics', 'Flight', 'shipbuilding',
                                 'e-navigation', 'E-Parth', 'Car', 'Connected', 'DTSW', 'ship']
        }

    def create_graph(self):
        path = ""
        data = pd.read_csv(path + '4/new_repo_topic_data4.csv', error_bad_lines=False, header=None,
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

    def match_edgelist(self,row):
        cluster = row[1:]
        edges = []
        # print cluster
        for index,i in enumerate(self.edges):
            for j in cluster:
                if i[0] == j:
                    for k in cluster:
                        if i[1] == k:
                            edges.append(i)
                            continue
                if i[1] == j:
                    for k in cluster:
                        if i[0] == k:
                            edges.append(i)
                            continue
        return cluster, edges

    def centrality(self):
        with open('4/community4.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cluster, edges = self.match_edgelist(row)
                edges = list(set(edges))

                C = nx.Graph()
                C.add_nodes_from(cluster)
                C.add_edges_from(edges)

                node_count=nx.number_of_nodes(C)
                edge_count=nx.number_of_edges(C)

                print node_count, edge_count

                cent = self.degree_centrality_custom(C)

                print cent

                with open('4/centrality4.csv','a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Community '+row[0],'Node: '+str(node_count),'Edge: '+str(edge_count)])
                    for i,j in cent.items():
                        writer.writerow([i,j])
                print 'Finished Community '+row[0]

    def clustering(self,save_filename):
        partition = community.best_partition(self.G)
        with open(save_filename,'a') as csvfile:
            writer = csv.writer(csvfile)
            for community_num in set(partition.values()):
                print "Community", community_num
                members = list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == community_num]
                print members
                writer.writerow([community_num]+members)

    def degree_centrality_custom(self,G):
        centrality = {}
        s = 1.0
        print G.degree()
        centrality = dict((n, d * s) for n, d in G.degree_iter())
        return centrality

    # self.centrality['Community #']
    def centrality_parser(self):

        self.centrality = {}
        community = ''

        with open('4.5/centrality4.5.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            for i in reader:
                if 'Community' in i[0]:
                    self.centrality[i[0]] = {}
                    community = i[0]
                    continue
                self.centrality[community][i[0]]=float(i[1])


    def highest_centrality(self):
        for i in sorted(self.centrality.keys()):

            sorted_cent = sorted(self.centrality[i].items(), key=operator.itemgetter(1), reverse=True)

            count = 0
            high_centrality = []
            for k in sorted_cent:
                high_centrality.append(k)
                count+=1
                if count == 50:
                    break

            with open('4/highest_centrality4.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                if len(i) == 11:
                    writer.writerow([int(i[10]),len(self.centrality[i].items())]+high_centrality)
                elif len(i) == 12:
                    writer.writerow([int(i[10:12]),len(self.centrality[i].items())]+high_centrality)
                elif len(i) == 13:
                    writer.writerow([int(i[9:13]),len(self.centrality[i].items())]+high_centrality)

    def match_created(self):
        topic = []
        created = []
        with open('topic_with_created_at.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for i in reader:
                created.append(i)
        # print created[1]
        with open('4.5/new_repo_topic_data4.5.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            for i,j in enumerate(reader):
                for k in j[1:]:
                    created[i].append(k)
        with open('topic_with_created_at4.5.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            for i in created:
                writer.writerow(i)

    def clustering_partially(self):
        with open('4/community4.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cluster, edges = self.match_edgelist(row)
                edges = list(set(edges))

                C = nx.Graph()
                C.add_nodes_from(cluster)
                C.add_edges_from(edges)

                node_count = nx.number_of_nodes(C)
                edge_count = nx.number_of_edges(C)

                print node_count, edge_count

                self.clustering('4/community_partial4.csv')
                cent = self.degree_centrality_custom(C)

                print cent

                with open('4/centrality_partial4_Community_'+row[0]+'.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Community ' + row[0], 'Node: ' + str(node_count), 'Edge: ' + str(edge_count)])
                    for i, j in cent.items():
                        writer.writerow([i, j])
                print 'Finished Community ' + row[0]

    def reading_classification(self):
        remove_text_list = [',', '.', '/', "'", '"', '(', ')', '{', '}', '[', ']']
        stop_words = set(stopwords.words('english'))
        self.classification = {
            'System SW':['System', 'Operating ', 'Embedded', 'os', 'Real-Time', 'PCServer', 'data', 'DBMS', 'data', 'big-data', 'system', 'integration', 'big', 'backup', 'archiving', 'engineering', 'test', 'development', 'virutalization', 'hypervisor', 'archive', 'tool', 'serverpc', 'resource', 'virtualizing', 'security', 'Certified.', 'Access control', 'Intrusion detection / defence', 'Middleware', 'Distributed system SW', 'Web application server', 'Unified Integration Solution', 'TP monitor', 'IoT platform', 'UI / UX framework', 'CDN', 'Network security', 'Network access control', 'Secure communication', 'real-time', 'distributed', 'run', 'cloud', 'parallel', 'it-resource', 'incident', 'prevention'],
            'Application SW':[ 'image', 'recognition', 'Video codec / streaming', 'Image-writing / editing / synthesis', 'CGCCS', '3D scanning / print', 'Modelling / animation / rendering', 'Virtual Reality / Augmented Reality', 'Holographic / Stereoscopy 3D', 'Virtual simulation', 'Content distribution', 'Content Protection', 'Content distribution', 'natural language', 'informationsequence', 'Decision support', 'language conversion', 'conversational', 'Voice recognition', 'speech synthesis', 'acoustic', 'enterprise', 'Office wear', 'ERP', 'SCM', 'BI', 'CRM'],
            # 'Social-based industry':[ 'Construction', 'U-City', 'Farming', 'horticulture', 'livestock', 'national-defense', 'Weapon', 'city', 'medical', 'Hospital', 'U-health'],
            # 'Service SW':['Game', 'Public', 'disasters', 'disaster', 'living', 'Criminal', 'Medical welfare', 'Industrial', 'Environmental energy', 'Educational', 'Logistics', 'SCM', 'SCP', 'SCE', 'Shipping', 'Container-Carrier', 'Bulk-Carrier', 'Harbor', 'flight', 'Airport', 'Airline', 'Social-media', 'E-commerce'],
            # 'Manufacturing SW':['Fashion clothes', 'Manufacturing', 'Avionics', 'Flight', 'shipbuilding', 'e-navigation', 'E-Parth', 'Car', 'Connected', 'DTSW', 'ship']
        }
        self.result = {}
        for i in self.classification:
            self.result[i]=[]
        for i in self.classification:
            for index,j in enumerate(self.classification[i]):
                for k in remove_text_list:
                    if k in j:
                        self.classification[i][index] = j.replace(k, ' ')
            # print classification[i]
            for j in self.classification[i]:
                for k in j.split(' '):
                    self.result[i].append(k.lower())

            self.result[i] = list(set(self.result[i]))
            if '' in self.result[i]:
                self.result[i].remove('')
            for j in stop_words:
                if j in self.result[i]:
                    self.result[i].remove(j)
        # from pprint import pprint
        # pprint(self.result)
        for i in self.result:
            with open('4.5/topic_with_created_at4.5.csv','r') as csvfile:
                reader = csv.reader(csvfile)
                with open('4.5/Classification/'+i+'.csv','a') as csvfile2:
                    writer = csv.writer(csvfile2)
                    for read in reader:
                        for j in self.result[i]:
                            if j in read:
                                writer.writerow([j]+read)

    def compare_classification(self):
        classification = {}
        for i in self.centrality:
            classification[i] = []
            for j in self.centrality[i]:
                for k in self.result:
                    # for l in self.result[k]:
                    #     regex = re.compile(l)
                    #     topic = regex.findall(j)
                    #     # print topic
                    #     if len(topic) == 0:
                    #         pass
                    #     elif len(topic) != 0:
                    #         classification[i].append(j+'&'+l)
                    if j in self.result[k]:
                        classification[i].append(j)
            # print classification[i]
        # print classification
        with open('4.5/compare_classification4.5.2.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            for i in classification:
                if len(classification[i]) != 0:
                    writer.writerow([i]+classification[i])
    def compare_highest_centrality_with_repository(self):
        highest_centrality = {}
        with open('4.5/highest_centrality4.5.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                highest_centrality[row[0]] = []
                for tuple in row[2:12]:
                    regex = re.compile("'(.+)'")
                    word = regex.findall(tuple)
                    if len(word) != 0:
                        highest_centrality[row[0]].append(word[0])
        print highest_centrality
        with open('4.5/topic_with_created_at4.5.csv','r') as csvfile:
            with open('4.5/compare_highest_centrality_with_repository4.5.csv','a') as csvfile2:
                writer = csv.writer(csvfile2)
                reader = csv.reader(csvfile)
                for row in reader:
                    # print row
                    for topic in row[1:]:
                        for highest in highest_centrality:
                            if topic in highest_centrality[highest]:
                                print highest
                                print topic
                                print row
                                # writer.writerow(['Community '+highest]+[topic]+row)



sna = SNA()
# sna.create_graph()
# sna.clustering('4/community_test.csv')
# sna.centrality()
# sna.centrality_parser()
# sna.highest_centrality()
# sna.match_created()
# sna.clustering_partially()
# sna.reading_classification()
# sna.compare_classification()
sna.compare_highest_centrality_with_repository()

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