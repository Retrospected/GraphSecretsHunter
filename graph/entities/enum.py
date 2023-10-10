from enum import Enum
from graph.entities.types import O365drive, O365driveItem, O365list, O365listItem, O365Site

class EntityEnum(Enum):
    drive = O365drive
    driveItem = O365driveItem
    list = O365list
    listItem = O365listItem
    site = O365Site