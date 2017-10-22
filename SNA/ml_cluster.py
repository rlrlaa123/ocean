import networkx as nx
import matplotlib.pyplot as plt
import csv

class ml_cluster():
    def ml_year(self):
        year = {
            '2008_2010': [],
            '2011_2013': [],
            '2014': [],
            '2015': [],
            '2016': [],
            '2017': [],
        }
        with open('4.2/Topic_Repository/ml_repository_4.2.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[3][0:4] == '2008' or row[3][0:4] == '2009' or row[3][0:4] == '2010':
                    year['2008_2010'].append(row)
                elif row[3][0:4] == '2011' or row[3][0:4] == '2012' or row[3][0:4] == '2013':
                    year['2011_2013'].append(row)
                elif row[3][0:4] == '2014':
                    year['2014'].append(row)
                elif row[3][0:4] == '2015':
                    year['2015'].append(row)
                elif row[3][0:4] == '2016':
                    year['2016'].append(row)
                elif row[3][0:4] == '2017':
                    year['2017'].append(row)
        return year

    def create_graph(self,year):
        nodes = []
        edges = []
        ml_list = self.ml_year()

        # print ml_list[year]
        for repo in ml_list[year]:
            for topic in repo[4:]:
                nodes.append(topic)

        nodes = list(set(nodes))

        for repo in ml_list[year]:
            for i in range(len(repo[4:])):
                for j in range(i+1, len(repo[4:])):
                    edges.append((repo[4:][i],repo[4:][j]))

        return nodes,edges

    def create_network(self):
        year = '2015'
        year_list = [
            '2008_2010',
            '2011_2013',
            '2014',
            '2015',
            '2016',
            '2017'
        ]
        for year in year_list:
            nodes, edges = self.create_graph(year)

            G = nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)

            print nx.info(G)

            self.cent = nx.degree_centrality(G)
            sorted_cent = self.highest_centrality()

            with open('4.2/ml/highest_centrality.csv','a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([year]+sorted_cent)

            # nx.draw_networkx(G,node_size=10,font_size=10,font_color='grey')
            # plt.show()

    def highest_centrality(self):
        import operator
        sorted_cent = sorted(self.cent.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_cent

ml = ml_cluster()
# ml.ml_year()
# ml.create_graph()
ml.create_network()
ml.highest_centrality()
# ml.nodes()
# ml.count_year()