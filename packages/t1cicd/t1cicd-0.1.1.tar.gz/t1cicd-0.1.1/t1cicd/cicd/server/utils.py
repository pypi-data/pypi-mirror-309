import os

import git
import requests


def find_yaml_config():
    """Search for a YAML configuration file in the given directory."""
    current_dir = os.getcwd()  # Get the current working directory
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(".yml") or file.endswith(".yaml"):
                return os.path.join(
                    root, file
                )  # Return the full path to the first found .yml file
    return None


def is_valid_remote_repo(repo_url):
    """
    Check if a remote Git repository is valid by attempting to list references.
    For HTTP(S) URLs, an additional request check is done.
    """
    try:
        # Check if it's an HTTP(S) repository
        if repo_url.startswith("http"):
            # Make a simple request to check if the URL exists
            response = requests.get(repo_url)
            return response.status_code == 200
    except git.exc.GitCommandError:
        return False
    except requests.exceptions.RequestException:
        return False
