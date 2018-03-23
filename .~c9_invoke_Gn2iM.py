""" Abstracts the process of converting the output from the requests 
into more workable json objects
"""
class OutputHandler(object):
    def __init__(self):
        import json
        
        self.json = json
        
    """ Turns a object into the string form of a json and returns it as 
    a beautified json
    
    @param data dict
    """
    def outputToJson(self, data):
        data = data.text
        data = self.json.loads(data)
        return self.json.dumps(data, sort_keys=True, indent=4)
        
    def dictToJson(self, data):
        return self.json.dumps(data, sort_keys=True, indent=4)

""" To make the requests to the jira plataform and return their raw 
output 

@param user string - the user name to sign into the jira platform
@param password string - the api key or password for the authentication
"""
class Requester():
    def __init__(self, user, password):
        import requests
        import json
        
        self.json = json
        self.requests = requests
        self.user = user
        self.password = password
        
        # json header for the requests
        self.jsonContentType = {'Content-type': 'application/json'}
    
    """ Sends a generic get requests with the option to append values
    
    @param url string - url to make the requests to 
    @param payload dict - contains the values to be sent
    """
    def getRequest(self, url, payload = None):
        return self.requests.get(url, auth=(self.user, self.password), params=payload)
        
    """ Sends a generic post request with a json object as its request body
    
    @param url string - url to make the requests to 
    @param payload dict - contains the values to be sent
    """
    def postRequestWithJsonBody(self, url, payload = None):
        # Converts the payload to josn
        payload = self.json.dumps(payload)
        return self.requests.post(url, auth=(self.user, self.password), data=payload, headers=self.jsonContentType)
        
        
""" Wrapper for the different jira endpoints that will be used as well 
as container for the interaction logic
"""
class Jira(object):
    def __init__(self, Requester):
        import configparser
        from os.path import expanduser
        
        # Parsing data from the config file
        homePath = expanduser("~")
        configFilePath = "%s%s%s" % (homePath, "/", ".config.ini")
        config = configparser.ConfigParser()
        config.read(configFilePath)
        
        # Intantiates the requester class
        self.requester = Requester(config['auth']['userName'], config['auth']['apikey'])

        # Forms the base url to which all the api calls will be made
        self.jiraUrl = "%s%s" % (config['url']['baseurl'], config['url']['apiparturl'])
        
        # Url to query the boards available to the user
        self.boardListingUrl = "%s%s" % (self.jiraUrl, config['boardListing']['urlpart'])
        
        # Required to form the url with parms for issues by board
        self.issuesByBoard1 = config['issuesByBoard']['urlpart1']
        self.issuesByBoard2 = config['issuesByBoard']['urlpart2']
        
        # Url to query the metadata for the issues
        self.metadataForIssuesUrl = "%s%s" % (self.jiraUrl, config['metadataForIssues']['urlpart'])
        
        # Url to create a new issue
        self.createNewIssueUrl = "%s%s" % (self.jiraUrl ,config['sendIssue']['urlpart'])
        
    def listBoards(self, payload):
        return self.requester.getRequest(self.boardListingUrl, payload)
        
    def issuesByBoardId(self, boardId, payload = None):
        url = "%s%s%s%s" % (self.jiraUrl, self.issuesByBoard1, boardId, self.issuesByBoard2)
        return self.requester.getRequest(url, payload)
        
    def metadataForIssues(self):
        return self.requester.getRequest(self.metadataForIssuesUrl)
    
    # Creates a issue and if the user data was sent asigns it to them
    def sendNewIssue(self, projectId, summary, description, issuetype, userName, email):
        # Creates a dictionary with the sent data to submit a new issue
        body = {}
        body['fields'] = {}
        body['fields']['summary'] = summary
        body['fields']['description'] = description
        body['fields']['project'] = {}
        body['fields']['project']['id'] = projectId
        body['fields']['issuetype'] = {}
        body['fields']['issuetype']['id'] = issuetype
        
        if userName is not None and email is not None:
            body['fields']['assignee'] = {}
            body['fields']['assignee']['name'] = userName
            body['fields']['assignee']['key'] = userName
            body['fields']['assignee']['emailAddress'] = email
        
        return self.requester.postRequestWithJsonBody(self.createNewIssueUrl, body)

""" The application logic 

The classes above will be used here to serve the requests made to the 
script
"""
import argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-a', '--action', type=str, help='The desired type of action to interact with jira', required=True)
parser.add_argument('--name', type=str, help='Name of the board', default=None)
parser.add_argument('--maxResults', type=str, help='Maximun amount of board to return, by default 50', default=None)
parser.add_argument('--boardId', type=str, help='The id of the board')
parser.add_argument('--startAt', type=int, help='The desired start point of the sequence', default=None)
parser.add_argument('--projectId', type=int, help='The id of the project', default=None)
parser.add_argument('--summary', type=str, help='A summary of the issue', default=None)
parser.add_argument('--description', type=str, help='A description of the issue', default=None)
parser.add_argument('--issuetype', type=int, help='The id of the issue, can be taken from the issue metadata', default=None)
parser.add_argument('--userName', type=str, help='Username of the user being handled', default=None)
parser.add_argument('--email', type=str, help='Email of the user being handled', default=None)
args = parser.parse_args()

jira = Jira(Requester)
outputHandler = OutputHandler()

""" This methods interact directly with the classes and are
called depending on the action argument sent by the user 
"""
def listBoards(payload):
    output = jira.listBoards(payload)
    return outputHandler.outputToJson(output)

def issuesByBoard():
    output = jira.issuesByBoardId(args.boardId, payload)
    return outputHandler.outputToJson(output)

def metadataForIssues():
    output = jira.metadataForIssues()
    return outputHandler.outputToJson(output)

def createIssue(projectId, summary, description, issuetype, userName, email):
    output = jira.sendNewIssue(projectId, summary, description, issuetype, userName, email)
    return outputHandler.outputToJson(output)
    #return output

""" This section determines what's the desired action to perform by the 
user and processes the aeguments taken from the scrip calling according 
to the action
"""
# Listing boards
if args.action == "listBoards":
    payload = {}
    if args.name is not None:
        payload['name'] = args.name
    if args.maxResults is not None:
        payload['maxResults'] = args.maxResults

    print listBoards(payload)

# Listing issues by board 
elif args.action == "issuesByBoard":
    payload = {}
    if args.startAt is not None:
        payload['startAt'] = args.startAt
    if args.maxResults is not None:
        payload['maxResults'] = args.maxResults
    print issuesByBoard()

# Lists the met available adata for the issues
elif args.action == "metadataForIssues":
    print metadataForIssues()
    
# Creating a new issue
elif args.action == "createIssue":
    print createIssue(args.projectId, args.summary, args.description, args.issuetype, args.userName, args.email)

# If the action is not mapped
else:
    print "Invalid action"