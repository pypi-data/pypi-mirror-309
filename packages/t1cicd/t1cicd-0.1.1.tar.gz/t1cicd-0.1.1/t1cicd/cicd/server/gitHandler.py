import os
import subprocess

import git

from t1cicd.cicd.server.custom_logger import CustomLogger

from .utils import is_valid_remote_repo


class HandleGit:
    def __init__(self):
        self.cur_dir = os.getcwd()  # Get the current directory
        self.temp_dir = os.path.join(
            os.path.dirname(self.cur_dir), "temp"
        )  # Set temp in root of cur_dir (server)
        self.commit = None
        print(os.getcwd())

    def clone_and_checkout(self, repo=None, branch="main", commit=None, temp_dir=None):
        # Clone a Git repository and checkout to a specific branch and commit.

        # Set temp_dir to self.temp_dir if not provided
        temp_dir = temp_dir or self.temp_dir

        # TODO: Check if --repo is provided, if not, check if the current directory is a Git repository
        if not repo:
            try:
                # Attempt to open the local repository in the current directory
                local_repo = git.Repo(os.getcwd(), search_parent_directories=False)
                repo = local_repo.working_dir  # Set repo to local path
                print(f"Using local repository at: {repo}")
                CustomLogger.add(f"Using local repository at: {repo}")
            except git.exc.InvalidGitRepositoryError:
                raise ValueError(
                    "No --repo provided and the current directory is not a Git repository"
                )

        # Check if it is a valid repo either from remote or local
        if repo.startswith("http"):
            # Check if the remote repository exists
            if not is_valid_remote_repo(repo):
                raise ValueError(
                    f"Remote repository '{repo}' does not exist or is not accessible."
                )
        elif not os.path.exists(repo) or not os.path.isdir(os.path.join(repo, ".git")):
            raise ValueError(
                f"Local repository '{repo}' does not exist or is not a valid Git repository."
            )

        # Clean up temp_dir if it already exists
        if os.path.exists(temp_dir):
            subprocess.run(["rm", "-rf", temp_dir], check=True)

        try:
            # Clone the repository to temp_dir
            git.Repo.clone_from(repo, temp_dir)
            print(f"Cloned repository from {repo} to {temp_dir}")
            CustomLogger.add(f"Cloned repository from {repo} to {temp_dir}")

            # Change to the cloned repository directory
            os.chdir(temp_dir)
            # Open the cloned repository
            repo_clone = git.Repo(temp_dir)

            # Checkout the specified branch and commit
            repo_clone.git.checkout(branch)
            if commit:
                self.commit = commit
                repo_clone.git.checkout(commit)
            else:
                # Use the latest commit on the specified branch if no specific commit is provided
                latest_commit = repo_clone.head.commit.hexsha
                self.commit = latest_commit
                print(f"No commit specified, using latest commit: {latest_commit}")
                CustomLogger.add(
                    f"No commit specified, using latest commit: {latest_commit}"
                )
                repo_clone.git.checkout(latest_commit)

            return self.commit

        except git.exc.GitCommandError as e:
            print(f"Error: Failed to clone repository '{repo}': {e}")
            raise ValueError(f"Failed to clone repository: {e}")


if __name__ == "__main__":
    git_handler = HandleGit()
    # git_handler.clone_and_checkout(repo="https://github.com/example/repo.git", branch="main")
    # git_handler.clone_and_checkout(repo="~/Desktop/repo_example", branch="main")
    git_handler.clone_and_checkout(repo="~/Desktop/repo_example", branch="main")
