from typing import Dict, List

from .basenode import BaseTasknode
from .fanout_task import FanOutTask
from .passthrough_task import PassTask


class Transition:
    def __init__(
        self,
        left: BaseTasknode,
        right: BaseTasknode | List[BaseTasknode] | None
    ):
        self.left = left
        self.right = right

    def __call__(self, **kwargs) -> BaseTasknode:
        if self.right:
            return self.right
        else:
            return self.left.execute(**kwargs)


class GraphCoreRunner:
    def __init__(
        self,
        entry: BaseTasknode,
        transitions: Dict[BaseTasknode,
                          BaseTasknode | List[BaseTasknode] | None]
    ):
        self.entry = entry
        self.transitions = transitions

    def exec(self, **kwargs):
        curr_task = self.entry
        params = dict(kwargs)
        while curr_task:
            resp = curr_task.execute(**params)
            next_task = self.transitions[curr_task]
            if (isinstance(curr_task, PassTask) and next_task):
                curr_task = next_task
                params |= resp.model_dump()
            elif isinstance(curr_task, FanOutTask):
                curr_task = resp.answer
            else:
                curr_task = None
        return resp
