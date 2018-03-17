import argparse
import configparser

parser = argparse.ArgumentParser()
parser.add_argument('--baseUrl', type=str, help='The base url for the jira project')
parser.add_argument('--userName', type=str, help='The user name to use for authentication')
parser.add_argument('--apiKey', type=str, help='The api key for jira, will be used instead of a password')
args = parser.parse_args()

#print(args)

config = configparser.ConfigParser()
config['auth'] = {}
config['auth']['userName'] = args.userName
config['auth']['apiKey'] = args.apiKey
config['url'] = {}
config['url']['baseUrl'] = args.baseUrl # The jira url
config['url']['apiPartUrl'] = '/rest' # This is what follows the jira url
config['boardListing'] = {}
config['boardListing']['urlPart'] = '/agile/1.0/board'
config['issuesByBoard'] = {}
# <baseUrl>/rest/agile/1.0/<boardId>/293/issue 
config['issuesByBoard']['urlPart1'] = '/agile/1.0/board/'
config['issuesByBoard']['urlPart2'] = '/issue'
config['metadataForIssues'] = {}
config['metadataForIssues']['urlPart'] = '/api/2/issue/createmeta'
config['sendIssue'] = {}
config['sendIssue']['urlPart'] = '/api/2/issue'

with open('config.ini', 'w') as configfile:
  config.write(configfile)