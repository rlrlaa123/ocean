import urllib.request
import json
import csv
import re
import datetime
from time import sleep
import requests
import time

class CollectCommitUser():
    def Request(self,url):
        id = 'rlrlaa123'
        pw = 'ehehdd009'
        # auth = base64.encodestring(id + ':' + pw)
        auth = id+':'+pw
        return requests.get(url,auth=(id,pw))

    def collectCommitUser(self):
        url_name = 'https://api.github.com/repos/jquery/jquery/commits/866ba43d0a8cd9807a39483df48d9366558cb6dd'

        print (url_name)
        content = self.Request(url_name).headers['X-RateLimit-Reset']
        print (time.time())
        print (content)
        sleeptime = float(content)-float(time.time())
        current_time = datetime.datetime.fromtimestamp(time.time())
        print(current_time.strftime('%Y-%m-%d %H:%M:%S'))
        rate_time = datetime.datetime.fromtimestamp(float(content))
        print (rate_time.strftime('%Y-%m-%d %H:%M:%S'))
        remaining_time = float(content)-float(time.time())
        print (remaining_time)
        wait_time = datetime.datetime.fromtimestamp(remaining_time)
        print (wait_time.strftime('%Y-%m-%d %H:%M:%S'))
        # print (sleeptime)
        # time.sleep(sleeptime)
        # user_name = content['commit']['committer']['name']
        # print (user_name)
        # url_id = 'https://api.github.com/users/'+str(user_name)
        # print (url_id)
        # content = self.Request(url_id).json()
        # print (content['id'])


collector = CollectCommitUser()
collector.collectCommitUser()