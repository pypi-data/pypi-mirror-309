import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from model_optimization_workflow.report.report import RunReport, ValidationRow


class ScoreCalculation(ABC):
    def __init__(self, window_indices: List[int], container_indices: List[int], model_indices: List[int]):
        self.window_indices = window_indices
        self.container_indices = container_indices
        self.model_indices = model_indices

    @staticmethod
    def _get_indices(indices: List[int], max_length: int) -> List[int]:
        return indices if indices else list(range(max_length))

    @staticmethod
    def _select_reports(reports: List, indices: List[int]) -> List:
        return [reports[i] for i in indices]

    def execute(self, report: RunReport) -> float:
        window_indices = self._get_indices(self.window_indices, len(report.windows_reports))
        window_validation_rows = []

        for window_report in self._select_reports(report.windows_reports, window_indices):
            container_indices = self._get_indices(
                self.container_indices, len(window_report.containers_reports)
            )
            containers_validation_rows = []

            for container_report in self._select_reports(
                    window_report.containers_reports, container_indices
            ):
                model_indices = self._get_indices(
                    self.model_indices, len(container_report.models_reports)
                )

                for model_report in self._select_reports(
                        container_report.models_reports, model_indices
                ):
                    if not model_report.validation_rows:
                        raise ValueError(
                            f"process-{os.getpid()}, time: {datetime.now()}, "
                            f"Model must provide reports. Missing report for window {window_report.window_id}, "
                            f"container {container_report.container_id}, model ID {model_report.model_id}."
                        )

                    sorted_rows = sorted(
                        model_report.validation_rows, key=lambda row: row.time
                    )
                    containers_validation_rows.extend(sorted_rows)

            window_validation_rows.append(containers_validation_rows)

        return self.calculate(window_validation_rows)

    @abstractmethod
    def calculate(self, validation_rows: List[List[ValidationRow]]) -> float:
        pass
