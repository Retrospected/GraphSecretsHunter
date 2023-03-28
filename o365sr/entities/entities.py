class Entities():

    def __init__(self, keyword, size):
        self.keyword = keyword
        self.size = size
        self.entityType = ""

    def get_json(self, start=0):
        body={
                "requests": [
                    {
                        "entityTypes": [
                            self.entityType
                        ],
                        "query": {
                            "queryString": self.keyword
                        },
                        "from": start,
                        "size": self.size,
                        "fields": [
                            "webUrl",
                            "parentReference",
                            "siteId"
                        ]
                    }
                ]
        }

        return body