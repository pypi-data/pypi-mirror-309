from abc import ABC, abstractmethod

from qagent.udm.base_schema import AnswerResponseWithStatus


class BaseTasknode(ABC):
    """Base class of a `Task Node` in an execution graph."""

    @abstractmethod
    def execute(self, **kwargs) -> AnswerResponseWithStatus:
        raise NotImplementedError

    def __str__(self):
        return self.__doc__

    def _log(self, **kwargs):
        print(f"{self.label} going ...")
        for kw, arg in kwargs.items():
            print(f"   {kw} --> {arg}")


class TaskResponse:
    def __init__(self, answer: BaseTasknode, status: str):
        self.answer = answer
        self.status = status
