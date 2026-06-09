from src.agents.researcher import ResearchAgent
from src.agents.strategist import StrategistAgent
from src.agents.writer import WriterAgent

from src.delivery.delivery_manager import DeliveryManager
from src.integrations.telegram import TelegramClient


class ContentPipeline:

    def __init__(self):

        self.research_agent = ResearchAgent()
        self.strategist_agent = StrategistAgent()
        self.writer_agent = WriterAgent()

        self.delivery_manager = DeliveryManager()

        self.telegram = TelegramClient()

    def run(
        self,
        category: str,
        subject: str,
        topic: str,
    ):

        try:

            self.telegram.send_message(
                f"""
[STARTED] Content Generation Started

Category: {category}
Subject: {subject}
Topic: {topic}
"""
            )

            self.telegram.send_message(
                "[STARTED] Research Phase Started"
            )

            research = self.research_agent.run(
                category=category,
                subject=subject,
                topic=topic,
            )

            self.research_agent.save(
                sprint_id=topic,
                research=research,
            )

            self.telegram.send_message(
                "[SUCCESS] Research Completed"
            )

            self.telegram.send_message(
                "[STARTED] Content Strategy Started"
            )

            ideas = self.strategist_agent.run(
                research
            )

            self.strategist_agent.save(
                sprint_id=topic,
                ideas=ideas,
            )

            self.telegram.send_message(
                "[SUCCESS] Content Strategy Completed"
            )

            self.telegram.send_message(
                "[STARTED] Post Generation Started"
            )

            posts = self.writer_agent.run(
                research,
                ideas,
            )

            self.writer_agent.save(
                sprint_id=topic,
                posts=posts,
            )

            self.telegram.send_message(
                "[SUCCESS] Post Generation Completed"
            )

            self.delivery_manager.deliver(
                posts
            )

            self.telegram.send_message(
                "[SUCCESS] Delivery Completed"
            )

            return posts

        except Exception as e:

            self.telegram.send_message(
                f"""
[FAILED] Pipeline Failed

Topic: {topic}

Error:
{str(e)}
"""
            )

            raise
        