from qagent.executor import SimpleSingularExecutor
from qagent.udm.base_schema import AnswerResponse

from .passthrough_task import PassTask


class LLMTask(PassTask):
    def __init__(self, label: str, prompt: str):
        super().__init__(label=label)
        self.llm = SimpleSingularExecutor(
            prompt=prompt,
            response_type="object",
            object_constructor=AnswerResponse
        )

    def execute(self, **kwargs) -> AnswerResponse:
        self._log(**kwargs)
        resp = self.llm.execute(**kwargs)
        print(f"LLMRESPON: {resp}")
        return AnswerResponse(
            answer=resp.data.answer,
            status="OK"
        )
