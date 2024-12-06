from model_optimization_workflow.workflow.workflow_processor import WorkflowProcessor

if __name__ == "__main__":
    processor = WorkflowProcessor(user_config_path='workflow_config.yaml')
    processor.run_processing()
