from flask import Flask
from github_webhook import Webhook
import requests
import json
import sys
import pickle

app = Flask(__name__)
webhook = Webhook(app)
#load conifurations
config = json.loads(open('configurations.txt','r').read())

#config['user'] = sys.argv[1] if len(sys.argv)>1 else input('repo username: ')
#config['passwd'] = sys.argv[2] if len(sys.argv)>2 else input('repo password: ')
config['user'] = 'icantrell'
config['passwd'] = 'krusalvere1'




def git_pr_status(data):
    print(data['pull_request']['statuses_url'])
    content = json.loads(requests.get(data['pull_request']['statuses_url']).content)
    return content[0]['state']




def git_post_status(data,status, discription):
    content = requests.post(data['pull_request']['statuses_url'],
                            auth=(config['user'],config['passwd']), 
                            json = {"state":status, "target_url":config['target_url'], "description":discription,"context":"label checker"})
  
    if config['debug']:
        print(content)

def git_pr_labels(data):
    for label in data['pull_request']['labels']:
        if label['name'] in config['valid_labels']:
            return
    
    git_post_status(data,'pending','Valid label('+data['label']['name']+') removed. Waiting for valid label.')
        
def git_check_labels(data):
    if data['label']['name'] in config['valid_labels']:
        content = git_post_status(data,'success',"Valid label has been set.")
    else:
        content = git_post_status(data, 'pending', "Waiting for valid label to be set. Last label: " +
                        data['label']['name']+'. Is not in the list of valid labels: ' 
                        +','.join(config['valid_labels']) +'.')
    
    if config['debug'] and content:
        print(content['label'])     
        
def entry(data):
    if data['action'] == 'opened':
        git_post_status(data, 'pending', "Waiting for valid label to be set.")
        
    if data['action'] == 'labeled':
        git_check_labels(data)
    
    if data['action'] == 'unlabeled': 
        git_pr_labels(data)
       
    return 'OK'

@app.route("/")
def payload():
    return 'OK'

@webhook.hook('pull_request') 
def on_pull_request(data):
    entry(data)
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)