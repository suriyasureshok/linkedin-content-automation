from src.integrations.cloudflare_gemini import (
    CloudflareMultiIPGeminiClient,
)

from dotenv import load_dotenv

load_dotenv()

def main():

    client = (
        CloudflareMultiIPGeminiClient()
    )

    print("=" * 60)
    print("REAL FAILOVER TEST")
    print("=" * 60)

    prompt = """
    IMPORTANT

Return ONLY valid JSON.

Use EXACTLY the following schema.

{
  "summary": "string",

  "definitions": [
    {
      "term": "string",
      "definition": "string"
    }
  ],

  "concepts": [
    {
      "concept": "string",
      "explanation": "string"
    }
  ],

  "best_practices": [
    {
      "practice": "string",
      "details": "string"
    }
  ],

  "mistakes": [
    {
      "mistake": "string",
      "consequence": "string"
    }
  ],

  "case_studies": [
    {
      "title": "string",
      "description": "string"
    }
  ],

  "interview_questions": [
    {
      "question": "string",
      "answer": "string"
    }
  ],

  "trends": [
    {
      "trend": "string",
      "details": "string"
    }
  ],

  "sources": [
    {
      "name": "string",
      "url": "string"
    }
  ]
}

    Category:
    Backend Development

    Subject:
    Redis

    Topic:
    memory Management
    """

    result = client.research(prompt)

    print()

    print(result.summary)


if __name__ == "__main__":
    main()