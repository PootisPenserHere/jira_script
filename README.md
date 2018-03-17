# Setting up the project

## To install the dependencies 
```sh
sudo pip install --upgrade pip
pip install -r requirements.txt
```

# Configuring the enviroment
```sh
python setup.py --baseUrl <jira url> --userName <jira username> --apiKey <jira api key>
```

# Parameters
|   Option   | Type   | Value                                                                   |
|:----------:|--------|-------------------------------------------------------------------------|
| --baseUrl  | String | The url to acces the jira project: example.com:8080 or domain.jira.net  |              |
| --userName | String | The user name used to login                                             |
| --apiKey   | String | The generated api key from the jira interface, will be used as password |