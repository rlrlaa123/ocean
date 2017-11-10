# -*- coding: utf-8 -*-

## Bigquery credential file needed!
## Reference: https://cloud.google.com/bigquery/docs/authentication/service-account-file

import requests
import os
import csv
import collections
import networkx as nx
import scipy
import matplotlib.pyplot as plt


# create directory: os.mkdir
# if not os.path.exists(directory):
#     os.makedirs(directory)

from google.cloud import bigquery

PullRequestReviewCommentQuery = """
SELECT
  repo_name,
  event_type,
  actor_id AS pullrequest_comment_actor,
  JSON_EXTRACT(JSON_EXTRACT(JSON_EXTRACT(event_payload, '$.pull_request'), '$.user'), '$.id') AS pullreqeust_actor
FROM
  `github-sna.SNA.15_17_eventactors`
WHERE
  event_type = 'PullRequestReviewCommentEvent' and
  repo_name = """

CommitCommentQuery = """
SELECT
  repo_name,
  event_type,
  actor_id AS commit_comment_actor,
  JSON_EXTRACT(JSON_EXTRACT(event_payload, '$.comment'), '$.commit_id') AS commit_actor
FROM
  `github-sna.SNA.15_17_eventactors`
WHERE
  event_type = 'CommitCommentEvent' and
  repo_name = """

IssueCommentQuery = """
SELECT
  repo_name,
  event_type,
  actor_id AS issue_comment_actor,
  JSON_EXTRACT(JSON_EXTRACT(JSON_EXTRACT(event_payload, '$.issue'), '$.user'), '$.id') AS issue_actor
FROM
  `github-sna.SNA.15_17_eventactors`
WHERE
  event_type = 'IssueCommentEvent' and
  repo_name = """

