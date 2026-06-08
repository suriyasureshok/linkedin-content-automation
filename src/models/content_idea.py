from pydantic import BaseModel, Field


class ContentIdea(BaseModel):
    content_type: str = Field(description="Type of content")

    title: str = Field(description="Title of the post")

    angle: str = Field(description="Specific angle to explore")
