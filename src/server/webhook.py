from fastapi import FastAPI
from pydantic import BaseModel

from src.integrations.telegram import TelegramClient
from src.pipelines.content_pipeline import ContentPipeline
from src.storage.github_issues import GitHubIssueStateManager


app = FastAPI()

pipeline = ContentPipeline()


class TelegramMessage(BaseModel):
    text: str


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }

@app.post("/telegram")
async def telegram_webhook(
    payload: TelegramMessage
):

    text = payload.text

    parsed = TelegramClient.process_message(
        text
    )

    if not parsed:
        return {
            "status": "ignored"
        }

    pipeline.run(
        category=parsed["category"],
        subject=parsed["subject"],
        topic=parsed["topic"]
    )

    GitHubIssueStateManager.complete_sprint()

    return {
        "status": "success"
    }
