
import logging

from requests import HTTPError
from graphunter.entities.enum import EntityEnum
import traceback

class Search:
    def __init__(self, GraphClient, size=499):
        self.logger = logging.getLogger("SEARCH")
        self.client = GraphClient
        self.size = size


    def search(self, O365Item, keywords, start=0):
        if not isinstance(O365Item, EntityEnum):
            raise TypeError('O365Item must be an instance of O365Items Enum')

        results={}

        for keyword in keywords:
            try:
                moreResults = True
                start = 0
                results_keyword = []
                self.logger.info(f"Searching {O365Item.name} for keyword {keyword}")
                while moreResults:
                    self.logger.debug(f"Using startpoint {start} and max size {self.size}.")

                    json_body = O365Item.value().get_json(keyword, self.size, start)

                    max_retries = 3
                    retry_count = 0

                    while retry_count < max_retries:
                        try:
                            response = self.search_page(json_body)
                            response.raise_for_status()
                        except HTTPError as exc:
                            retry_count += 1
                            status_code = exc.response.status_code
                        else:
                            status_code = 200
                            break

                    if status_code != 200:
                        raise HTTPError(self.client.url+"/search/query", status_code, "Error while performing request to server.")

                    results_page = response.json()
                    total = results_page["value"][0]['hitsContainers'][0]['total']
                    self.logger.debug(f"In progress of retrieving a total of {total} results")

                    if total:
                        [ results_keyword.append(hit) for hit in results_page["value"][0]['hitsContainers'][0]['hits'] ] 
                        moreResults = results_page["value"][0]['hitsContainers'][0]['moreResultsAvailable']

                        start = start + self.size + 1
                        total = results_page["value"][0]['hitsContainers'][0]['total']

                    else:
                        moreResults = False

                self.logger.info(f"Search completed with {len(results_keyword)} results")
                results[keyword] = results_keyword
            except HTTPError as exc:
                if status_code:
                    code = status_code
                else:
                    code = exc.response.status_code
                if code == 403 or code == 401:
                    self.logger.error(f"Access denied to query entity: {O365Item.name}. This entity is not part of the scope of your Access Token.")
                else:
                    self.logger.error(f"Exception for {O365Item.name} for keyword {keyword} with startpoint {start} and max size {self.size}.")
                    self.logger.error(f"JSON payload: {json_body}")
                    self.logger.error(f"HTTP status code received {response.status_code} and content {response.content}")
                    self.logger.error(traceback.print_exc())
            except Exception as e:
                self.logger.error(f"Exception for {O365Item.name} for keyword {keyword} with startpoint {start} and max size {self.size}.")
                self.logger.error(f"JSON payload: {json_body}")
                self.logger.error(f"HTTP status code received {response.status_code} and content {response.content}")
                self.logger.error(traceback.print_exc())

        return results
    
    def search_page(self, json_body):
        return self.client.post('/search/query',json=json_body)