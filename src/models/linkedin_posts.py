from pydantic import BaseModel, Field, ConfigDict

from src.models.linkedin_post import LinkedInPost


class LinkedInPostsResponse(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    posts: list[LinkedInPost] = Field(
        min_length=10,
        max_length=10,
    )