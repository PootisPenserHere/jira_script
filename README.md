# Jira from shell 
### This is a tool meant to be run from the  command line with the intention of being simple, light and easy to manage hence all contained within a single file.

### The script allows to interact with the jira cloud platform in a way that it's easy to create a wrapper around it to place one's logic over it for virtually any purpose be it generating statistics about issues, opening new issues, and many more.

# Setting up the project

### While most python installations should already contain the necessary modules by default they can be installed by running the following command
```sh
sudo pip install --upgrade pip
pip install -r requirements.txt
```

## Configuring the enviroment
### This will create a file named .config.ini which will be stored in the home directory of the user
```sh
python setup.py --baseUrl <jira url> --userName <jira username> --apiKey <jira api key>
```

### Parameters
|   Option   | Type   | Value                                                                   |
|:----------:|--------|-------------------------------------------------------------------------|
| --baseUrl  | String | The url to acces the jira project: example.com:8080 or domain.jira.net  |              |
| --userName | String | The user name used to login                                             |
| --apiKey   | String | The generated api key from the jira interface, will be used as password |

### After the config file has been created the config scrip may be removed

### Optionally the jira script may be moved to the user's bin folder to be called as a shell command  
```sh
cp jira.py $HOME/bin/
chmod +x $HOME/bin/jira.py
```

# Using the script 

### Basic usage
```sh
python jira.py
```

## Listing boards 

### Parameters
| Option       | type   | Value                                             | Required |
|--------------|--------|---------------------------------------------------|----------|
| -a, --action | String | listBoards                                        | Yes      |
| --boardName  | String | The name or part of the name of the desired board | No       |
| --maxBoards  | Int    | Default to 50                                     | No       |

## Issues by board 
| Option       | type   | Value                                 | Required |
|--------------|--------|---------------------------------------|----------|
| -a, --action | String | issuesByBoard                         | Yes      |
| boardId      | Int    | The id of the board                   | Yes      |
| startAt      | Int    | The record from which the query start |          |
| maxResults   | Int    | Max number of results, by default 50  |          |