from typing import Optional, List, Union
from pydantic import BaseModel, Field

from murnitur.annotation.evaluation.utils import get_or_create_event_loop, prettify_list
from murnitur.annotation.evaluation.metrics.utils import (
    print_intermediate_steps,
    validate_conversational_test_case,
    trimAndLoadJson,
    check_llm_test_case_params,
    initialize_model,
)
from murnitur.annotation.evaluation.test_case import (
    LLMTestCase,
    LLMTestCaseParams,
    ConversationalTestCase,
)
from murnitur.annotation.evaluation.metrics import BaseMetric
from murnitur.annotation.evaluation.models import DeepEvalBaseLLM
from murnitur.annotation.evaluation.metrics.contextual_recall.template import (
    ContextualRecallTemplate,
)
from murnitur.annotation.evaluation.metrics.indicator import metric_progress_indicator

required_params: List[LLMTestCaseParams] = [
    LLMTestCaseParams.INPUT,
    LLMTestCaseParams.ACTUAL_OUTPUT,
    LLMTestCaseParams.RETRIEVAL_CONTEXT,
    LLMTestCaseParams.EXPECTED_OUTPUT,
]


class ContextualRecallVerdict(BaseModel):
    verdict: str
    reason: str = Field(default=None)


class ContextualRecallMetric(BaseMetric):
    def __init__(
        self,
        threshold: float = 0.5,
        model: Optional[Union[str, DeepEvalBaseLLM]] = None,
        include_reason: bool = True,
        async_mode: bool = True,
        strict_mode: bool = False,
        verbose_mode: bool = False,
    ):
        self.threshold = 1 if strict_mode else threshold
        self.model, self.using_native_model = initialize_model(model)
        self.evaluation_model = self.model.get_model_name()
        self.include_reason = include_reason
        self.async_mode = async_mode
        self.strict_mode = strict_mode
        self.verbose_mode = verbose_mode

    def measure(self, test_case: Union[LLMTestCase, ConversationalTestCase]) -> float:
        if isinstance(test_case, ConversationalTestCase):
            test_case = validate_conversational_test_case(test_case, self)
        check_llm_test_case_params(test_case, required_params, self)
        self.evaluation_cost = 0 if self.using_native_model else None

        with metric_progress_indicator(self):
            if self.async_mode:
                loop = get_or_create_event_loop()
                loop.run_until_complete(
                    self.a_measure(test_case, _show_indicator=False)
                )
            else:
                self.verdicts: List[ContextualRecallVerdict] = self._generate_verdicts(
                    test_case.expected_output, test_case.retrieval_context
                )
                self.score = self._calculate_score()
                self.reason = self._generate_reason(test_case.expected_output)
                self.success = self.score >= self.threshold
                if self.verbose_mode:
                    print_intermediate_steps(
                        self.__name__,
                        steps=[
                            f"Verdicts:\n{prettify_list(self.verdicts)}\n",
                            f"Score: {self.score}\nReason: {self.reason}",
                        ],
                    )
                return self.score

    async def a_measure(
        self,
        test_case: Union[LLMTestCase, ConversationalTestCase],
        _show_indicator: bool = True,
    ) -> float:
        if isinstance(test_case, ConversationalTestCase):
            test_case = validate_conversational_test_case(test_case, self)
        check_llm_test_case_params(test_case, required_params, self)

        self.evaluation_cost = 0 if self.using_native_model else None
        with metric_progress_indicator(
            self,
            async_mode=True,
            _show_indicator=_show_indicator,
        ):
            self.verdicts: List[ContextualRecallVerdict] = (
                await self._a_generate_verdicts(
                    test_case.expected_output, test_case.retrieval_context
                )
            )
            self.score = self._calculate_score()
            self.reason = await self._a_generate_reason(test_case.expected_output)
            self.success = self.score >= self.threshold
            if self.verbose_mode:
                print_intermediate_steps(
                    self.__name__,
                    steps=[
                        f"Verdicts:\n{prettify_list(self.verdicts)}\n",
                        f"Score: {self.score}\nReason: {self.reason}",
                    ],
                )
            return self.score

    async def _a_generate_reason(self, expected_output: str):
        if self.include_reason is False:
            return None

        supportive_reasons = []
        unsupportive_reasons = []
        for verdict in self.verdicts:
            if verdict.verdict.lower() == "yes":
                supportive_reasons.append(verdict.reason)
            else:
                unsupportive_reasons.append(verdict.reason)

        prompt = ContextualRecallTemplate.generate_reason(
            expected_output=expected_output,
            supportive_reasons=supportive_reasons,
            unsupportive_reasons=unsupportive_reasons,
            score=format(self.score, ".2f"),
        )

        if self.using_native_model:
            res, cost = self.model.generate(prompt)
            self.evaluation_cost += cost
        else:
            res = self.model.generate(prompt)

        data = trimAndLoadJson(res, self)
        return data["reason"]

    def _generate_reason(self, expected_output: str):
        if self.include_reason is False:
            return None

        supportive_reasons = []
        unsupportive_reasons = []
        for verdict in self.verdicts:
            if verdict.verdict.lower() == "yes":
                supportive_reasons.append(verdict.reason)
            else:
                unsupportive_reasons.append(verdict.reason)

        prompt = ContextualRecallTemplate.generate_reason(
            expected_output=expected_output,
            supportive_reasons=supportive_reasons,
            unsupportive_reasons=unsupportive_reasons,
            score=format(self.score, ".2f"),
        )

        if self.using_native_model:
            res, cost = self.model.generate(prompt)
            self.evaluation_cost += cost
        else:
            res = self.model.generate(prompt)

        data = trimAndLoadJson(res, self)
        return data["reason"]

    def _calculate_score(self):
        number_of_verdicts = len(self.verdicts)
        if number_of_verdicts == 0:
            return 0

        justified_sentences = 0
        for verdict in self.verdicts:
            if verdict.verdict.lower() == "yes":
                justified_sentences += 1

        score = justified_sentences / number_of_verdicts
        return 0 if self.strict_mode and score < self.threshold else score

    async def _a_generate_verdicts(
        self, expected_output: str, retrieval_context: List[str]
    ) -> List[ContextualRecallVerdict]:
        prompt = ContextualRecallTemplate.generate_verdicts(
            expected_output=expected_output, retrieval_context=retrieval_context
        )
        if self.using_native_model:
            res, cost = await self.model.a_generate(prompt)
            self.evaluation_cost += cost
        else:
            res = await self.model.a_generate(prompt)
        data = trimAndLoadJson(res, self)
        verdicts = [ContextualRecallVerdict(**item) for item in data["verdicts"]]
        return verdicts

    def _generate_verdicts(
        self, expected_output: str, retrieval_context: List[str]
    ) -> List[ContextualRecallVerdict]:
        prompt = ContextualRecallTemplate.generate_verdicts(
            expected_output=expected_output, retrieval_context=retrieval_context
        )
        if self.using_native_model:
            res, cost = self.model.generate(prompt)
            self.evaluation_cost += cost
        else:
            res = self.model.generate(prompt)
        data = trimAndLoadJson(res, self)
        verdicts = [ContextualRecallVerdict(**item) for item in data["verdicts"]]
        return verdicts

    def is_successful(self) -> bool:
        if self.error is not None:
            self.success = False
        else:
            try:
                self.success = self.score >= self.threshold
            except:
                self.success = False
        return self.success

    @property
    def __name__(self):
        return "Contextual Recall"
