class CicdCommands:
    def __init__(self, client):
        self.client = client

    def check_config(self, yaml_path):
        payload = {"yaml_path": yaml_path}
        # click.echo(payload)
        endpoint = "/api/check-config"
        response = self.client.request("POST", endpoint, payload, local=True)
        self.client.handle_response(response)

    def perform_dry_run(self, yaml_path):
        payload = {"yaml_path": yaml_path}
        # click.echo(payload)
        endpoint = "/api/dry-run"
        response = self.client.request("POST", endpoint, payload, local=True)
        self.client.handle_response(response)

    def show_report(self, repo, local, pipeline, run, stage, job):
        payload = {"repo": repo}
        local = True  # only for now
        # click.echo(payload)
        if not pipeline and not run and not stage and not job:
            endpoint = "/api/report"
            response = self.client.request("GET", endpoint, payload, local)
        elif pipeline and not run and not stage and not job:
            endpoint = f"/api/report/pipeline/{pipeline}"
            response = self.client.request("GET", endpoint, payload, local)
        elif pipeline and run and not stage and not job:
            endpoint = f"/api/report/pipeline/{pipeline}/{run}"
            response = self.client.request("GET", endpoint, payload, local)
        elif pipeline and not run and stage and not job:
            endpoint = f"/api/report/stage/{pipeline}/{stage}"
            response = self.client.request("GET", endpoint, payload, local)
        elif pipeline and run and stage and not job:
            endpoint = f"/api/report/stage/{pipeline}/{stage}/{run}"
            response = self.client.request("GET", endpoint, payload, local)
        elif pipeline and not run and stage and job:
            endpoint = f"/api/report/job/{pipeline}/{stage}/{job}"
            response = self.client.request("GET", endpoint, payload, local)
        elif pipeline and run and stage and job:
            endpoint = f"/api/report/job/{pipeline}/{stage}/{job}/{run}"
            response = self.client.request("GET", endpoint, payload, local)
        else:
            response = None

        self.client.handle_response(response)

    def override_config(self, repo, local, override):
        payload = {
            "repo": repo,
            "local": local,
            "override": override,
        }
        # click.echo(payload)
        endpoint = "/api/override-config"
        local = True  # only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response)

    # the location of the repo where the code and the pipeline config file is located.
    # xx run --local --repo https: // github.com / company / test --commit 3df7142 --branch main
    # (future not for now:) reading configuration from a different repo by passing the repo’s location (local or remote location)
    def run_pipeline(self, repo, local, branch, commit, pipeline, file, verbose):
        payload = {
            "repo": repo,
            "commit": commit,
            "branch_name": branch,
            "pipeline": pipeline,
            "file": file,
        }
        # click.echo(payload)
        endpoint = "/api/run-pipeline"
        local = True  # only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response, verbose)

    def stop_pipeline(self, repo, local, branch, commit, pipeline, file):
        payload = {
            "repo": repo,
            "commit": commit,
            "branch_name": branch,
            "pipeline": pipeline,
            "file": file,
        }
        # click.echo(payload)
        endpoint = "/api/stop-pipeline"
        local = True  # only for now
        response = self.client.request("POST", endpoint, payload, local)
        self.client.handle_response(response)


# if __name__ == "__main__":
#     # Initialize the CICDClient
#
#     client= CICDClient()
#     cicd_cmds = CicdCommands(client)
#
#     cicd_cmds.run_pipelines(repo="my-repo", commit="abc123", branch="main", local=True)
