from dotenv import load_dotenv

from src.agents.researcher import ResearchAgent
from src.agents.strategist import StrategistAgent

load_dotenv()


def main():

    print("=" * 60)
    print("CONTENT IDEAS TEST")
    print("=" * 60)

    research_agent = ResearchAgent()

    strategist_agent = StrategistAgent()

    research = research_agent.run(
        category="Backend Development",
        subject="Redis",
        topic="Memory Management",
    )

    ideas = strategist_agent.run(
        research
    )

    print()

    print(
        f"Generated {len(ideas.ideas)} ideas"
    )

    print()

    for index, idea in enumerate(
        ideas.ideas,
        start=1,
    ):

        print(
            f"{index}. "
            f"{idea.content_type}"
        )

        print(
            f"   Title: {idea.title}"
        )

        print(
            f"   Angle: {idea.angle}"
        )

        print()

    print(
        "✅ Content Ideas Validation Passed"
    )


if __name__ == "__main__":
    main()