import configparser
config = configparser.ConfigParser()

config['jira'] = {}
config['jira']['baseUrl'] = ''

with open('config.ini', 'w') as configfile:
  config.write(configfile)