from typing import Any, Dict, List

from pydantic import BaseModel

from qagent.executor.simple_sequential_executor import SimpleSingularExecutor
from qagent.llms.base_lm import BaseLLM


class RecordList(BaseModel):
    data: List[Dict[str, Any]]


_prompt_recordlist = """Extract or generate a list of records for the input.

Output JSON schema is:

    data: List[Dict[<key>, <value>]], where

    - key: the required field
    - value: the value

You must follow these additional rules and requirements:

{requirements}

Input:

{text}
"""


class ObjectExtractionAgent(SimpleSingularExecutor):
    """Extract objects from text."""

    def __init__(
        self,
        llm: BaseLLM = None
    ):
        super().__init__(
            _prompt_recordlist,
            response_type='object',
            object_constructor=RecordList,
            llm=llm
        )

    def execute(self, requirement: str, text: str) -> List[Dict]:
        """Map each item to a new value.

        Parameters
        ----------
        items : List[str]

        Returns
        -------
        List[Dict]
            A list of records
        """
        resp = super().execute(requirements=requirement, text=text)
        return resp.data
