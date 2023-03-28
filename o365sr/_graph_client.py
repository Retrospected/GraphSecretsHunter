from requests import Session

class GraphClient:
    def __init__(self, token, url="https://graph.microsoft.com/", API="1.0"):
        self.token = token
        self.url = url + f"v{API}"

        self.graph_session = self.create_graph_session()

    def get(self, url: str, **kwargs):
        return self.graph_session.get(self._graph_url(url), **kwargs)

    def post(self, url: str, **kwargs):
        return self.graph_session.post(self._graph_url(url), **kwargs)

    def create_graph_session(self):
        graph_session = Session()
        graph_session.headers = { "Authorization": "Bearer " + self.token}
        
        return graph_session

    def _graph_url(self, url):
        return self.url + url if (url[0] == '/') else url

