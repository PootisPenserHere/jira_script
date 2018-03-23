import argparse
import configparser
from os.path import expanduser

homePath = expanduser("~")
configFilePath = "%s%s%s" % (homePath, "/", ".config.ini")

parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group('Required named arguments')
requiredNamed.add_argument('--baseUrl', type=str, help='The base url for the jira project', required=True)
requiredNamed.add_argument('--userName', type=str, help='he user name to use for authentication', required=True)
requiredNamed.add_argument('--apiKey', type=str, help='The api key for jira, will be used instead of a password', required=True)
args = parser.parse_args()

config = configparser.ConfigParser()
config['auth'] = {}
config['auth']['userName'] = args.userName
config['auth']['apiKey'] = args.apiKey

config['url'] = {}
config['url']['baseUrl'] = args.baseUrl # The jira url
config['url']['apiPartUrl'] = '/rest' # This is what follows the jira url

config['boardListing'] = {}
config['boardListing']['urlPart'] = '/agile/1.0/board'

# <baseUrl>/rest/agile/1.0/<boardId>/293/issue 
config['issuesByBoard'] = {}
config['issuesByBoard']['urlPart1'] = '/agile/1.0/board/'
config['issuesByBoard']['urlPart2'] = '/issue'

config['metadataForIssues'] = {}
config['metadataForIssues']['urlPart'] = '/api/2/issue/createmeta'

config['sendIssue'] = {}
config['sendIssue']['urlPart'] = '/api/2/issue'

with open(configFilePath, 'w') as configfile:
  config.write(configfile)