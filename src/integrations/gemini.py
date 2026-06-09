import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

from src.models.research import ResearchResponse
from src.models.content_ideas import ContentIdeasResponse
from src.models.linkedin_posts import LinkedInPostsResponse

load_dotenv()


class GeminiClient:
    def __init__(self, use_multi_ip: bool = None):
        if use_multi_ip is None:
            use_multi_ip = os.getenv("USE_MULTI_IP", "false").lower() == "true"
        
        self.use_multi_ip = use_multi_ip
        
        if use_multi_ip:
            from src.integrations.cloudflare_gemini import CloudflareMultiIPGeminiClient
            self.client = CloudflareMultiIPGeminiClient()
            print("[SUCCESS] Multi-IP mode enabled")
        else:
            # Keep original Google SDK for direct mode
            from google import genai
            from google.genai import types
            self.research_client = genai.Client(api_key=os.getenv("RESEARCH_GEMINI_API_KEY"))
            self.content_ideas_client = genai.Client(api_key=os.getenv("CONTENT_IDEAS_GEMINI_API_KEY"))
            self.writer_client_1 = genai.Client(api_key=os.getenv("WRITER_GEMINI_API_KEY_1"))
            self.writer_client_2 = genai.Client(api_key=os.getenv("WRITER_GEMINI_API_KEY_2"))
            self.types = types
            print("[INFO] Direct mode enabled")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=10, min=10, max=1000),
        retry=retry_if_exception(lambda e: "503" in str(e) or "429" in str(e)),
        reraise=True
    )
    def research(self, prompt: str) -> ResearchResponse:
        if self.use_multi_ip:
            return self.client.research(prompt)
        
        # Direct mode
        response = self.research_client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=self.types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json",
                response_schema=ResearchResponse,
            ),
        )
        return response.parsed
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=10, min=10, max=1000),
        retry=retry_if_exception(lambda e: "503" in str(e) or "429" in str(e)),
        reraise=True
    )
    def generate_content_ideas(self, prompt: str) -> ContentIdeasResponse:
        if self.use_multi_ip:
            return self.client.content_ideas(prompt)
        
        response = self.content_ideas_client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=self.types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
                response_schema=ContentIdeasResponse,
            ),
        )
        return response.parsed
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=10, min=10, max=1000),
        retry=retry_if_exception(lambda e: "503" in str(e) or "429" in str(e)),
        reraise=True
    )
    def generate_posts(self, prompt: str, writer_number: int = 1) -> LinkedInPostsResponse:
        if self.use_multi_ip:
            return self.client.linkedin_posts(prompt)
        
        client = self.writer_client_1 if writer_number == 1 else self.writer_client_2
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL"),
            contents=prompt,
            config=self.types.GenerateContentConfig(
                temperature=0.8,
                response_mime_type="application/json",
                response_schema=LinkedInPostsResponse,
            ),
        )
        return response.parsed