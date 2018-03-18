""" Wrapper for the different jira endpoints that will be used as well 
as container for the interaction logic
"""
class jira(object):
    def __init__(self):
        import configparser
        import requests
        import json
        
        # To do http requests
        self.requests = requests
        
        self.json = json
        
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

""" The application logic 

The classes above will be used here to serve the requests made to the 
script
"""
import json

jira = jira()
output = jira.listBoards()
output = output.text
output = json.loads(output)
print json.dumps(output, sort_keys=True, indent=4)