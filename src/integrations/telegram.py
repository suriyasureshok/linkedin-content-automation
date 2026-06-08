import os
import re
import requests

from dotenv import load_dotenv

from src.storage.github_issues import GitHubIssueStateManager

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


class TelegramClient:

    @staticmethod
    def send_message(message: str) -> None:

        url = f"{BASE_URL}/sendMessage"

        payload = {"chat_id": CHAT_ID, "text": message}

        response = requests.post(url, json=payload, timeout=30)

        response.raise_for_status()

    @staticmethod
    def send_long_message(message: str):

        chunk_size = 3500

        chunks = [
            message[i : i + chunk_size] for i in range(0, len(message), chunk_size)
        ]

        for chunk in chunks:
            TelegramClient.send_message(chunk)

    @staticmethod
    def ask_for_topic() -> None:

        message = """
[STARTED] Content Sprint Started

Reply using:

Category: <category>
Subject: <subject>
Topic: <topic>

Example:

Category: Backend Engineering
Subject: Redis
Topic: Memory Management
"""

        TelegramClient.send_message(message)

    @staticmethod
    def parse_topic_message(text: str):

        category_match = re.search(r"Category:\s*(.+)", text, re.IGNORECASE)

        subject_match = re.search(r"Subject:\s*(.+)", text, re.IGNORECASE)

        topic_match = re.search(r"Topic:\s*(.+)", text, re.IGNORECASE)

        if not (category_match and subject_match and topic_match):
            return None

        return {
            "category": category_match.group(1).strip(),
            "subject": subject_match.group(1).strip(),
            "topic": topic_match.group(1).strip(),
        }

    @staticmethod
    def process_message(text: str):

        state = GitHubIssueStateManager()

        if state.get_status() != "WAITING":

            TelegramClient.send_message("[WARNING] No active sprint waiting for topic.")

            return None

        parsed = TelegramClient.parse_topic_message(text)

        if not parsed:

            TelegramClient.send_message(
                """
[ERROR] Invalid format.

Use:

Category: ...
Subject: ...
Topic: ...
"""
            )

            return None

        state.save_topic(
            category=parsed["category"],
            subject=parsed["subject"],
            topic=parsed["topic"],
        )

        TelegramClient.send_message(
            f"""
[COMPLETED] Topic Received

Category: {parsed['category']}
Subject: {parsed['subject']}
Topic: {parsed['topic']}

Starting content generation...
"""
        )

        return parsed

    @staticmethod
    def parse_message_only(text: str):

        return TelegramClient.parse_topic_message(text)
