import enum


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    ASSISTENT = "ASSISTENT"
    ANALIST = "ANALIST"
