from pydantic import BaseModel


class PipelineCreateContext(BaseModel):
    git_branch: str
    git_hash: str
    git_comment: str
    repo_url: str
