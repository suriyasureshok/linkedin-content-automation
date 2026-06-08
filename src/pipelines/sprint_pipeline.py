from integrations.telegram import TelegramClient
from state.manager import SprintStateManager


class SprintPipeline:

    def __init__(self):

        self.telegram = TelegramClient()

    def run(self):

        SprintStateManager.create_sprint()

        self.telegram.ask_for_topic()
        