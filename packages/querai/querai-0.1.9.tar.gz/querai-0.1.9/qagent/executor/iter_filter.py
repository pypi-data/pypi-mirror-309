from typing import Any, Dict, List

from pydantic import BaseModel

from qagent.executor.simple_sequential_executor import SimpleSingularExecutor
from qagent.llms.base_lm import BaseLLM


class ItemSequence(BaseModel):
    data: List[str]


class ItemMap(BaseModel):
    data: Dict[str, str]


_prompt_itemfilter = """Select the items from the input based on this rule:
{requirement}

Output JSON schema is:

    data: List[str], which is the selected items

Input:

{items}
"""

_prompt_itemmap = """Transform each item in the input to a new one based on this rule:
{requirement}

Output JSON schema is:

    data: Dict[str, str], where

    - key: the original item
    - value: the new item

Input:

{items}
"""


class IterFilterAgent(SimpleSingularExecutor):
    """Filter an iterable."""

    def __init__(
        self,
        llm: BaseLLM = None
    ):
        super().__init__(
            _prompt_itemfilter,
            response_type='object',
            object_constructor=ItemSequence,
            llm=llm
        )

    def filter_positive(self, requirement: str, items: List[str]) -> List[str]:
        resp = super().execute(requirement=requirement, items=str(items))
        answer: ItemSequence = resp.data
        return answer.data

    def filter_negative(self, requirement: str, items: List[str]) -> List[str]:
        """Remove items and return the rest.

        Parameters
        ----------
        items : List[str]
            _description_

        Returns
        -------
        List[str]
            The items that are not removed.
        """
        resp = super().execute(requirement=requirement, items=str(items))
        answer: ItemSequence = resp.data
        to_remove = set(answer.data)
        return [item for item in items if item not in to_remove]


class IterMappingAgent(SimpleSingularExecutor):
    """Map each item to a new value."""

    def __init__(
        self,
        llm: BaseLLM = None
    ):
        super().__init__(
            _prompt_itemmap,
            response_type='object',
            object_constructor=ItemMap,
            llm=llm
        )

    def execute(self, requirement: str, items: List[str]) -> Dict[str, str]:
        """Map each item to a new value.

        Parameters
        ----------
        items : List[str]

        Returns
        -------
        List[str]
            The new values.
        """
        resp = super().execute(requirement=requirement, items=str(items))
        mapping: ItemMap = resp.data
        return mapping.data