QUERY = {
    'PullRequestReviewComment':PullRequestReviewCommentQuery,
    'CommitComment':CommitCommentQuery,
    'IssueComment':IssueCommentQuery,
}
REPOSITORY = [
    # 'jquery/jquery',
    'facebook/react',
    'twbs/bootstrap',
    'tensorflow/tensorflow',
    'd3/d3',
    'scikit-learn/scikit-learn',
    'airbnb/javascript',
    'angular/angular.js',
    'torvalds/linux',
    'apple/swift',
    'Microsoft/vscode',
    'Samsung/iotjs',
    'Samsung/GearVRf',
    'Samsung/TizenRT',
    'naver/pinpoint',
    'ncsoft/Unreal.js-core',
]
class UserDoesNotExistError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class EventAnalysis():
    def __init__(self):
        # Authenticate
        # self.client = bigquery.Client()
        service_account = 'Github-SNA-6cf7f22bd6fb.json'
        self.client = bigquery.Client.from_service_account_json(service_account)
    def collectEvent(self):
        # Iterate Repositories
        for repo in REPOSITORY:
            repo_name = repo.replace('/',':')
            # Create Directory
            if not os.path.exists(repo_name):
                os.makedirs(repo_name)
            print (repo_name)
            # Create csv file
            with open(repo_name+'/'+repo_name+'.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    ['repo_name', 'event_type', 'pullrequest_comment_actor', 'pullrequest_actor', 'commit_comment_actor',
                     'commit_actor', 'issue_comment_actor', 'issue_actor','weight'])
                # Iterate Queries
                for query in QUERY:
                    print ("Query Sent " + str(query) + '...')
                    # Send Query
                    query_job = self.client.query(QUERY[query]+"'"+repo+"'") # LIMIT 10 should be removed...

                    result = query_job.result()
                    data = []
                    count_list = []
                    for row in result:
                        if query == 'PullRequestReviewComment':
                            data.append([row[0],row[1],row[2],row[3],0,0,0,0])
                            count_list.append((row[2], row[3]))
                        elif query == 'CommitComment':
                            data.append([row[0],row[1],0,0,row[2],str(row[3]).replace('"',''),0,0])
                            count_list.append((row[2],row[3].replace('"','')))
                        elif query == 'IssueComment':
                            data.append([row[0],row[1],0,0,0,0,row[2],row[3]])
                            count_list.append((row[2], row[3]))

                    counter = collections.Counter(count_list)

                    # Write Results
                    for row in counter:
                        if query == 'PullRequestReviewComment':
                            writer.writerow([repo,query,row[0],row[1],0,0,0,0,counter[row]])
                        elif query == 'CommitComment':
                            commit_user_id = self.collectCommitUser(row[1],repo)
                            writer.writerow([repo,query,0,0,row[0],commit_user_id,0,0,counter[row]])
                        elif query == 'IssueComment':
                            writer.writerow([repo,query,0,0,0,0,row[0],commit_user_id,counter[row]])
                print ('Query Finished...\n')
    def snaAnalysis(self):
        for repo in REPOSITORY:
            repo_name = repo.replace('/',':')
            sna = {
                'PullRequestReviewComment': {
                    'node_list':[],
                    'edge_list':[],
                    'density':0
                },
                # 'CommitComment': {
                #     'node_list':[],
                #     'edge_list':[],
                #     'density':0
                # },
                'IssueComment': {
                    'node_list':[],
                    'edge_list':[],
                    'density':0
                },
            }
            with open(repo_name+'/'+repo_name+'.csv','r') as csvfile:
                reader = (csv.reader(csvfile))
                for row in reader:
                    if row[1] == 'PullRequestReviewComment':
                        sna['PullRequestReviewComment']['node_list'].append(row[2])
                        sna['PullRequestReviewComment']['node_list'].append(row[3])
                        sna['PullRequestReviewComment']['edge_list'].append((row[2],row[3],int(row[-1])))
                    # elif row[1] == 'CommitComment':
                    #     sna['CommitComment']['node_list'].append(row[4])
                    #     sna['CommitComment']['node_list'].append(row[5])
                    #     sna['CommitComment']['edge_list'].append((row[4], row[5], int(row[-1])))
                    elif row[1] == 'IssueComment':
                        sna['IssueComment']['node_list'].append(row[6])
                        sna['IssueComment']['node_list'].append(row[7])
                        sna['IssueComment']['edge_list'].append((row[6], row[7], int(row[-1])))

            for event in sna:
                print ('START '+repo_name+' '+event+'...')
                node_list = sna[event]['node_list']
                edge_list = sna[event]['edge_list']

                node_list = list(set(node_list))

                G = nx.DiGraph()
                G.add_nodes_from(node_list)
                G.add_weighted_edges_from(edge_list)
                print(nx.info(G))

                # print(edge_list)
                # nx.draw_networkx(G)
                # plt.show()

                user_indegree = nx.in_degree_centrality(G)
                print('FINISHED INDEGREE CENTRALITY...')
                user_outdegree = nx.out_degree_centrality(G)
                print('FINISHED OUTDEGREE CENTRALITY...')
                user_closeness = nx.closeness_centrality(G)
                print('FINISHED CLOSENESS CENTRALITY...')
                user_betweeness = nx.betweenness_centrality(G)
                print('FINISHED BETWEENESS CENTRALITY...')
                user_eigenvector = {}

                try:
                    user_eigenvector = nx.eigenvector_centrality_numpy(G)
                except:
                    print('EIGENVECTOR INVALID')
                    for i in node_list:
                        user_eigenvector[i] = 0
                print('FINISHED EIGENVECTOR CENTRALITY...')

                with open(repo_name + '/SNA_' + event + '_' + repo_name + '.csv', 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['user', 'indegree_centrality', 'outdegree_centrality', 'closeness_centrality', 'betweenness_centrality',
                                     'eigenvector_centrality'])

                    for user in node_list:
                        writer.writerow([
                            user,
                            user_indegree[user],
                            user_outdegree[user],
                            user_closeness[user],
                            user_betweeness[user],
                            user_eigenvector[user]
                        ])

                # print ('START DENSITY...')
                if event == 'PullRequestReviewComment':
                    sna[event]['density'] = nx.density(G)
                # elif event == 'CommitComment':
                #     sna[event]['density'] = nx.density(G)
                elif event == 'IssueComment':
                    sna[event]['density'] = nx.density(G)
                print(event+' Density: '+str(sna[event]['density']))
    def typeCount(self):
        for repo in REPOSITORY:
            print (repo+' Type Count Starts...')
            repo_name = repo.replace('/',':')
            user = []
            user_type = {}
            with open(repo_name+'/'+repo_name+'.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[1] == 'IssueComment':
                        user.append(row[6])
                        user.append(row[7])
                    elif row[1] == 'PullRequestReviewComment':
                        user.append(row[2])
                        user.append(row[3])

                user = list(set(user))

                for u in user:
                    user_type[u]={
                        'Issue':0,
                        'IssueComment':0,
                        'PullRequest':0,
                        'PullRequestComment':0,
                    }
            with open(repo_name+'/'+repo_name+'.csv') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[1] == 'IssueComment':
                        for u in user:
                            if u == row[6]:
                                user_type[u]['IssueComment']+=1 # row[8]
                        for u in user:
                            if u == row[7]:
                                user_type[u]['Issue']+=1
                    elif row[1] == 'PullRequestReviewComment':
                        for u in user:
                            if u == row[2]:
                                user_type[u]['PullRequestComment']+=1
                        for u in user:
                            if u == row[3]:
                                user_type[u]['PullRequest']+=1

            with open(repo_name+'/'+repo_name+'_TypeCount'+'.csv','a') as csvfile:
                writer = csv.DictWriter(csvfile,fieldnames=['user','Issue','IssueComment','PullRequest','PullRequestComment'])
                writer.writeheader()
                for user in user_type:
                    user_type[user]['user']=user
                    writer.writerow(user_type[user])
    def userCategorize(self):
        # 'Issue','IssueComment','PullRequest','PullRequestComment',
        #  0,0,0,1, Type 1
        #  0,0,1,0, Type 2
        #  0,0,1,1, Type 3
        #  0,1,0,0, Type 4
        #  0,1,0,1, Type 5
        #  0,1,1,0, Type 6
        #  0,1,1,1, Type 7
        #  1,0,0,0, Type 8
        #  1,0,0,1, Type 9
        #  1,0,1,0, Type 10
        #  1,0,1,1, Type 11
        #  1,1,0,0, Type 12
        #  1,1,0,1, Type 13
        #  1,1,1,0, Type 14
        #  1,1,1,1, Type 15
        for repo in REPOSITORY:
            print (repo+' User Categorize Starts...')
            repo_name = repo.replace('/',':')
            user_type = {}
            with open(repo_name+'/'+repo_name+'_TypeCount.csv','r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row[1] == 0 and row[2] == 0 and row[3] == 0 and row[4] != 0:
                        user_type[row[0]]='Type 1'
                    elif row[1] == '0' and row[2] == '0' and row[3] != '0' and row[4] == '0':
                        user_type[row[0]]='Type 2'
                    elif row[1] == '0' and row[2] == '0' and row[3] != '0' and row[4] != '0':
                        user_type[row[0]]='Type 3'
                    elif row[1] == '0' and row[2] != '0' and row[3] == '0' and row[4] == '0':
                        user_type[row[0]]='Type 4'
                    elif row[1] == '0' and row[2] != '0' and row[3] == '0' and row[4] != '0':
                        user_type[row[0]]='Type 5'
                    elif row[1] == '0' and row[2] != '0' and row[3] != '0' and row[4] == '0':
                        user_type[row[0]]='Type 6'
                    elif row[1] == '0' and row[2] != '0' and row[3] != '0' and row[4] != '0':
                        user_type[row[0]]='Type 7'
                    elif row[1] != '0' and row[2] == '0' and row[3] == '0' and row[4] == '0':
                        user_type[row[0]]='Type 8'
                    elif row[1] != '0' and row[2] == '0' and row[3] == '0' and row[4] != '0':
                        user_type[row[0]]='Type 9'
                    elif row[1] != '0' and row[2] == '0' and row[3] != '0' and row[4] == '0':
                        user_type[row[0]]='Type 10'
                    elif row[1] != '0' and row[2] == '0' and row[3] != '0' and row[4] != '0':
                        user_type[row[0]]='Type 11'
                    elif row[1] != '0' and row[2] != '0' and row[3] == '0' and row[4] == '0':
                        user_type[row[0]]='Type 12'
                    elif row[1] != '0' and row[2] != '0' and row[3] == '0' and row[4] != '0':
                        user_type[row[0]]='Type 13'
                    elif row[1] != '0' and row[2] != '0' and row[3] != '0' and row[4] == '0':
                        user_type[row[0]]='Type 14'
                    elif row[1] != '0' and row[2] != '0' and row[3] != '0' and row[4] != '0':
                        user_type[row[0]]='Type 15'
            with open(repo_name+'/'+repo_name+'_Categorized.csv','a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['user','type'])
                for user in user_type:
                    writer.writerow([user,user_type[user]])
    def categorizedUserCount(self):
        for repo in REPOSITORY:
            print (repo+' Categorized User Count Starts...')
            repo_name = repo.replace('/',':')
            type = []
            with open(repo_name+'/'+repo_name+'_Categorized.csv','r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    type.append(row[1])
                counter = collections.Counter(type)
                print (counter)
                print ('\n')
    def Request(self,url):
        id = 'rlrlaa123'
        pw = 'ehehdd009'
        return requests.get(url,auth=(id,pw))
    def collectCommitUser(self,commit_id,repo_name):
        try:
            url_commit_id = 'https://api.github.com/repos/'+repo_name+'/commits/'+str(commit_id)
            print (url_commit_id)
            content = self.Request(url_commit_id).json()
            if content['committer'] != None:
                user_login = content['committer']['login']
                url_commit_user = 'https://api.github.com/users/' + str(user_login)
                content = self.Request(url_commit_user).json()

                return content['id']
            else:
                raise UserDoesNotExistError('User Does Not Exist')
        except UserDoesNotExistError as e:
            user_name = content['commit']['committer']['name']
            return user_name
        except KeyError as e: # Limit에 도달 했을 시 어떻게 할지..
            print ('Limit reached...')
            sleep(60)



bquery = EventAnalysis()
bquery.collectEvent()
# bquery.snaAnalysis()
# bquery.typeCount()
# bquery.userCategorize()
# bquery.categorizedUserCount()