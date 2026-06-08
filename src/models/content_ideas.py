from pydantic import BaseModel, Field

from src.models.content_idea import ContentIdea


class ContentIdeasResponse(BaseModel):
    ideas: list[ContentIdea] = Field(min_length=10, max_length=10)
