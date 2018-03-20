""" Abstracts the process of converting the output from from the requests 
into more workable json objects
"""
class OutputHandler(object):
    def __init__(self):
        import json
        
        self.json = json
        
    def outputToJson(self, data):
        data = data.text
        data = self.json.loads(data)
        return self.json.dumps(data, sort_keys=True, indent=4)

""" To make the requests to the jira plataform and return their raw 
output 

@param user string - the user name to sign into the jira plataform
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
    def generalPurpose(self, url, payload = None):
        return self.requests.get(url, auth=(self.user, self.password), params=payload)
        
        
""" Wrapper for the different jira endpoints that will be used as well 
as container for the interaction logic
"""
class Jira(object):
    def __init__(self, Requester):
        import configparser
        
        # Data parsed from the config file
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.userName = config['auth']['userName']
        self.apikey = config['auth']['apikey']
        self.requester = Requester(self.userName, self.apikey)
        
        self.baseUrl = config['url']['baseurl']
        self.apiparturl = config['url']['apiparturl']
        
        self.boardListingUrl = "%s%s%s" % (self.baseUrl, self.apiparturl, config['boardListing']['urlpart'])
        self.boardListingRequestType = config['boardListing']['requesttype']
        
    def listBoards(self, payload):
        return self.requester.generalPurpose(self.boardListingUrl, payload)

""" The application logic 

The classes above will be used here to serve the requests made to the 
script
"""
import argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-a', '--action', type=str, help='The desired type of action to interact with jira', required=True)
parser.add_argument('--boardName', type=str, help='Name of the board', default=None)
parser.add_argument('--maxBoards', type=str, help='Maximun amount of board to return by default 50', default=50)
args = parser.parse_args()

jira = Jira(Requester)
outputHandler = OutputHandler()

def listBoards(payload):
    output = jira.listBoards(payload)
    return outputHandler.outputToJson(output)

def test():
    return 1

if args.action == "listBoards":
    payload = {}
    if args.boardName is not None:
        payload['name'] = args.boardName
    payload['maxResults'] = args.maxBoards

    print listBoards(payload)
elif args.action == "test":
    print test()
else:
    print "Invalid action"