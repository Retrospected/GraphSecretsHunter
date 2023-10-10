import logging
import traceback

from tqdm import tqdm


class Filter:
    def __init__(self,filter, o365results):
        self.logger = logging.getLogger("FILTER")
        self.filterList = filter
        self.o365results = o365results

    def filter(self):
        self.logger.debug("Filtering out items based on a blacklist of URLs")

        returnResults = {}

        for entity in self.o365results.keys():
            returnResults[entity] = {}
            for keyword in self.o365results[entity]:
                returnResults[entity][keyword] = []
                self.logger.debug(f"Filtering {entity.name} matching keyword {keyword}")
                for hit in tqdm(self.o365results[entity][keyword]):
                    try:
                        if hit['resource']['webUrl'].startswith(tuple(self.filterList)):
                            pass
                        else:
                            returnResults[entity][keyword].append(hit)
                    except Exception as e:
                        self.logger.error(f"Exception while filtering permissions for {hit['hitId']}")
                        self.logger.error(traceback.print_exc()) 
        
        return returnResults
