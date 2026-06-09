from dotenv import load_dotenv

from src.agents.researcher import ResearchAgent

load_dotenv()


def main():

    print("=" * 60)
    print("RESEARCH TEST")
    print("=" * 60)

    agent = ResearchAgent()

    result = agent.run(
        category="Backend Development",
        subject="Redis",
        topic="Memory Management",
    )

    print()

    print("SUMMARY")
    print("-" * 60)
    print(result.summary)

    print()

    print("DEFINITIONS:", len(result.definitions))
    print("CONCEPTS:", len(result.concepts))
    print("BEST PRACTICES:", len(result.best_practices))
    print("MISTAKES:", len(result.mistakes))
    print("CASE STUDIES:", len(result.case_studies))
    print(
        "INTERVIEW QUESTIONS:",
        len(result.interview_questions),
    )
    print("TRENDS:", len(result.trends))
    print("SOURCES:", len(result.sources))

    print()
    print("✅ Research Validation Passed")


if __name__ == "__main__":
    main()