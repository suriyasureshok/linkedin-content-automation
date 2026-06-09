import logging

from fastapi import (
    FastAPI,
    Request,
    BackgroundTasks,
)

from src.integrations.telegram import (
    TelegramClient,
)

from src.pipelines.content_pipeline import (
    ContentPipeline,
)

from src.storage.github_issues import (
    GitHubIssueStateManager,
)

logger = logging.getLogger(__name__)

app = FastAPI()

pipeline = ContentPipeline()

_generation_running = False


def run_generation(parsed):

    global _generation_running

    if _generation_running:

        logger.warning(
            "Generation already running"
        )

        TelegramClient.send_message(
            "[WARNING] Content generation already running."
        )

        return

    _generation_running = True

    try:

        logger.info(
            "Starting content generation"
        )

        pipeline.run(
            category=parsed["category"],
            subject=parsed["subject"],
            topic=parsed["topic"],
        )

        state = GitHubIssueStateManager()

        state.complete_sprint()

        logger.info(
            "Sprint completed successfully"
        )

    except Exception as e:

        logger.exception(
            "Pipeline execution failed"
        )

        TelegramClient.send_message(
            f"""
[FAILED] Content Generation Failed

Topic:
{parsed['topic']}

Reason:
{str(e)}
"""
        )

    finally:

        _generation_running = False


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "generation_running":
            _generation_running,
    }


@app.post("/telegram")
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
):

    try:

        payload = await request.json()

    except Exception as e:
        state = GitHubIssueStateManager()

        state.fail_sprint(
            str(e)
        )

        logger.exception(
            "Invalid JSON payload"
        )

        return {
            "status": "invalid_payload"
        }

    message = payload.get(
        "message"
    )

    if not message:

        return {
            "status": "ignored"
        }

    text = message.get(
        "text"
    )

    if not text:

        return {
            "status": "ignored"
        }

    parsed = (
        TelegramClient.process_message(
            text
        )
    )

    if not parsed:

        return {
            "status": "ignored"
        }

    background_tasks.add_task(
        run_generation,
        parsed,
    )

    logger.info(
        "Generation accepted"
    )

    return {
        "status": "accepted"
    }