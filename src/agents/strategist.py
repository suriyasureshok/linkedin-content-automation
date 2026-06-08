from pathlib import Path
import json

from src.integrations.gemini import GeminiClient
from src.models.content_ideas import ContentIdeasResponse
from src.models.research import ResearchResponse


class StrategistAgent:

    def __init__(self):

        self.current_dir = Path(
            __file__
        ).parent  # linkedin-content-automation/src/agents/
        self.repo_root = self.current_dir.parent.parent

        self.gemini = GeminiClient()

        prompt_path = self.repo_root / "src" / "prompts" / "strategist.txt"
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

        # Set absolute path for generated content (inside repo)
        self.generated_dir = self.repo_root / "generated" / "ideas"
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def _build_prompt(self, research: ResearchResponse) -> str:

        return f"""
{self.prompt_template}

RESEARCH:

{research.model_dump_json(indent=2)}
"""

    def run(self, research: ResearchResponse) -> ContentIdeasResponse:

        prompt = self._build_prompt(research)

        return self.gemini.generate_content_ideas(prompt)

    def save(self, sprint_id: str, ideas: ContentIdeasResponse):

        output_file = self.generated_dir / f"{sprint_id}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(ideas.model_dump_json(indent=4))
