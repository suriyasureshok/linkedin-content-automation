import os
import requests

from dotenv import load_dotenv

load_dotenv()

WORKERS = [
    (
        "US",
        os.getenv(
            "CLOUDFLARE_WORKER_US_URL"
        ),
    ),
    (
        "EU",
        os.getenv(
            "CLOUDFLARE_WORKER_EU_URL"
        ),
    ),
    (
        "ASIA",
        os.getenv(
            "CLOUDFLARE_WORKER_ASIA_URL"
        ),
    ),
    (
        "AU",
        os.getenv(
            "CLOUDFLARE_WORKER_AU_URL"
        ),
    ),
]


def main():

    print("=" * 60)
    print("WORKER HEALTH TEST")
    print("=" * 60)

    for name, url in WORKERS:

        if not url:
            continue

        print()
        print(f"Testing {name}")

        response = requests.get(
            f"{url}/health",
        )

        print(
            "Status:",
            response.status_code,
        )

        print(
            response.json()
        )


if __name__ == "__main__":
    main()