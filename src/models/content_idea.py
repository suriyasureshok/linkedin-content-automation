from pydantic import BaseModel, Field, ConfigDict


class ContentIdea(BaseModel):

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
        description="Title of the post",
        min_length=5,
        max_length=200,
    )

    angle: str = Field(
        description="Specific angle to explore",
        min_length=10,
        max_length=500,
    )