import json
from pathlib import Path

from src.integrations.gemini import GeminiClient
from src.models.research import ResearchResponse
from src.models.content_idea import ContentIdea
from src.models.linkedin_posts import LinkedInPostsResponse


class WriterAgent:

    def __init__(self):
        self.current_dir = Path(__file__).parent
        self.repo_root = self.current_dir.parent.parent

        self.gemini = GeminiClient()

        prompt_path = self.repo_root / "src" / "prompts" / "writer.txt"
        self.prompt_template = prompt_path.read_text(encoding="utf-8")

        self.generated_dir = self.repo_root / "generated" / "posts"
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    def _build_prompt(
        self, research: ResearchResponse, ideas: list[ContentIdea]
    ) -> str:

        ideas_json = [idea.model_dump() for idea in ideas]

        return f"""
    {self.prompt_template}

    RESEARCH:

    {research.model_dump_json(indent=2)}

    CONTENT IDEAS:

    {json.dumps(ideas_json, indent=2)}
    """

    def run(
        self, research: ResearchResponse, ideas: ContentIdeasResponse
    ) -> LinkedInPostsResponse:

        first_batch = ideas.ideas[:5]
        second_batch = ideas.ideas[5:]

        prompt_for_first_5 = self._build_prompt(research, first_batch)

        prompt_for_last_5 = self._build_prompt(research, second_batch)

        posts_batch_1 = self.gemini.generate_posts(prompt_for_first_5, writer_number=1)

        posts_batch_2 = self.gemini.generate_posts(prompt_for_last_5, writer_number=2)

        return self.merge_post_responses(posts_batch_1, posts_batch_2)

    def merge_post_responses(
        self, first: LinkedInPostsResponse, second: LinkedInPostsResponse
    ) -> LinkedInPostsResponse:

        return LinkedInPostsResponse(posts=[*first.posts, *second.posts])

    def save(self, sprint_id: str, posts: LinkedInPostsResponse):

        output_file = self.generated_dir / f"{sprint_id}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(posts.model_dump_json(indent=4))
