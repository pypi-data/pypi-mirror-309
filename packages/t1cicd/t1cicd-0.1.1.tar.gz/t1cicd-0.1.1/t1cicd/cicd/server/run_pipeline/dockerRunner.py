import os

import docker
from docker.errors import DockerException, ImageNotFound


class DockerJobRunner:
    def __init__(self, pipeline_name=None, absolute_path=None):
        self.client = docker.from_env()
        base_directory = os.path.abspath(os.path.join(os.getcwd(), ".."))
        self.doc_path = f"{base_directory}/logs/{pipeline_name}"
        volumes = {
            absolute_path: {
                "bind": "/app",
                "mode": "rw",
            },
            self.doc_path: {
                "bind": "/app/docs",
                "mode": "rw",
            },
            # Map host directory to /app inside container
        }
        self.volumes = volumes
        self.work_dir = "/app"
        self.pipeline_name = pipeline_name

    def get_doc_path(self):
        return self.doc_path

    def execute_job(self, job, environment=None, auto_clean=False):
        """
        Check and pull the Docker image if not present, create and start the container, execute commands, and fetch logs.

        :param job: A parsed job from parser, including image name, script commands, etc.
        :param environment: Environment variables for the container
        :param auto_clean: If True, clean the container immediately after job completion.
        """

        # 1,Check if the image is already present, if not pull it
        image_name = job.image
        try:
            # Check if the image is already available locally
            self.client.images.get(image_name)
        except ImageNotFound:
            # Pull the image if it doesn't exist locally
            try:
                self.client.images.pull(image_name)
            except DockerException as e:
                error_message = f"Docker error during image pull: {e}"
                raise RuntimeError(error_message)

        # 2,run the container
        try:
            # print( f"Running container for job '{job.name}' with working directory '{self.work_dir}'")
            container = self.client.containers.run(
                image=image_name,
                command=f"/bin/sh -c '{' && '.join(job.script)}'",  # run the script one by one
                tty=True,  # Keep the terminal open
                working_dir=self.work_dir,
                volumes=self.volumes,
                environment=environment,
                name=f"{job.name}_container",
                detach=True,
            )
        except DockerException as e:
            error_message = f"Docker error during container run: {e}"
            raise RuntimeError(error_message)

        # 3,Wait for container to finish
        try:
            # print(f"Waiting for container {container.name} to finish...")
            container.wait()
        except DockerException as e:
            error_message = f"Error waiting for container: {e}"
            raise RuntimeError(error_message)

        # 4,write container logs to file
        try:
            self.write_container_logs_to_file(container)
        except RuntimeError as e:
            error_message = f"error detected in logs: {e}"
            raise RuntimeError(error_message)
        except Exception as e:
            error_message = f"Error writing container logs to file: {e}"
            raise RuntimeError(error_message)

        # 5,Clean up the container
        finally:
            if auto_clean:
                try:
                    container.stop()
                    container.remove()
                    # print("Container stopped and removed.")
                except DockerException as e:
                    error_message = f"Failed to clean up container: {e}"
                    raise RuntimeError(error_message)

    def write_container_logs_to_file(self, container):
        try:
            # Add timestamps=True to get logs containing timestamps
            logs = container.logs(stdout=True, stderr=True, timestamps=True)

            # Move up one level from the current working directory
            base_directory = os.path.abspath(os.path.join(os.getcwd(), ".."))

            # Build the full log file path, including the container name
            directory_path = os.path.join(
                base_directory, "logs", f"{self.pipeline_name}"
            )

            # Ensure the directory exists
            os.makedirs(directory_path, exist_ok=True)

            container_file_path = os.path.join(
                directory_path, f"{container.name}_output.log"
            )

            # Write logs to file
            with open(container_file_path, "w", encoding="utf-8") as file:
                file.write(logs.decode("utf-8"))
            # print(f"log has been successfully written to { container_file_path}")

            # catch log error
            exit_code = container.wait().get("StatusCode")
            logs_decoded = logs.decode("utf-8")
            if exit_code != 0:
                raise RuntimeError(
                    f"Container exited with error status {exit_code}: {logs_decoded}"
                )

        except Exception as e:
            error_message = f"Error writing container logs to file: {e}"
            raise RuntimeError(error_message)
