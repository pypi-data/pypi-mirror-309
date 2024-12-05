from enum import Enum
from typing import Literal, Set

from pydantic import BaseModel


class AnswerOption(BaseModel):
    choices: Set[str | Enum]


class AnswerResponse(BaseModel):
    answer: str


class AnswerResponseWithStatus(AnswerResponse):
    status: Literal["OK", "ERR"] = "OK"
