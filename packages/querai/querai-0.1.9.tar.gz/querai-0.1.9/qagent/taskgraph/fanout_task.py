from __future__ import annotations

from typing import Dict

from qagent.udm import AnswerOption

from .basenode import BaseTasknode, TaskResponse


class FanOutTask(BaseTasknode):
    def __init__(self, book: Dict[str, FanOutTask]):
        """Return a predefined `Task` based on the `Answer`.

        The `Task` already equips the necessary prompt which optionally can use
        the answer.

        - It must also `carry on` the previous context e.g. parameters

        Typical flow
        ============

        So the `lookup` *must always* delegate to a pair of (prompt, executor)

        ```
                      LLM <---------------------------------------------.
                       ^                                                |
                       |                                                |
        PROMPT1 --> Executor1 --> ANSWER --> LOOKUP --> PROMPT_i        |
                                                    .     |             |
                                                     .    |             |
                                                      .   V             |
                                                       Executor_i ------/
        ```
        """
        self._lookupbook = book
        self._options = AnswerOption(choices=set(book.keys()))

    @property
    def book(self) -> dict:
        return self._lookupbook

    def execute(self, answer: str, **kwargs) -> TaskResponse:
        print(f"FANOUT switching on {answer}")
        assert answer in self._options.choices, f"Unknown choice: {answer}"
        return TaskResponse(
            answer=self.book[answer],
            status="OK"
        )
