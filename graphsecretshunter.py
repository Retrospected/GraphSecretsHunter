#!/usr/bin/python3
#

import json
from graph import GraphClient
from graph import Search
from graph import Filter
from graph.jwt import JWTScopeVerifier
from dotenv import load_dotenv
from azure.identity import UsernamePasswordCredential
import os
import argparse
import logging
import csv

from graph.entities.enum import EntityEnum

load_dotenv()

__version__="1.0.0"

class GraphSecretsHunter:
    def __init__(self, token=None, keywords=None, entitytypes=None, filter=None):
        self.logger = logging.getLogger("GRAPHSECRETSHUNTER")

        self.token = token

        if token:
            client = GraphClient(token=token)
            try:
                authtest = client.get('/me')
                if authtest.status_code == 200:
                    user = authtest.json()
                    logger.info("Authentication succesful")
                else:
                    raise Exception("Unauthorized access")
            except Exception as e:
                logger.error(e)
                return
        
        search = Search(client)
        scopeVerifier = JWTScopeVerifier()
        o365results = {}

        for entityType in entitytypes:
            if not scopeVerifier.verify(token, entityType.value().scope):
                self.logger.error(f"The JWT scope does not include the required access to entity: {entityType.name}")
            else:
                o365results[entityType] = search.search(entityType, keywords)

        if filter:
            o365results = Filter(filter, o365results).filter()

        for entity in o365results.keys():
            logger.info(f"Writing out results of entity: {entity.name}")
            for keyword in o365results[entity]:
                for hit in o365results[entity][keyword]:
                    # TODO: I'm not writing the most interesting results, missing webUrl for sure. Have to expand this and make it dynamic somehow as well
                    self.writeResultCSV(entity, keyword, hit)

        if options.debug:
            self.writeResultJSON(o365results)

        logger.info("GraphSecretsHunter finished")


    def writeResultJSON(self,results):
        for entity in results.keys():
            with open(f'results_{entity.name}.json', 'w') as f:
                json.dump(results[entity], f)

    def writeResultCSV(self, entity, keyword, hit):
        file = f'results_{entity.name}.csv'

        if not os.path.exists(file):
            with open(file, 'w', newline='') as csvfile:
                headerwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                headerwriter.writerow(['entity','keyword','hitid','summary','weburl'])


        with open(file, 'a', newline='') as csvfile:
            hitId=hit['hitId']
            summary=hit['summary']
            webUrl=hit['resource']['webUrl']
            rowwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
            rowwriter.writerow([entity.name,keyword,hitId,summary,webUrl])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(add_help =  True, description = "Crawling O365 for secrets using the GraphAPI.")
    parser.add_argument("-auth", choices=["jwt", "appreg"], help='Using a GraphAPI access token or an app registration configured in your .env file.')
    parser.add_argument('-keywords', required=False, action='store', default=None, type=str,
                        help='Comma separated list of keywords (wildcard * is allowed).')
    parser.add_argument('-e', '--entityTypes', action='store', default=None, type=str,
                        help='Comma separated list of O365 entity types. Use -l to get a list of available entity types.')
    parser.add_argument('-a', '--all', default=True, action='store_true', help='Use all entity types.')
    parser.add_argument('-l', '--list', action='store_true', help='List available O365 entity types.')
    parser.add_argument('-f', '--filter', action='store', default=None, type=argparse.FileType('r'), help='Filter out items that have their webUrl start with these URL\'s. Takes a path to a file as input.')
    parser.add_argument('-debug', action='store_true', help='Enable DEBUG output.')

    options = parser.parse_args()

    logger = logging.getLogger("MAIN")
    if (options.debug):
        logging.basicConfig(format='%(name)-11s | %(asctime)s - %(levelname)-5s - %(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(name)-11s | %(asctime)s - %(levelname)-5s - %(message)s', level=logging.INFO)

    logger.info(f"GraphSecretsHunter - v{__version__}")
    filter = []
    if options.filter:
        with options.filter as file:
            filter = file.read().split("\n")

    if options.list:
        logger.info("The following O365 entities are available")
        [ logger.info(f"* { entity.name }") for entity in EntityEnum ]
        exit()
        
    if not options.keywords:
        logger.error("The following arguments are required: -keywords")
        exit()

    if options.auth != "jwt" and options.auth != "appreg":
        logger.error("Specify the desired authentication mode using -auth either by using '-auth jwt' or '-auth appreg'")
        exit()

    entityTypes = []

    if options.entityTypes:
        try:
            [ entityTypes.append(EntityEnum[entity]) for entity in options.entityTypes.split(",") ]
        except KeyError as e:
            logger.error(f"Could not find entityType: {e}. Use -l to get a list of available O365 entity types")
            exit()
    elif options.all:
        [ entityTypes.append(EntityEnum[entity.name]) for entity in EntityEnum ]

    logger.debug(f"Searching entity types: {[ entity.name for entity in entityTypes ]}")

    if options.auth == "jwt":
        GraphSecretsHunter(token=os.getenv("jwt"), keywords=options.keywords.split(','), entitytypes=entityTypes, filter=filter)
    elif options.auth == "appreg":
        CLIENT_ID=os.getenv("client_id")
        USERNAME=os.getenv("username")
        PASSWORD=os.getenv("password")

        app = UsernamePasswordCredential(
            client_id=CLIENT_ID, username=USERNAME ,password=PASSWORD
        )
        token = app.get_token('https://graph.microsoft.com/.default')
        GraphSecretsHunter(token=token[0], keywords=options.keywords.split(','), entitytypes=entityTypes, filter=filter)
else:
        exit()