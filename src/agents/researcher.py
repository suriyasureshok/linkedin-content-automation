from pathlib import Path

from src.integrations.gemini import GeminiClient
from src.models.research import ResearchResponse


class ResearchAgent:

    def __init__(self):

        self.current_dir = Path(__file__).parent
        self.repo_root = self.current_dir.parent.parent

        self.gemini = GeminiClient()

        prompt_path = self.repo_root / "src" / "prompts" / "researcher.txt"
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

        self.generated_dir = self.repo_root / "generated" / "research"
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def _build_prompt(self, category: str, subject: str, topic: str) -> str:

        return f"""
{self.prompt_template}

CATEGORY:
{category}

SUBJECT:
{subject}

TOPIC:
{topic}
"""

    def run(self, category: str, subject: str, topic: str) -> ResearchResponse:

        prompt = self._build_prompt(category, subject, topic)

        return self.gemini.research(prompt)

    def save(self, sprint_id: str, research: ResearchResponse) -> None:

        output_file = self.generated_dir / f"{sprint_id}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(research.model_dump_json(indent=4))
