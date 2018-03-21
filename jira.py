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

""" To make the requests to the jira plataform and return their raw 
output 

@param user string - the user name to sign into the jira platform
@param password string - the api key or password for the authentication
"""
class Requester():
    def __init__(self, user, password):
        import requests
        
        self.requests = requests
        self.user = user
        self.password = password
    
    """ Sends a generic get requests with the option to append values
    
    @param url string - url to make the requests to 
    @param payload dict - contains the values to be sent
    """
    def getRequest(self, url, payload = None):
        return self.requests.get(url, auth=(self.user, self.password), params=payload)
        
        
""" Wrapper for the different jira endpoints that will be used as well 
as container for the interaction logic
"""
class Jira(object):
    def __init__(self, Requester):
        import configparser
        
        # Parsing data from the config file
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        # Intantiates the requester class
        self.requester = Requester(config['auth']['userName'], config['auth']['apikey'])

        # Forms the base url to which all the api calls will be made
        self.jiraUrl = "%s%s" % (config['url']['baseurl'], config['url']['apiparturl'])
        
        # Url to query the boards available to the user
        self.boardListingUrl = "%s%s" % (self.jiraUrl, config['boardListing']['urlpart'])
        
        # Required to form the url with parms for issues by board
        self.issuesByBoard1 = config['issuesByBoard']['urlpart1']
        self.issuesByBoard2 = config['issuesByBoard']['urlpart2']
        
    def listBoards(self, payload):
        return self.requester.getRequest(self.boardListingUrl, payload)
        
    def issuesByBoardId(self, boardId, payload = None):
        url = "%s%s%s%s" % (self.jiraUrl, self.issuesByBoard1, boardId, self.issuesByBoard2)
        return self.requester.getRequest(url, payload)

""" The application logic 

The classes above will be used here to serve the requests made to the 
script
"""
import argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-a', '--action', type=str, help='The desired type of action to interact with jira', required=True)
parser.add_argument('--name', type=str, help='Name of the board', default=None)
parser.add_argument('--maxResults', type=str, help='Maximun amount of board to return by default 50', default=None)
parser.add_argument('--boardId', type=str, help='The id of the board')
parser.add_argument('--startAt', type=int, help='The desired start point of the sequence', default=None)
args = parser.parse_args()

jira = Jira(Requester)
outputHandler = OutputHandler()

def listBoards(payload):
    output = jira.listBoards(payload)
    return outputHandler.outputToJson(output)

def issuesByBoard():
    output = jira.issuesByBoardId(args.boardId, payload)
    return outputHandler.outputToJson(output)

if args.action == "listBoards":
    payload = {}
    if args.name is not None:
        payload['name'] = args.name
    if args.maxResults is not None:
        payload['maxResults'] = args.maxResults

    print listBoards(payload)
elif args.action == "issuesByBoard":
    payload = {}
    if args.startAt is not None:
        payload['startAt'] = args.startAt
    if args.maxResults is not None:
        payload['maxResults'] = args.maxResults
    print issuesByBoard()
else:
    print "Invalid action"