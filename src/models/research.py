from pydantic import BaseModel, Field, ConfigDict


class Definition(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    term: str = Field(
        min_length=1,
        max_length=200,
    )

    definition: str = Field(
        min_length=1,
    )


class Concept(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    concept: str = Field(
        min_length=1,
        max_length=300,
    )

    explanation: str = Field(
        min_length=1,
    )


class BestPractice(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    practice: str = Field(
        min_length=1,
        max_length=300,
    )

    details: str = Field(
        min_length=1,
    )


class Mistake(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    mistake: str = Field(
        min_length=1,
        max_length=300,
    )

    consequence: str = Field(
        min_length=1,
    )


class CaseStudy(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    title: str = Field(
        min_length=1,
        max_length=300,
    )

    description: str = Field(
        min_length=1,
    )


class InterviewQuestion(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    question: str = Field(
        min_length=1,
    )

    answer: str = Field(
        min_length=1,
    )


class Trend(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    trend: str = Field(
        min_length=1,
        max_length=300,
    )

    details: str = Field(
        min_length=1,
    )


class Source(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    name: str = Field(
        min_length=1,
        max_length=300,
    )

    url: str = Field(
        min_length=1,
    )


class ResearchResponse(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    summary: str = Field(
        description="High level summary of the topic",
        min_length=50,
    )

    definitions: list[Definition] = Field(
        default_factory=list,
    )

    concepts: list[Concept] = Field(
        default_factory=list,
    )

    best_practices: list[BestPractice] = Field(
        default_factory=list,
    )

    mistakes: list[Mistake] = Field(
        default_factory=list,
    )

    case_studies: list[CaseStudy] = Field(
        default_factory=list,
    )

    interview_questions: list[InterviewQuestion] = Field(
        default_factory=list,
    )

    trends: list[Trend] = Field(
        default_factory=list,
    )

    sources: list[Source] = Field(
        default_factory=list,
    )