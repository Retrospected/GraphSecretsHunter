# GrapHunter

Searching for secrets on O365 based on keywords using Graph API.

## Usage

Login to https://developer.microsoft.com/en-us/graph/graph-explorer and grab your Authorization Token via Developer Toolbar or the `Access token` tab.\
Copy .env.example to .env and update it with your token.\
This session is valid for a limited amount of time.

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