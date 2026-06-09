import logging

from src.integrations.telegram import (
    TelegramClient,
)

from src.storage.github_issues import (
    GitHubIssueStateManager,
)

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


def main():

    state = GitHubIssueStateManager()

    telegram = TelegramClient()

    existing_status = (
        state.get_status()
    )

    if existing_status in (
        "WAITING",
        "PROCESSING",
    ):

        logger.warning(
            "Active sprint already exists"
        )

        telegram.send_message(
            """
[WARNING]

A sprint is already active.

Create a new sprint only after
the current sprint is completed.
"""
        )

        return

    sprint_number = (
        state.create_sprint()
    )

    logger.info(
        "Created sprint #%s",
        sprint_number,
    )

    telegram.ask_for_topic()

    logger.info(
        "Topic request sent"
    )


if __name__ == "__main__":

    main()