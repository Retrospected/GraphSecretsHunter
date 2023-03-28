from o365sr.entities.entities import Entities

class O365driveItem(Entities):
    def __init__(self, keyword, size):
        super().__init__(keyword, size)
        self.entityType = "driveItem"

class O365Site(Entities):
    def __init__(self, keyword, size):
        super().__init__(keyword, size)
        self.entityType = "site"

class O365list(Entities):
    def __init__(self, keyword, size):
        super().__init__(keyword, size)
        self.entityType = "list"

class O365listItem(Entities):
    def __init__(self, keyword, size):
        super().__init__(keyword, size)
        self.entityType = "listItem"

class O365drive(Entities):
    def __init__(self, keyword, size):
        super().__init__(keyword, size)
        self.entityType = "drive"