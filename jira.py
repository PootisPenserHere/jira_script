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
        
    def generalPurpose(self, url):
        return self.requests.get(url, auth=(self.user, self.password))
        
        
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
        
    def listBoards(self):
        return self.requester.generalPurpose(self.boardListingUrl)

""" The application logic 

The classes above will be used here to serve the requests made to the 
script
"""
import argparse

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('-a', '--action', type=str, help='The desired type of action to interact with jira', required=True)
args = parser.parse_args()

jira = Jira(Requester)
outputHandler = OutputHandler()

def listBoards():
    output = jira.listBoards()
    return outputHandler.outputToJson(output)

def test():
    return 1

if args.action == "listBoards":
    print listBoards()
elif args.action == "test":
    print test()
else:
    print "Invalid action"