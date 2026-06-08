import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models.research import ResearchResponse
from models.content_ideas import ContentIdeasResponse
from models.linkedin_posts import LinkedInPostsResponse

load_dotenv()


class GeminiClient:

    def __init__(self):
        self.research_client = genai.Client(
            api_key=os.getenv("RESEARCH_GEMINI_API_KEY")
        )
        self.content_ideas_client = genai.Client(
            api_key=os.getenv("CONTENT_IDEAS_GEMINI_API_KEY")
        )
        self.writer_client_1 = genai.Client(
            api_key=os.getenv("WRITER_GEMINI_API_KEY_1")
        )
        self.writer_client_2 = genai.Client(
            api_key=os.getenv("WRITER_GEMINI_API_KEY_2")
        )

    def research(self, prompt: str) -> ResearchResponse:

        response = self.research_client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
                response_schema=ResearchResponse,
            ),
        )

        return response.parsed

    def generate_content_ideas(self, prompt: str) -> ContentIdeasResponse:

        response = self.content_ideas_client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
                response_schema=ContentIdeasResponse,
            ),
        )

        return response.parsed

    def generate_posts(
        self, prompt: str, writer_number: int = 1
    ) -> LinkedInPostsResponse:

        client = self.writer_client_1 if writer_number == 1 else self.writer_client_2

        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
                response_schema=LinkedInPostsResponse,
            ),
        )

        return response.parsed
