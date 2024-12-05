from __future__ import annotations

from qagent.udm.base_schema import AnswerResponse

from .basenode import BaseTasknode


class PassTask(BaseTasknode):
    def __init__(self, label: str = ""):
        self.label = label

    def execute(self, **kwargs) -> AnswerResponse:
        self._log(**kwargs)
        return AnswerResponse(
            answer=self.label,
            status="OK"
        )
