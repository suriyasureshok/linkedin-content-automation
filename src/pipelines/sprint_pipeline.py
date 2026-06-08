from src.integrations.telegram import TelegramClient
from src.storage.github_issues import GitHubIssueStateManager


class SprintPipeline:

    def __init__(self):

        self.telegram = TelegramClient()

    def run(self):

        GitHubIssueStateManager.create_sprint()

        self.telegram.ask_for_topic()
