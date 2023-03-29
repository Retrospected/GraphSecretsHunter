from o365sr.entities.entities import Entities

class O365driveItem(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "driveItem"
        self.scope = ['Files.Read.All', 'Files.ReadWrite.All', 'Files.Read', 'Files.ReadWrite', 'Files.Read.Selected', 'Files.ReadWrite.AppFolder', 'Files.ReadWrite.Selected']

class O365drive(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "drive"
        self.scope = ['Files.Read.All', 'Files.ReadWrite.All', 'Files.Read', 'Files.ReadWrite', 'Files.Read.Selected', 'Files.ReadWrite.AppFolder', 'Files.ReadWrite.Selected']

class O365Site(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "site"
        self.scope = ['Sites.Read.All', 'Sites.ReadWrite.All', 'Sites.Read', 'Sites.ReadWrite', 'Sites.Manage.All', 'Sites.FullControl.All', 'Sites.Selected']

class O365list(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "list"
        self.scope = ['Sites.Read.All', 'Sites.ReadWrite.All', 'Sites.Read', 'Sites.ReadWrite', 'Sites.Manage.All', 'Sites.FullControl.All', 'Sites.Selected']

class O365listItem(Entities):
    def __init__(self):
        super().__init__()
        self.entityType = "listItem"
        self.scope = ['Sites.Read.All', 'Sites.ReadWrite.All', 'Sites.Read', 'Sites.ReadWrite', 'Sites.Manage.All', 'Sites.FullControl.All', 'Sites.Selected']
