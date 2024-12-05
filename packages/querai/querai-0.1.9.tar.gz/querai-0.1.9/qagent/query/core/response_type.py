from enum import Enum


class ResponseTypeEnum(str, Enum):
    TEXT = "text"
    CHOICES = "choice"
    OBJECT = "object"
    LIST = "list"
    DICTOFLIST = "dict-of-list"
