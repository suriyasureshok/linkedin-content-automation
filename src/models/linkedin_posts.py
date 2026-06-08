from pydantic import BaseModel, Field

from src.models.linkedin_post import LinkedInPost


class LinkedInPostsResponse(BaseModel):
    posts: list[LinkedInPost] = Field(min_length=10, max_length=10)
