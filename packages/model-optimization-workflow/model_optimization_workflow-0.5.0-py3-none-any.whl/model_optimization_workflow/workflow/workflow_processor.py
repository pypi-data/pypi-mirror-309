import json
import multiprocessing
import os
from datetime import datetime

from market_data_assembler.common.common import prepare_directory
from market_data_assembler.providers.crypto_series_data_provider import CryptoSeriesDataProvider

from model_optimization_workflow.configs.config_loader import ConfigLoader
from model_optimization_workflow.optimizer.global_hyperparameter_optimizer import GlobalHyperparameterOptimizer
from model_optimization_workflow.report.validations_report_manager import ValidationsReportManager
from model_optimization_workflow.workflow.run_processor import RunProcessor


class WorkflowProcessor:
    def __init__(self, user_config_path=None):
        self.config = ConfigLoader(user_config_path=user_config_path).get_config()
        self.root = self.config['workflow']['root_path']
        self.reports_detailed_directory = f'{self.root}/reports/detailed'
        self.reports_validation_directory = f'{self.root}/reports/validation'
        prepare_directory(self.root)
        prepare_directory(self.reports_detailed_directory)
        prepare_directory(self.reports_validation_directory)
        self.optimizer = GlobalHyperparameterOptimizer(self.config)
        self.optimizer.initialize_study()

    def _load_raw_data(self):
        provider_config = self.config['provider']
        provider = CryptoSeriesDataProvider(instruments=provider_config['instruments'],
                                            day_from=provider_config['day_from'],
                                            day_to=provider_config['day_to'],
                                            ohlc_loader_class=provider_config['ohlc_loader']['class'],
                                            trades_loader_class=provider_config['trades_loader']['class'],
                                            book_depth_loader_class=provider_config['book_depth_loader']['class'],
                                            max_workers=provider_config['max_workers'])
        provider.load_raw_series()

    def _init_score_calculator(self):
        parameters = self.config['hyperparameter_optimizer']['score_calculator']['parameters']
        model_class = parameters['class']
        return model_class(parameters['window_indices'], parameters['container_indices'], parameters['model_indices'])

    def _init_validation_report_filter(self):
        parameters = self.config['report']['validation_filter']['parameters']
        model_class = parameters['class']
        return model_class(parameters['window_indices'], parameters['container_indices'], parameters['model_indices'])

    def _start_processor(self, config):
        optimizer = GlobalHyperparameterOptimizer(config)
        score_calculator = self._init_score_calculator()
        visualization_filter = self._init_validation_report_filter()
        params, trial = optimizer.suggest_parameters()

        if len(params['instruments']) == 0:
            optimizer.passed(trial)
            return

        run_report = RunProcessor(config=config, params=params).run_process()
        score = score_calculator.execute(run_report)
        run_report.score = score
        validation_report = visualization_filter.transform(run_report)
        self._save_run_report(self.reports_detailed_directory, run_report)
        self._save_run_report(self.reports_validation_directory, validation_report)
        optimizer.report_result(trial, score)
        print(f"process-{os.getpid()}, time: {datetime.now()}, run id: {run_report.run_id}, score: {score}")

    @staticmethod
    def _save_run_report(directory, run_report):
        report_file = os.path.join(directory, f'{run_report.run_id}.json')
        with open(report_file, 'w') as file:
            json.dump(run_report.to_dict(), file, indent=1)

    def run_processing(self):
        workflow_config = self.config['workflow']
        multiprocessing_size = workflow_config['multiprocessing_size']
        self._load_raw_data()
        while True:
            if self.optimizer.should_stop():
                break

            processes = []
            for _ in range(multiprocessing_size):
                p = multiprocessing.Process(target=self._start_processor, args=(self.config,))
                processes.append(p)
                p.start()

            for p in processes:
                p.join()

        self.optimizer.print_final_results()
        ValidationsReportManager(self.root).generate_reports()
