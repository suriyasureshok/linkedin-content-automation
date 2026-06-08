from src.agents.researcher import ResearchAgent
from src.agents.strategist import StrategistAgent
from src.agents.writer import WriterAgent

from src.delivery.delivery_manager import DeliveryManager

research_agent = ResearchAgent()

research = research_agent.run(
    category="Backend Engineering", subject="Redis", topic="Memory Management"
)

strategist = StrategistAgent()

ideas = strategist.run(research)

writer = WriterAgent()

posts = writer.run(research, ideas)

delivery = DeliveryManager()

delivery.deliver(posts)
