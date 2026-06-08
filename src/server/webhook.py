from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel

from src.integrations.telegram import TelegramClient
from src.pipelines.content_pipeline import ContentPipeline
from src.storage.github_issues import GitHubIssueStateManager


app = FastAPI()

pipeline = ContentPipeline()


def run_generation(parsed):

    pipeline.run(
        category=parsed["category"], subject=parsed["subject"], topic=parsed["topic"]
    )

    state = GitHubIssueStateManager()

    state.complete_sprint()


class TelegramMessage(BaseModel):
    text: str


@app.get("/health")
async def health():

    return {"status": "ok"}


@app.post("/telegram")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):

    payload = await request.json()

    message = payload.get("message")

    if not message:
        return {"status": "ignored"}

    text = message.get("text")

    if not text:
        return {"status": "ignored"}

    parsed = TelegramClient.process_message(text)

    if not parsed:
        return {"status": "ignored"}

    background_tasks.add_task(run_generation, parsed)

    return {"status": "accepted"}
