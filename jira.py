""" Wrapper for the different jira endpoints that will be used as well 
as container for the interaction logic
"""
class jira(object):
    def __init__(self):
        import configparser
        import requests
        
        # To do http requests
        self.requests = requests
        
        # Data parsed from the config file
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.baseUrl = config['url']['baseurl']
        self.apiparturl = config['url']['apiparturl']
        
        self.userName = config['auth']['userName']
        self.apikey = config['auth']['apikey']
        
        self.boardListingUrl = "%s%s%s" % (self.baseUrl, self.apiparturl, config['boardListing']['urlpart'])
        self.boardListingRequestType = config['boardListing']['requesttype']
        
    def listBoards(self):
        return self.requests.get(self.boardListingUrl, auth=(self.userName, self.apikey))

""" Abstracts the process of converting the output from from the requests 
into more workable json objects
"""
class outputHandler():
    def __init__(self):
        import json
        
        self.json = json
        
    def outputToJson(self, data):
        data = data.text
        data = self.json.loads(data)
        return self.json.dumps(data, sort_keys=True, indent=4)

""" The application logic 

The classes above will be used here to serve the requests made to the 
script
"""
jira = jira()
outputHandler = outputHandler()

output = jira.listBoards()
print outputHandler.outputToJson(output)