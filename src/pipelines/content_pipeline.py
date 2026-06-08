from src.agents.researcher import ResearchAgent
from src.agents.strategist import StrategistAgent
from src.agents.writer import WriterAgent

from src.delivery.delivery_manager import DeliveryManager


class ContentPipeline:

    def __init__(self):

        self.research_agent = ResearchAgent()
        self.strategist_agent = StrategistAgent()
        self.writer_agent = WriterAgent()

        self.delivery_manager = DeliveryManager()

    def run(self, category: str, subject: str, topic: str):

        research = self.research_agent.run(
            category=category, subject=subject, topic=topic
        )

        self.research_agent.save(sprint_id=topic, research=research)

        ideas = self.strategist_agent.run(research)

        self.strategist_agent.save(sprint_id=topic, ideas=ideas)

        posts = self.writer_agent.run(research, ideas)

        self.writer_agent.save(sprint_id=topic, posts=posts)

        self.delivery_manager.deliver(posts)

        return posts
