from pydantic import BaseModel, Field


class ResearchResponse(BaseModel):
    summary: str = Field(description="High level summary of the topic")

    definitions: list[str] = Field(default_factory=list)

    concepts: list[str] = Field(default_factory=list)

    best_practices: list[str] = Field(default_factory=list)

    mistakes: list[str] = Field(default_factory=list)

    case_studies: list[str] = Field(default_factory=list)

    interview_questions: list[str] = Field(default_factory=list)

    trends: list[str] = Field(default_factory=list)

    sources: list[str] = Field(default_factory=list)
