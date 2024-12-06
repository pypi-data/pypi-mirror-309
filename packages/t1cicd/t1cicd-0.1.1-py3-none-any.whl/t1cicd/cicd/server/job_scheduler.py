import asyncio
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from t1cicd.cicd.db.db import DB
from t1cicd.cicd.db.model.job import Job, JobStatus
from t1cicd.cicd.db.repository.job import JobRepository
from t1cicd.cicd.server.custom_logger import CustomLogger


class ScheduledJob:
    def __init__(
        self,
        name: str,
        needs: list,
        image: str,
        script: list | None,
        artifacts,
        allow_failure=False,
    ):
        self.name = name
        self.needs = needs
        self.in_degree = len(needs)
        self.image = image
        self.script = script
        self.artifacts = artifacts
        self.allow_failure = allow_failure
        self.future = None


class JobScheduler:  # for one stage
    def __init__(self, job_dict: dict[str, Job], max_jobs=10, docker_runner=None):
        self.job_dict = job_dict
        self.jobs = {}  # {job_name: ParsedJob}
        self.dependency_graph = defaultdict(list)  # {job_name: [dependent_job_name]}
        self.lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=max_jobs)
        self.docker_runner = docker_runner
        self.total_jobs = 0
        self.completed_jobs = 0
        self.condition = threading.Condition()
        self.job_failed = (
            False  # Flag to indicate if a non-allow-failure job has failed
        )

    def add_job(self, job):
        self.jobs[job.name] = ScheduledJob(
            job.name, job.needs, job.image, job.script, job.artifacts, job.allow_failure
        )
        self.total_jobs += 1
        for dep_job in job.needs:
            self.dependency_graph[dep_job].append(job.name)

    def run_jobs(self):
        ready_jobs = [
            job_name for job_name, job in self.jobs.items() if job.in_degree == 0
        ]
        with self.lock:
            for job_name in ready_jobs:
                self._start_job(job_name)

        # Wait for all jobs to complete
        with self.condition:
            while self.completed_jobs < self.total_jobs:
                self.condition.wait()

        self.executor.shutdown(wait=True)

    def _start_job(self, job_name):
        job = self.jobs[job_name]
        with self.lock:
            should_cancel = self.job_failed
            db_job = self.job_dict[job_name]
            needs_update = False
            if should_cancel:
                # Do not start new jobs; mark them as CANCELLED
                if db_job.status not in [
                    JobStatus.CANCELLED,
                    JobStatus.FAILED,
                    JobStatus.SUCCESS,
                ]:
                    db_job.status = JobStatus.CANCELLED
                    self.completed_jobs += 1
                    needs_update = True
                with self.condition:
                    self.condition.notify_all()

        if should_cancel:
            # update database outside of lock
            if needs_update:
                asyncio.run(DB.get_repository(JobRepository).update(db_job))
            return

        print(f"Starting job {job_name}")
        CustomLogger.add(f"Starting job {job_name}")
        future = self.executor.submit(self._run_job, job)
        job.future = future

    def _run_job(self, job):
        # add start_time, status to job
        db_job = self.job_dict[job.name]
        db_job.start_time = datetime.now()
        db_job.status = JobStatus.RUNNING
        # update
        asyncio.run(DB.get_repository(JobRepository).update(db_job))
        try:
            print(f"Running job {job.name}")
            CustomLogger.add(f"Running job {job.name}")
            self.docker_runner.execute_job(job, auto_clean=True)
            print(f"Job {job.name} completed")
            CustomLogger.add(f"Job {job.name} completed")

            db_job.status = JobStatus.SUCCESS
            db_job.end_time = datetime.now()
            asyncio.run(DB.get_repository(JobRepository).update(db_job))
        except Exception as e:
            print(f"Job {job.name} failed with error: {e}")
            CustomLogger.add(f"Job {job.name} failed with error: {e}")
            db_job.status = JobStatus.FAILED
            db_job.end_time = datetime.now()
            asyncio.run(DB.get_repository(JobRepository).update(db_job))

            if not job.allow_failure:
                with self.lock:
                    self.job_failed = True
        finally:
            with self.lock:
                self.completed_jobs += 1
                with self.condition:
                    self.condition.notify_all()  # Notify that a job is completed

                dep_jobs_to_start = []
                for dep_job_name in self.dependency_graph.get(job.name, []):
                    dep_job = self.jobs[dep_job_name]
                    dep_job.in_degree -= 1
                    if dep_job.in_degree == 0:
                        dep_jobs_to_start.append(dep_job_name)

            # Start dependent jobs outside of lock
            for dep_job_name in dep_jobs_to_start:
                self._start_job(dep_job_name)
