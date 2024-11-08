from enum import Enum

class Role(str, Enum):
    USER = "User"
    ADMIN = "Admin"
    MANAGER = "Manager"
