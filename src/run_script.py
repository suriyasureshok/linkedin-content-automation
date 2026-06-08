from integrations.telegram import (
    TelegramClient
)

from storage.github_issues import (
    GitHubIssueStateManager
)


state = GitHubIssueStateManager()

telegram = TelegramClient()

state.create_sprint()

telegram.ask_for_topic()
