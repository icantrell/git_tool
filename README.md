# git_tool
Github tool for requiring labels in pull requests before merge.

# configurations
The configurations are listed in JSON.
valid_labels: a list of labels that are satisfactory for merging to be allowed. list of strings.
target_url: a target url for github users which provides full URL to the build output. string.
debug: Says where or not to show debug output. boolean value.
user(optional): username with access to repo. string.
passwd(optional): password for user with access to repo. string.

# setup
First you will need an application to forward ports. I used Ngrok for temporary testing.

To setup up this tool you will first need to setup the requirements in requirements.txt.

Once setup you should have flask available.

In the directory of the project you will need to set a local variable called FLASK_APP with the name of the entry file in this case it is "git_label_checker.py".
On windows the command to set env. variables is (no spaces)...
cmd$ set FLASK_APP=git_label_checker.py
cmd$ flask run -p <the port you are forwarding from>

Once the server starts running you will need to provide a username and password to a repo account that has access to repo where the webhooks are setup if they were not set in the config.
 
# setting up webhooks(don't skip)

when setting up webhooks the URL to send to will be <the web url where app is located>/postreceive
  
don't forget the /postreceive.
  
# testing
For testing I captured a github pull request with action 'labeled'. You will need to recapture another pull request if you want to run the test.

The pull request is pickled and stored in the json_test.py file.

There's some commented out code in git_label_checker.py that makes this easier.


