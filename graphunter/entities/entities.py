class Entities():

    def __init__(self):
        self.entityType = ""
        self.scope = []

    def get_json(self, keyword, size, start=0):
        body={
                "requests": [
                    {
                        "entityTypes": [
                            self.entityType
                        ],
                        "query": {
                            "queryString": keyword
                        },
                        "from": start,
                        "size": size,
                        "trimDuplicates": True,
                        "fields": [
                            "webUrl",
                            "parentReference",
                            "siteId"
                        ]
                    }
                ]
        }

        return body