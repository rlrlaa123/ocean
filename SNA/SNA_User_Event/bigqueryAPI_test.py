import os
import csv
import collections
import networkx as nx

class EventAnalysis():
    def __init__(self):
        # Authenticate
        # self.client = bigquery.Client()
        service_account = 'Github-SNA-6cf7f22bd6fb.json'
        self.client = bigquery.Client.from_service_account_json(service_account)