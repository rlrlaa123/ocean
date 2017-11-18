import os
import csv
import collections
import networkx as nx
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

class EventAnalysis():
    def __init__(self):
        # Authenticate
        # self.client = bigquery.Client()
        service_account = 'Github-SNA-6cf7f22bd6fb.json'
        self.client = bigquery.Client.from_service_account_json(service_account)

    def explit(self):
        query = """
SELECT
  repo_name,
  event_type,
  actor_id AS issue_comment_actor,
  JSON_EXTRACT(JSON_EXTRACT(JSON_EXTRACT(event_payload, '$.issue'), '$.user'), '$.id') AS issue_actor
FROM
  `github-sna.SNA.15_17_eventactors`
WHERE
  event_type = 'IssueCommentEvent' and
  repo_name = 'naver/pinpoint'
  
"""
        query_job = self.client.query(query)
        result = query_job.result()
        for row in result:
            print (row)