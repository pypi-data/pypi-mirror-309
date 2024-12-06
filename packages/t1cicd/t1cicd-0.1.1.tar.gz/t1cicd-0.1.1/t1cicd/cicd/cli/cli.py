import click

from t1cicd.cicd.cli.client import CICDClient
from t1cicd.cicd.cli.commands import CicdCommands
from t1cicd.cicd.cli.utils import is_git_repo

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.option("--check", "-c", is_flag=True, help="Check config file.")
@click.option("--dryrun", "-dr", is_flag=True, help="Dry run.")
@click.option(
    "--config-file",
    "-cf",
    default="./.cicd-pipelines/pipeline.yml",
    help="Path to config file.",
)
@click.pass_context
def cicd(ctx, check, dryrun, config_file):
    """Welcome to the CICD CLI.

    This CLI is used to interact with the CICD server.

    This command is the entry point to the CLI.
    It can be used to check the config file,
    perform a dry run, or run a pipeline.

    If no subcommand is specified, it will check the config file.
    """
    ctx.ensure_object(dict)
    ctx.obj["client"] = CICDClient()
    cicd_cmds = CicdCommands(ctx.obj["client"])

    if ctx.invoked_subcommand is None:
        if check and dryrun:
            raise click.UsageError("Cannot specify both --check and --dryrun")
        elif dryrun:
            cicd_cmds.perform_dry_run(config_file)
            print(f"Performing dry run with config file: {config_file}")
        else:
            cicd_cmds.check_config(config_file)
            print(f"Checking config file: {config_file}")
    else:
        pass


@cicd.command()
@click.option("--repo", "-r", required=True, help="Repository path.")
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--run", "-rn", help="Run number.")
@click.option("--stage", "-s", help="Stage name.")
@click.option("--job", "-j", help="Job name.")
@click.pass_context
def report(ctx, repo, local, pipeline, run, stage, job):
    """Show a report of a pipeline.

    --local flag is used to run the command locally.

    Use cases:

    1. no options are specified, show a report of all pipelines.

    2. --pipeline is specified, show a report of all runs for the pipeline.

    3. --pipeline and --run are specified, show a report of the run for the pipeline.

    4. --pipeline and --stage are specified, show a report of all runs in the stage.

    5. --pipeline, --run, and --stage are specified, show a report of the run in the stage.

    6. --pipeline, --stage, and --job are specified, show a report of all runs in the job.

    7. --pipeline, --run, --stage, and --job are specified, show a report of the run in the job.

    8. otherwise, no report is shown.
    """
    if local and not is_git_repo(repo):
        raise click.UsageError("Local flag can only be used in a git repository")

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.show_report(repo, local, pipeline, run, stage, job)


@cicd.command()
@click.option(
    "--repo",
    "-r",
    default="./",
    show_default="current local directory",
    help="Repository path.",
)
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option("--branch", "-b", show_default="main branch", help="Branch name.")
@click.option("--commit", "-c", show_default="the latest commit", help="Commit hash.")
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--file", "-f", help="Path to config file.")
@click.option("--override", "-o", multiple=True, help="Override config file.")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output.")
@click.pass_context
def run(ctx, repo, local, branch, commit, pipeline, file, override, verbose):
    """Run a specific pipeline or override the config file in a repository.

    If --override is specified, override the config file with the new config.

    if either --pipeline or --file is specified, run the specific pipeline.

    Otherwise, run all pipelines in the repository.
    """
    if local and not is_git_repo(repo):
        raise click.UsageError("Local flag can only be used in a git repository")

    if override and (branch or commit):
        raise click.UsageError("Cannot specify both --branch/--commit and --override")

    if pipeline and file:
        raise click.UsageError("Cannot specify both --pipeline and --file")

    if override:
        cicd_cmds = CicdCommands(ctx.obj["client"])
        cicd_cmds.override_config(repo, local, override)
        print(f"Overriding config file with: {override}")
        return

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.run_pipeline(repo, local, branch, commit, pipeline, file, verbose)


@cicd.command()
@click.option(
    "--repo",
    "-r",
    default="./",
    show_default="current local directory",
    help="Repository path.",
)
@click.option("--local", "-l", is_flag=True, help="Run locally.")
@click.option(
    "--branch",
    "-b",
    default="main",
    show_default="main branch",
    help="Branch name.",
)
@click.option(
    "--commit",
    "-c",
    default="HEAD",
    show_default="the latest commit",
    help="Commit hash.",
)
@click.option("--pipeline", "-p", help="Pipeline name.")
@click.option("--file", "-f", help="Path to config file.")
@click.pass_context
def stop(ctx, repo, local, branch, commit, pipeline, file):
    """Stop a specific pipeline in a repository."""
    if local and not is_git_repo(repo):
        raise click.UsageError("Local flag can only be used in a git repository")

    cicd_cmds = CicdCommands(ctx.obj["client"])
    cicd_cmds.stop_pipeline(repo, local, branch, commit, pipeline, file)
    print(f"Stopping pipeline in repo: {repo}")


def main():
    cicd()


if __name__ == "__main__":
    cicd()
