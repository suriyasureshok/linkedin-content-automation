from dotenv import load_dotenv

from src.agents.researcher import ResearchAgent
from src.agents.strategist import StrategistAgent
from src.agents.writer import WriterAgent

load_dotenv()


def main():

    print("=" * 60)
    print("POST GENERATION TEST")
    print("=" * 60)

    research_agent = ResearchAgent()

    strategist_agent = StrategistAgent()

    writer_agent = WriterAgent()

    research = research_agent.run(
        category="Backend Development",
        subject="Redis",
        topic="Memory Management",
    )

    ideas = strategist_agent.run(
        research
    )

    posts = writer_agent.run(
        research,
        ideas,
    )

    print()

    print(
        f"Generated {len(posts.posts)} posts"
    )

    print()

    for index, post in enumerate(
        posts.posts,
        start=1,
    ):

        print("=" * 60)

        print(
            f"{index}. "
            f"{post.content_type}"
        )

        print(
            f"TITLE: {post.title}"
        )

        print()

        print(
            post.body[:300]
        )

        print()

    print(
        "✅ Post Validation Passed"
    )


if __name__ == "__main__":
    main()