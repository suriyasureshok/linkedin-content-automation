from src.integrations.telegram import TelegramClient

from src.storage.github_issues import GitHubIssueStateManager


state = GitHubIssueStateManager()

telegram = TelegramClient()

state.create_sprint()

telegram.ask_for_topic()
