#!/usr/bin/python3
#

import json
from graphunter import GraphClient
from graphunter import Search
from graphunter import Filter
from graphunter.jwt import JWTScopeVerifier
from dotenv import load_dotenv
import os
import argparse
import logging
import csv

from graphunter.entities.enum import EntityEnum

load_dotenv()

__version__="0.0.1"

class GrapHunter:
    def __init__(self, jwt=None, keywords=None, entitytypes=None, filter=None):
        self.logger = logging.getLogger("O365")

        if jwt:
            client = GraphClient(token=jwt)
            try:
                authtest = client.get('/me')
                if authtest.status_code == 200:
                    user = authtest.json()
                    logger.info("Authentication succesful")
                else:
                    raise Exception("Unauthorized access - JWT token expired?")
            except Exception as e:
                logger.error(e)
                return
        
        search = Search(client)
        scopeVerifier = JWTScopeVerifier()
        o365results = {}

        for entityType in entitytypes:
            if not scopeVerifier.verify(jwt, entityType.value().scope):
                self.logger.error(f"The JWT scope does not include the required access to entity: {entityType.name}")
            else:
                o365results[entityType] = search.search(entityType, keywords)

        if filter:
            o365results = Filter(filter, o365results).filter()

        for entity in o365results.keys():
            logger.info(f"Writing out results of entity: {entity.name}")
            for keyword in o365results[entity]:
                for hit in o365results[entity][keyword]:
                    self.writeResultCSV(entity, keyword, hit)

        if (options.debug):
            self.writeResultRaw(o365results)
 
        # TODO next: 
        # - figure out how to download the relevant content accordingly

        logger.info("O365 finished")

    def writeResultRaw(self,results):
        for entity in results.keys():
            with open(f'results_{entity.name}.raw', 'w') as f:
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
    parser.add_argument('-jwt', default=False, action='store_true', help='Using a JWT token obtained from the GraphAPI Explorer configured in your .env file.')
    parser.add_argument('-keywords', required=False, action='store', default=None, type=str,
                        help='Comma separated list of keywords.')
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

    logger.info(f"O365 - v{__version__}")
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

    if options.jwt:
        graphunter = GrapHunter(jwt=os.getenv("jwt"), keywords=options.keywords.split(','), entitytypes=entityTypes, filter=filter)
    else:
        exit()