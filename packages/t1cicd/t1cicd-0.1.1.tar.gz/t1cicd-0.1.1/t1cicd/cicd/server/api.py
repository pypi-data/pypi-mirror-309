import asyncio
import os
import traceback

import yaml
from flask import jsonify, request

from t1cicd.cicd.parser.parser import YAMLParser
from t1cicd.cicd.parser.utils import apply_override, get_dry_run_order, is_valid_override
from t1cicd.cicd.server.custom_logger import CustomLogger
from t1cicd.cicd.server.gitHandler import HandleGit
from t1cicd.cicd.server.mock import MockConfiguration
from t1cicd.cicd.server.run_pipeline.dockerRunner import DockerJobRunner
from t1cicd.cicd.server.run_pipeline.pipelineScheduler import PipelineScheduler

# from uuid import UUID


mock = MockConfiguration()
config = mock.load_config()

# Define the API root dir
API_ROOT_DIR = os.getcwd()
TEMP_DIR = os.path.abspath("./tmp")
PIPELINES_DIR = os.path.abspath(".cicd-pipelines")


def register_routes(app, summary_service=None):
    @app.route("/")
    def welcome_page():
        """Welcome Page
        ---
        responses:
          200:
            description: Welcome message
        """
        return "REST API for CICD System!"

    @app.route("/api/check-config", methods=["POST"])
    def check_config():
        """Check YAML Configuration
        ---
        parameters:
          - name: yaml_path
            in: body
            type: string
            required: true
            description: Path to the YAML configuration file
        responses:
          200:
            description: Valid YAML configuration
          404:
            description: YAML file not found
          400:
            description: Invalid YAML or other error
        """
        data = request.json

        # Get the path to the YAML config file
        yaml_path = data.get("yaml_path")

        # Try parsing the YAML configuration
        try:
            parser = YAMLParser(yaml_path)
            parser.parse()
        except FileNotFoundError:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "YAML file not found at the specified path",
                    }
                ),
                404,
            )
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        except yaml.YAMLError as exc:
            return (
                jsonify({"status": "error", "message": f"Invalid YAML: {str(exc)}"}),
                400,
            )

        return (
            jsonify({"status": "success", "message": "YAML configuration is valid"}),
            200,
        )

    @app.route("/api/dry-run", methods=["POST"])
    def dry_run():
        """Dry Run Pipeline
        ---
        parameters:
          - name: yaml_path
            in: body
            required: true
            schema:
              type: object
              properties:
                yaml_path:
                  type: string
                  description: Path to the YAML configuration file
        responses:
          200:
            description: Successful dry run execution
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                message:
                  type: string
                  example: "Dry run executed successfully. Pipeline: TestPipeline, Job order: Stage: Stage1, Job: Job1"
          404:
            description: YAML file not found
          400:
            description: Invalid YAML or other error
        """
        data = request.json
        # Get the path to the YAML config file
        yaml_path = data.get("yaml_path")

        if not yaml_path:
            yaml_path = "../../../.cicd/pipeline.yml"

        # Parse the YAML configuration using YAMLParser
        try:
            parser = YAMLParser(yaml_path)
            parsed_pipeline = parser.parse()
        except FileNotFoundError:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "YAML file not found at the specified path",
                    }
                ),
                404,
            )
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        except yaml.YAMLError as exc:
            return (
                jsonify({"status": "error", "message": f"Invalid YAML: {str(exc)}"}),
                400,
            )

        # job order
        job_order = get_dry_run_order(parsed_pipeline.parsed_stages.stages)

        print(job_order)
        # For each stage, add all jobs in topo order in job_order
        # for stage_name, jobs in parsed_pipeline.get_all_stages():
        #     # Create a new dictionary for each stage
        #     stage = {"stage_name": stage_name}
        #
        #     # Perform topological sorting for the jobs in the current stage
        #     jobs_in_stage = get_dry_run_order(jobs)
        #
        #     # Add the sorted jobs to the stage dictionary
        #     stage["jobs"] = jobs_in_stage
        #
        #     # Append the stage to the job order
        #     job_order.append(stage)

        # Including the job order in the message
        message = (
            f"Dry run executed successfully. \n"
            f"Pipeline: {parsed_pipeline.pipeline_name}, \n"
            f"Job order: {job_order}"
        )

        return jsonify({"status": "success", "message": message}), 200

    @app.route("/api/run-pipeline", methods=["POST"])
    def run_pipeline():
        """Run Pipelines
        ---
        parameters:
          - in: body
            name: pipeline_data
            required: false
            schema:
              type: object
              properties:
                repo:
                  type: string
                  description: URL of the repository
                  example: "https://github.com/example/repo.git"
                commit:
                  type: string
                  description: Commit hash to use for the pipeline run
                  example: "abc123"
                branch_name:
                  type: string
                  description: Name of the branch to run pipelines on (default is 'main')
                  example: "main"
                pipeline:
                  type: string
                  description: Name of the pipeline to execute (mutually exclusive with 'file')
                  example: "pipeline_hello_world"
                file:
                  type: string
                  description: Path to the specific pipeline config file (mutually exclusive with 'pipeline')
                  example: "../.cicd-pipelines/pipeline_hello_world.yml"
        responses:
          200:
            description: Successful pipeline run
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                message:
                  type: string
                  example: "Pipelines successfully triggered for branch 'main', commit 'abc123' on repository 'https://github.com/example/repo.git'"
          400:
            description: Bad request due to mutual exclusivity error or invalid input
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "error"
                message:
                  type: string
                  example: "Only one of --pipeline or --file can be provided."
          404:
            description: Config file or resource not found
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "error"
                message:
                  type: string
                  example: "Config file or resource not found. Ensure the file path is correct and the file exists."
          500:
            description: Server error due to runtime issues or unexpected failures
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "error"
                message:
                  type: string
                  example: "A runtime error occurred during pipeline execution: Git cloning errors, Docker issues, or pipeline configuration issues."
        """
        # Get the parameters from the request
        data = request.json
        pipeline_name = data.get("pipeline")
        config_file = data.get("file")
        repo = data.get("repo")
        commit = data.get("commit")
        branch = data.get("branch_name") or "main"
        # Mutual exclusivity check
        if pipeline_name and config_file:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Only one of --pipeline or --file can be provided.",
                    }
                ),
                400,
            )

        try:
            # Change to API ROOT DIR before every request
            os.chdir(API_ROOT_DIR)

            # Initialize and run the PipelineScheduler
            pipeline_scheduler = PipelineScheduler(
                repo=repo,
                branch=branch,
                commit=commit,
                config_file=config_file,
                pipeline_name=pipeline_name,
                temp_dir=TEMP_DIR,  # Make sure this points to your temporary directory
                pipelines_dir=PIPELINES_DIR,  # Your folder containing pipelines
                git_handler=HandleGit(),  # Custom or default git handler
                docker_runner=DockerJobRunner(),  # Custom or default Docker runner
            )

            # Run the pipeline
            pipeline_result = pipeline_scheduler.run()

            # Change to API ROOT DIR from TEMP DIR
            os.chdir(API_ROOT_DIR)

        except FileNotFoundError as e:
            tb = traceback.format_exc()
            error_msg = (
                f"Config file or resource not found: {str(e)}."
                f"Ensure the file path is correct and the file exists."
                f"Attempted to find the file: {config_file or 'No config file provided'}"
            )
            return (
                jsonify({"status": "error", "message": error_msg, "verbose_data": tb}),
                404,
            )

        except ValueError as e:
            tb = traceback.format_exc()
            error_msg = (
                f"Invalid input detected: {str(e)}."
                f"Check the repository URL, branch name, commit hash, or pipeline name."
                f"Provided repo: {repo}, branch: {branch}, commit: {commit}, pipeline: {pipeline_name}."
            )
            return (
                jsonify({"status": "error", "message": error_msg, "verbose_data": tb}),
                400,
            )

        except RuntimeError as e:
            tb = traceback.format_exc()
            error_msg = (
                f"A runtime error occurred during pipeline execution: {str(e)}."
                f"Possible issues include Git cloning errors, Docker execution problems, "
                f"or pipeline configuration issues."
                f"Attempted repository: {repo}, branch: {branch}, commit: {commit}, config: {config_file}."
            )
            return (
                jsonify({"status": "error", "message": error_msg, "verbose_data": tb}),
                500,
            )

        except Exception as e:
            tb = traceback.format_exc()
            error_msg = (
                f"An unexpected error occurred: {str(e)}. "
                f"Please check the provided repository URL, branch, commit hash, and config file. "
                f"Provided data: repo: {repo}, branch: {branch}, commit: {commit}, config file: {config_file}, pipeline: {pipeline_name}."
            )
            return (
                jsonify({"status": "error", "message": error_msg, "verbose_data": tb}),
                500,
            )

        vd = CustomLogger.get()
        CustomLogger.reset()
        return (
            jsonify(
                {"status": "success", "message": pipeline_result, "verbose_data": vd}
            ),
            200,
        )

    @app.route("/api/stop-pipeline", methods=["POST"])
    def stop_pipeline():
        """Stop Pipelines
        ---
        parameters:
          - name: repo
            in: body
            required: true
            schema:
              type: object
              properties:
                repo:
                  type: string
                  description: URL of the repository
                commit:
                  type: string
                  description: Commit hash to use
                branch_name:
                  type: string
                  description: Name of the branch to stop pipelines on
        responses:
          200:
            description: Successful pipeline stop
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                message:
                  type: string
                  example: "Pipelines successfully stopped for branch 'main', commit 'abc123' on repository 'https://github.com/example/repo.git'"
          500:
            description: Failed to stop pipeline
        """
        data = request.json

        # Get the repository URL and branch name from the request
        repo = data.get("repo")
        commit = data.get("commit")
        branch = data.get("branch_name")

        # Dummy logic for stop the pipeline
        try:
            # In a real use case, you would clone the repository and check out the branch here
            # This could be done with git commands or a similar mechanism
            pipeline_result = f"Pipelines successfully stopped for branch '{branch}', commit '{commit}' on repository '{repo}'"

            # For example, you might run some pipeline logic here and todo

        except Exception as e:
            # Return an error if something went wrong
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Failed to stopped pipeline: {str(e)}",
                    }
                ),
                500,
            )

        # Return success with the pipeline result
        return jsonify({"status": "success", "message": pipeline_result}), 200

    @app.route("/api/override-config", methods=["POST"])
    def override_config():
        """Override Configuration
        ---
        parameters:
          - name: repo
            in: body
            required: true
            schema:
              type: object
              properties:
                repo:
                  type: string
                  description: URL of the repository
                override:
                  type: string
                  description: New configuration to override the existing configuration
        responses:
          200:
            description: Successful configuration override
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
                message:
                  type: string
                  example: "Configuration successfully overridden for repository "
          500:
            description: Failed to override configuration
          400:
            description: Invalid override configuration
        """
        data = request.json

        # Get the repository URL and override configuration from the request
        repo = data.get("repo")
        override = data.get("override")
        print(override)
        try:
            if not is_valid_override(override):
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": "Invalid override configuration",
                        }
                    ),
                    400,
                )
            print(config)
            apply_override(config, override)
            print(config)
            override_result = (
                f"Configuration successfully overridden for repository {repo}"
            )

        except Exception as e:
            # Return an error if something went wrong
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Failed to override configuration: {str(e)}",
                    }
                ),
                500,
            )

        # Return success with the override result
        return jsonify({"status": "success", "message": override_result}), 200

    @app.route("/api/report", methods=["GET"])
    def get_all_pipelines_summary():
        """Get all pipeline summaries
        ---
        responses:
          200:
            description: Successful retrieval of pipeline summaries
        """
        data = request.json
        repo = data.get("repo")
        if not repo:
            return (
                jsonify({"status": "error", "message": "Repository URL is required"}),
                400,
            )
        repo_summary = asyncio.run(summary_service.get_pipeline_summary_by_repo(repo))
        # print(repo_summary)
        return jsonify({"status": "success", "message": repo_summary}), 200

    @app.route("/api/report/pipeline/<pipeline_name>", methods=["GET"])
    def get_pipeline_summaries(pipeline_name):
        """Get pipeline summaries for all runs of a pipeline
        ---
        parameters:
          - name: pipeline_name
            in: path
            type: string
            required: true
            description: Name of the pipeline
        responses:
          200:
            description: Successful retrieval of pipeline summaries
        """
        try:
            pipeline_name_ids = asyncio.run(summary_service.get_pipeline_name_ids())
            pipeline_ids = pipeline_name_ids.get(pipeline_name)
            if not pipeline_ids:
                return (
                    jsonify({"status": "error", "message": "Pipeline not found"}),
                    404,
                )
            # Get pipeline summaries
            summaries = []
            for pipeline_id in pipeline_ids:
                pipeline_summary = asyncio.run(
                    summary_service.get_pipeline_summary(pipeline_id)
                )
                summaries.append(pipeline_summary)
            # print("summaries", summaries)
            return jsonify({"status": "success", "message": summaries}), 200
        except Exception as e:
            return (
                jsonify({"status": "error", "message": str(e)}),
                500,
            )

    @app.route("/api/report/pipeline/<pipeline_name>/<run>", methods=["GET"])
    def get_pipeline_run(pipeline_name, run):
        """Get specific pipeline run summary
        ---
        parameters:
          - name: pipeline_name
            in: path
            type: string
            required: true
            description: Name of the pipeline
          - name: run
            in: path
            type: string
            required: true
            description: Run identifier (can be UUID)
        responses:
          200:
            description: Successful retrieval of pipeline run summary
        """
        try:
            # Check if run is a valid UUID
            # pipeline_id = UUID(run)
            pipeline_id = int(run)
            pipeline_summary = asyncio.run(
                summary_service.get_pipeline_summary(pipeline_id)
            )
            if not pipeline_summary:
                return (
                    jsonify({"status": "error", "message": "Pipeline run not found"}),
                    404,
                )
            # Check if pipeline name matches
            if pipeline_summary.get("pipeline_name") != pipeline_name:
                return (
                    jsonify(
                        {"status": "error", "message": "Pipeline name does not match"}
                    ),
                    400,
                )
            return jsonify({"status": "success", "message": pipeline_summary}), 200
        except ValueError:
            # Return error if run is not a valid UUID
            return (
                jsonify({"status": "error", "message": "Invalid run identifier"}),
                400,
            )
        except Exception as e:
            return (
                jsonify({"status": "error", "message": str(e)}),
                500,
            )

    @app.route("/api/report/stage/<pipeline_name>/<stage_name>", methods=["GET"])
    def get_stage_summaries(pipeline_name, stage_name):
        """Get stage summaries for all runs of a specific stage in a pipeline
        ---
        parameters:
          - name: pipeline_name
            in: path
            type: string
            required: true
            description: Name of the pipeline
          - name: stage_name
            in: path
            type: string
            required: true
            description: Name of the stage
        responses:
          200:
            description: Successful retrieval of stage summaries
        """
        try:
            pipeline_name_ids = asyncio.run(summary_service.get_pipeline_name_ids())
            pipeline_ids = pipeline_name_ids.get(pipeline_name)
            if not pipeline_ids:
                return (
                    jsonify({"status": "error", "message": "Pipeline not found"}),
                    404,
                )
            # Get stage summaries
            stage_summaries = []
            stage_ids = []
            for pipeline_id in pipeline_ids:
                pipeline_summary = asyncio.run(
                    summary_service.get_pipeline_summary(pipeline_id)
                )
                stages = pipeline_summary.get("stage", [])
                for stage in stages:
                    if stage.get("stage_name") == stage_name:
                        stage_ids.append(stage.get("id"))
            # print(stage_ids)
            for stage_id in stage_ids:
                stage_summary = asyncio.run(summary_service.get_stage_summary(stage_id))
                stage_summaries.append(stage_summary)
            if not stage_summaries:
                return (
                    jsonify(
                        {"status": "error", "message": "Stage not found in any runs"}
                    ),
                    404,
                )
            return jsonify({"status": "success", "message": stage_summaries}), 200
        except Exception as e:
            return (
                jsonify({"status": "error", "message": str(e)}),
                500,
            )

    @app.route("/api/report/stage/<pipeline_name>/<stage_name>/<run>", methods=["GET"])
    def get_stage_run(pipeline_name, stage_name, run):
        """Get specific stage run summary
        ---
        parameters:
          - name: pipeline_name
            in: path
            type: string
            required: true
            description: Name of the pipeline
          - name: stage_name
            in: path
            type: string
            required: true
            description: Name of the stage
          - name: run
            in: path
            type: string
            required: true
            description: Run identifier (can be UUID)
        responses:
          200:
            description: Successful retrieval of stage run summary
        """
        try:
            # pipeline_id = UUID(run)
            pipeline_id = int(run)
            pipeline_summary = asyncio.run(
                summary_service.get_pipeline_summary(pipeline_id)
            )
            if not pipeline_summary:
                return (
                    jsonify({"status": "error", "message": "Pipeline run not found"}),
                    404,
                )
            if pipeline_summary.get("pipeline_name") != pipeline_name:
                return (
                    jsonify(
                        {"status": "error", "message": "Pipeline name does not match"}
                    ),
                    400,
                )
            stage_ids = []
            stages = pipeline_summary.get("stage", [])
            for stage in stages:
                if stage.get("stage_name") == stage_name:
                    stage_ids.append(stage.get("id"))
            for stage_id in stage_ids:
                stage_summary = asyncio.run(summary_service.get_stage_summary(stage_id))
                if stage_summary:
                    return jsonify({"status": "success", "message": stage_summary}), 200
            return (
                jsonify({"status": "error", "message": "Stage not found in this run"}),
                404,
            )
        except ValueError:
            return (
                jsonify({"status": "error", "message": "Invalid run identifier"}),
                400,
            )
        except Exception as e:
            return (
                jsonify({"status": "error", "message": str(e)}),
                500,
            )

    @app.route(
        "/api/report/job/<pipeline_name>/<stage_name>/<job_name>", methods=["GET"]
    )
    def get_job_summaries(pipeline_name, stage_name, job_name):
        """Get job summaries for all runs of a specific job in a pipeline
        ---
        parameters:
          - name: pipeline_name
            in: path
            type: string
            required: true
            description: Name of the pipeline
          - name: stage_name
            in: path
            type: string
            required: true
            description: Name of the stage
        responses:
          200:
            description: Successful retrieval of stage summaries
        """
        try:
            pipeline_name_ids = asyncio.run(summary_service.get_pipeline_name_ids())
            pipeline_ids = pipeline_name_ids.get(pipeline_name)
            if not pipeline_ids:
                return (
                    jsonify({"status": "error", "message": "Pipeline not found"}),
                    404,
                )
            # Get stage summaries
            stage_summaries = []
            stage_ids = []
            for pipeline_id in pipeline_ids:
                pipeline_summary = asyncio.run(
                    summary_service.get_pipeline_summary(pipeline_id)
                )
                stages = pipeline_summary.get("stage", [])
                for stage in stages:
                    if stage.get("stage_name") == stage_name:
                        stage_ids.append(stage.get("id"))
            job_ids = []
            for stage_id in stage_ids:
                stage_summary = asyncio.run(summary_service.get_stage_summary(stage_id))
                jobs = stage_summary.get("job", [])
                for job in jobs:
                    if job.get("job_name") == job_name:
                        job_ids.append(job.get("id"))
            job_summaries = []
            for job_id in job_ids:
                job_summary = asyncio.run(summary_service.get_job_summary(job_id))
                job_summaries.append(job_summary)
            if not stage_summaries:
                return (
                    jsonify(
                        {"status": "error", "message": "Stage not found in any runs"}
                    ),
                    404,
                )
            return jsonify({"status": "success", "message": stage_summaries}), 200
        except Exception as e:
            return (
                jsonify({"status": "error", "message": str(e)}),
                500,
            )

    @app.route(
        "/api/report/job/<pipeline_name>/<stage_name>/<job_name>/<run>",
        methods=["GET"],
    )
    def get_job_run(pipeline_name, stage_name, job_name, run):
        """Get specific stage run summary
        ---
        parameters:
          - name: pipeline_name
            in: path
            type: string
            required: true
            description: Name of the pipeline
          - name: stage_name
            in: path
            type: string
            required: true
            description: Name of the stage
          - name: run
            in: path
            type: string
            required: true
            description: Run identifier (can be UUID)
        responses:
          200:
            description: Successful retrieval of stage run summary
        """
        try:
            # pipeline_id = UUID(run)
            pipeline_id = int(run)
            pipeline_summary = asyncio.run(
                summary_service.get_pipeline_summary(pipeline_id)
            )
            if not pipeline_summary:
                return (
                    jsonify({"status": "error", "message": "Pipeline run not found"}),
                    404,
                )
            if pipeline_summary.get("pipeline_name") != pipeline_name:
                return (
                    jsonify(
                        {"status": "error", "message": "Pipeline name does not match"}
                    ),
                    400,
                )
            stage_ids = []
            stages = pipeline_summary.get("stage", [])
            for stage in stages:
                if stage.get("stage_name") == stage_name:
                    stage_ids.append(stage.get("id"))
            job_ids = []
            for stage_id in stage_ids:
                stage_summary = asyncio.run(summary_service.get_stage_summary(stage_id))
                jobs = stage_summary.get("job", [])
                for job in jobs:
                    if job.get("job_name") == job_name:
                        job_ids.append(job.get("id"))
            for job_id in job_ids:
                job_summary = asyncio.run(summary_service.get_job_summary(job_id))
                if job_summary:
                    return jsonify({"status": "success", "message": job_summary}), 200
            return (
                jsonify({"status": "error", "message": "Stage not found in this run"}),
                404,
            )
        except ValueError:
            return (
                jsonify({"status": "error", "message": "Invalid run identifier"}),
                400,
            )
        except Exception as e:
            return (
                jsonify({"status": "error", "message": str(e)}),
                500,
            )
