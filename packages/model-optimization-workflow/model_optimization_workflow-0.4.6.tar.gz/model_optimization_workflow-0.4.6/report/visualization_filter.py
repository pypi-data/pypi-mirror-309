from typing import List

from report.report import RunReport, VisualizationBinaryReport, VisualizationBinaryRow


class VisualizationFilter:
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

    def transform(self, report: RunReport) -> VisualizationBinaryReport:
        window_indices = self._get_indices(self.window_indices, len(report.windows_reports))
        validation_results = []

        for window_report in self._select_reports(report.windows_reports, window_indices):
            container_indices = self._get_indices(self.container_indices, len(window_report.containers_reports))

            for container_report in self._select_reports(window_report.containers_reports, container_indices):
                model_indices = self._get_indices(self.model_indices, len(container_report.models_reports))

                for model_report in self._select_reports(container_report.models_reports, model_indices):
                    sorted_rows = sorted(model_report.validation_rows, key=lambda r: r.time)
                    validation_results.extend(self._convert_to_visualization_rows(sorted_rows))

        return VisualizationBinaryReport(
            run_id=report.run_id,
            score=report.score,
            params=report.params,
            validation_results=validation_results
        )

    @staticmethod
    def _convert_to_visualization_rows(validation_rows: List) -> List[VisualizationBinaryRow]:
        return [
            VisualizationBinaryRow(time=row.time,
                                   is_correct=(row.planned['labels']['class_1'] == row.predicted['labels']['class_1']))
            for row in validation_rows
        ]
