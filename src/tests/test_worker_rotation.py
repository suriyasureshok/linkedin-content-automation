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
    print("WORKER ROTATION TEST")
    print("=" * 60)

    for i in range(20):

        worker = (
            client._select_worker()
        )

        print(
            f"{i + 1:02d}",
            worker["name"],
        )

        worker["failures"] += 1


if __name__ == "__main__":
    main()