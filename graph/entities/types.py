from graph.entities.entities import Entities

class O365driveItem(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "driveItem"
        self.scope = ['Files.ReadWrite.All', 'Files.Read', 'Files.ReadWrite']

class O365drive(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "drive"
        self.scope = ['Files.ReadWrite.All', 'Files.Read', 'Files.ReadWrite' ]

class O365Site(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "site"
        self.scope = ['Sites.ReadWrite.All', 'Sites.Read', 'Sites.ReadWrite' ]

class O365list(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "list"
        self.scope = ['Sites.ReadWrite.All', 'Sites.Read', 'Sites.ReadWrite' ]

class O365listItem(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "listItem"
        self.scope = [ 'Sites.ReadWrite.All', 'Sites.Read', 'Sites.ReadWrite' ]
