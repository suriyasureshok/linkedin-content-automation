from pydantic import BaseModel, Field


class LinkedInPost(BaseModel):
    content_type: str = Field(description="Type of content")

    title: str = Field(description="Post title")

    body: str = Field(description="Complete LinkedIn post")
