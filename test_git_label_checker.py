import json
import git_label_checker as test
import pickle

test_json = pickle.load(open('json_test.txt','rb'))

def test_pr_opened_status():
    test_json['action'] = 'opened'
    test.entry(test_json)
    assert(test.git_pr_status(test_json) == 'pending')
    
def test_pr_labeled_status():
    test_json['action'] = 'labeled'
    test.entry(test_json)
    assert(test.git_pr_status(test_json) == 'success')
    
def test_pr_unlabeled_status():
    test_json['action'] = 'unlabeled'
    test_json['pull_request']['labels']=[]
    test.entry(test_json)
    assert(test.git_pr_status(test_json) == 'pending')
    
#so that it ends on success and starts on pending
def test_pr_labeled_status2():
    test_json['action'] = 'labeled'
    test.entry(test_json)
    assert(test.git_pr_status(test_json) == 'success')