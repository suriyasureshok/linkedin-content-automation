from pydantic import BaseModel, Field, ConfigDict


class LinkedInPost(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    content_type: str = Field(
        description="Type of content",
        min_length=3,
        max_length=50,
    )

    title: str = Field(
        description="Post title",
        min_length=5,
        max_length=200,
    )

    body: str = Field(
        description="Complete LinkedIn post",
        min_length=100,
        max_length=10000,
    )