from enum import Enum
from o365sr.entities.types import *

class EntityEnum(Enum):
    drive = O365drive
    driveItem = O365driveItem
    list = O365list
    listItem = O365listItem
    site = O365Site