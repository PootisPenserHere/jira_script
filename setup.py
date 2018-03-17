import argparse
import configparser

parser = argparse.ArgumentParser()
parser.add_argument('--baseUrl', type=str, help='The base url for the jira project')
parser.add_argument('--userName', type=str, help='The user name to use for authentication')
parser.add_argument('--apiKey', type=str, help='The api key for jira, will be used instead of a password')
args = parser.parse_args()


config = configparser.ConfigParser()
config['jira'] = {}
config['jira']['baseUrl'] = args.baseUrl
config['jira']['userName'] = args.userName
config['jira']['apiKey'] = args.apiKey

with open('config.ini', 'w') as configfile:
  config.write(configfile)