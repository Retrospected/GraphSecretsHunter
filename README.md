# GrapSecretsHunter

Searching for secrets on O365 based on keywords using Graph API.

## Requirements

The GraphSecretsHunter requires authentication to the Graph API service. You can leverage of existing tokens that are obtained from Office applications, for example via Red Team operations.

From a whitebox perspective you can take the token that is used by the [GraphAPI explorer](https://developer.microsoft.com/en-us/graph/graph-explorer). Login and grab your Authorization Token via Developer Toolbar or the `Access token` tab. Note that this session is only valid for a limited amount of time.

A third option is to use delegated permissions based on an Application Registration in Azure. The steps to set this up are best explained [here]('https://learn.microsoft.com/en-us/graph/auth-register-app-v2'). After registering an application you will need to grant consent to the relevant scopes of the specific entities. The scope requirements per entity are configured [here]('graphunter/entities/types.py'). 

## Usage

Copy .env.example to .env and update it with your token.

```
graphunter.py [-h] [-jwt] [-keywords KEYWORDS] [-e ENTITYTYPES] [-a] [-l] [-f FILTER] [-debug]

Crawling O365 for secrets using the GraphAPI.

options:
  -h, --help            show this help message and exit
  -jwt                  Using a JWT token obtained from the GraphAPI Explorer configured in your .env file. (default: False)
  -keywords KEYWORDS    Comma separated list of keywords.
  -e ENTITYTYPES, --entityTypes ENTITYTYPES
                        Comma separated list of O365 entity types. Use -l to get a list of available entity types.
  -a, --all             Use all entity types.
  -l, --list            List available O365 entity types.
  -f FILTER, --filter FILTER
                        Filter out items that have their webUrl start with these URL's. Takes a path to a file as input.
  -debug                Enable DEBUG output.
```