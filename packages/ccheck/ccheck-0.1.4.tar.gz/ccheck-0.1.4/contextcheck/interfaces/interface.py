from __future__ import annotations

import copy
from collections import defaultdict
from typing import TYPE_CHECKING, Any

import numpy as np
from loguru import logger
from pydantic import BaseModel

from contextcheck.assertions.settings import AssertionKind

if TYPE_CHECKING:
    from contextcheck.executors.executor import Executor


class InterfaceBase(BaseModel):
    """UI should "know" what to do with a given object."""

    def __call__(self, obj: Any) -> Any:
        logger.info(obj)

    @staticmethod
    def summary(obj: Any, **kwargs: Any) -> Any:
        logger.info(obj)

    def _create_a_summary_report(
        self, executor: Executor
    ) -> dict[str, dict[str, dict[str, float]]]:
        """
        Create a summary of the results obtained from a test scenario

        Warning: The results must be a nested dict of type dict[str, dict[str, dict[str, float]]]
        """

        # This function is taken straight from assertion factory
        def get_assertion_kind(assertion: dict):
            kind = next(
                assert_key
                for assert_key in assertion.keys()
                if assert_key in [ak.value for ak in AssertionKind]
            )
            return kind

        # Summarize binary statistics
        def summarize_binary_statistics(data: list[float]) -> dict[str, float]:
            if not data:
                return {"mean": 0.0, "count": 0}

            count1 = sum(data)
            count = len(data)
            mean = count1 / count

            return {"mean": mean, "count": count}

        # In place aggregation of the assertion results
        def aggregate_data(data: dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    aggregate_data(value)
                else:
                    # NOTE: Currently all statistics are binary, therefore it can be leave as it is
                    # If continous statistics occur then this functionality shall be extended
                    # NOTE: One option that I see is to create (key-type) mapper where each
                    # statistic would be summarized differently depending on its name
                    data[key] = summarize_binary_statistics(data[key])

        assertion_results = defaultdict(lambda: defaultdict(list))
        for step in executor.test_scenario.steps:
            for assertion in step.asserts:
                assertion = assertion.model_dump()
                kind = get_assertion_kind(assertion=assertion)
                assertion_results[kind][
                    assertion[kind] if kind != AssertionKind.EVAL else kind
                ].append(
                    float(assertion["result"]) if assertion["result"] is not None else 0.0
                )  # Dump results to float for easier manipulation

        # Copy is technically not necessary, but it logically separates the results from
        # the aggregation
        assertion_results_aggregated = copy.deepcopy(assertion_results)
        aggregate_data(data=assertion_results_aggregated)
        return assertion_results_aggregated

    def _create_time_statistics(self, executor: "Executor") -> dict[str, float]:
        request_times = []
        for step in executor.test_scenario.steps:
            request_times.append(step.response.stats.conn_duration)

        mean = np.mean(request_times)
        median = np.median(request_times)
        minimum = np.min(request_times)
        maximum = np.max(request_times)
        std = np.std(request_times)

        time_statistics = {
            "mean": mean,
            "median": median,
            "minimum": minimum,
            "maximum": maximum,
            "std": std,
        }
        return time_statistics

    def report_results(self, executor: "Executor", **kwargs) -> None:
        raise NotImplementedError("Functionality is not implemented")

    def report_time(self, executor: "Executor", **kwargs) -> None:
        raise NotImplementedError("Functionality is not implemented")
