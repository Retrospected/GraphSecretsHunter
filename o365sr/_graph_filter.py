import logging
import traceback

from tqdm import tqdm

class Filter:
    def __init__(self,filter, o365results):
        self.logger = logging.getLogger("FILTER")
        self.filterList = filter
        self.o365results = o365results

    def filter(self):
        self.logger.info("Filtering out items based on a blacklist of URL's")

        returnResults = {}

        for entity in self.o365results.keys():
            returnResults[entity] = {}
            for keyword in self.o365results[entity]:
                returnResults[entity][keyword] = []
                self.logger.info(f"Filtering {entity} matching keyword {keyword}")
                for hit in tqdm(self.o365results[entity][keyword]):
                    try:
                        if hit['resource']['webUrl'].startswith(tuple(self.filterList)):
                            self.logger.debug("Found a filtered URL in the webUrl of the item, so removing this entry.")
                        else:
                            returnResults[entity][keyword].append(hit)
                    except Exception as e:
                        self.logger.info(f"Exception while filtering permissions for {hit['hitId']}")
                        self.logger.info(traceback.print_exc()) 
        
        return returnResults
