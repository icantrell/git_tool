from flask import Flask
from github_webhook import Webhook
import requests
import json
import sys
#import pickle
from getpass import getpass

#load conifurations
config = json.loads(open('configurations.txt','r').read())
#start flask app
app = Flask(__name__)

#set up webhook object
if 'secert' in config:
    #add secret from secret file if available.
    webhook = Webhook(app,open(config['secret'],'r').read())
else:
    webhook = Webhook(app)



#get user and hidden password
config['user'] = config['user'] if 'user' in config else input('repo owner username: ')
config['passwd'] = config['passwd'] if 'passwd' in config else getpass('owner password: ')





def git_pr_status(data):
    '''
    input: JSON data oject representing github pull request state
    output: state of the status of the pull request
    
    used for testing only.
    '''
    content = json.loads(requests.get(data['pull_request']['statuses_url']).content)
    return content[0]['state']




def git_post_status(data,status, discription):
    '''
    input: -JSON data oject representing github pull request state.
    -string whose value is the desired status of the pull request.
    -string for a discription of why the pull request has this status.
    output: None
    debug: prints contents returned from post
    
    changes corresponding github pull request's status.
    '''
    content = requests.post(data['pull_request']['statuses_url'],
                            auth=(config['user'],config['passwd']), 
                            json = {"state":status, "target_url":config['target_url'], "description":discription,"context":"label checker"})
  
    if config['debug']:
        print(content)

def git_pr_labels(data):
    '''
    input: -JSON data oject representing github pull request state.
    output:None
    '''
    for label in data['pull_request']['labels']:
        if label['name'] in config['valid_labels']:
            return
    
    git_post_status(data,'pending','Valid label('+data['label']['name']+') removed. Waiting for valid label.')
        
def git_check_labels(data):
    '''
    input: -JSON data oject representing github pull request state.
    output:None
    debug:print label contents
    
    When a label is changed function checks type of label against valid labels in config.
    If valid the status of the corresponding pull request is set to success.
    '''    
    if data['label']['name'] in config['valid_labels']:
        content = git_post_status(data,'success',"Valid label has been set.")
    else:
        content = git_post_status(data, 'pending', "Waiting for valid label to be set. Last label: " +
                        data['label']['name']+'. Is not in the list of valid labels: ' 
                        +','.join(config['valid_labels']) +'.')
    
    if config['debug'] and content:
        print(content['label'])     
        
def entry(data):
    '''
    input: -JSON data oject representing github pull request state.
    output:None
    
    entry point for request from github. Checks actions that were taken on pull request. 
    and inside sub-routines responds with a new status.
    '''
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

'''
#for capturing a pull request for testing.(should be on a labeled action)
@webhook.hook('pull_request') 
def on_pull_request(data):
    pickle.dump('json_test.txt', open('json_test.txt','wb'))
    
'''


if __name__ == "__main__":
    #run at 0.0.0.0 at port 80 by default
    app.run(host="0.0.0.0", port=80)
