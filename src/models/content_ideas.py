from pydantic import BaseModel, Field, ConfigDict

from src.models.content_idea import ContentIdea


class ContentIdeasResponse(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    ideas: list[ContentIdea] = Field(
        min_length=10,
        max_length=10,
    )