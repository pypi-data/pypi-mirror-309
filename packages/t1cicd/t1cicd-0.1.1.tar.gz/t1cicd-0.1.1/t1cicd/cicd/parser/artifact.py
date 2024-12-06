from pydantic import BaseModel, Field


class Artifact(BaseModel):
    paths: list[str] = Field(..., description="The paths to the artifacts to upload")
    # expire_id: str | None = Field(None, description="The expire id for the artifacts")
