# A mock configuration based on the system design


# A configuration ParsedPipeline example class
from t1cicd.cicd.parser.job import ParsedJob
from t1cicd.cicd.parser.pipeline import ParsedPipeline
from t1cicd.cicd.parser.stage import ParsedStage


class MockConfiguration:
    example_pipeline: ParsedPipeline

    def __init__(self):
        example_job1 = ParsedJob(
            name="test_job1",
            stage="build",
            image="python:3.8",
            script="python test.py",
        )
        example_job2 = ParsedJob(
            name="test_job2",
            stage="build",
            image="python:3.8",
            script="python test.py",
        )
        example_job3 = ParsedJob(
            name="test_job3",
            stage="test",
            image="python:3.8",
            script="python test.py",
        )
        example_job4 = ParsedJob(
            name="test_job4",
            stage="deploy",
            image="python:3.8",
            script="python test.py",
        )
        example_stages = ParsedStage(
            stages={
                "build": [example_job1, example_job2],
                "test": [example_job3],
                "deploy": [example_job4],
            }
        )

        self.example_pipeline = ParsedPipeline(
            pipeline_name="test_pipeline",
            parsed_stages=example_stages,
            variables={},
        )

    def load_config(self):
        return self.example_pipeline
