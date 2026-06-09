import os
import time
import logging
from typing import Type, TypeVar

import requests

from pydantic import BaseModel, ValidationError
from requests.exceptions import Timeout, RequestException
from json_repair import repair_json

from src.models.research import ResearchResponse
from src.models.content_ideas import ContentIdeasResponse
from src.models.linkedin_posts import LinkedInPostsResponse

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class CloudflareMultiIPGeminiClient:

    def __init__(self):

        self.proxy_urls = []

        workers = [
            ("CLOUDFLARE_WORKER_US_URL", "us-east"),
            ("CLOUDFLARE_WORKER_EU_URL", "europe"),
            ("CLOUDFLARE_WORKER_ASIA_URL", "asia"),
            ("CLOUDFLARE_WORKER_AU_URL", "australia"),
        ]

        for env_key, name in workers:

            url = os.getenv(env_key)

            if not url:
                continue

            self.proxy_urls.append(
                {
                    "name": name,
                    "url": url,
                    "failures": 0,
                    "successes": 0,
                    "validation_failures": 0,
                    "disabled_until": 0,
                }
            )

        if not self.proxy_urls:
            raise ValueError(
                "No Cloudflare workers configured"
            )

        logger.info(
            "Loaded %s Cloudflare workers",
            len(self.proxy_urls),
        )

    def _available_workers(self):

        now = time.time()

        available = [
            worker
            for worker in self.proxy_urls
            if worker["disabled_until"] < now
        ]

        if available:
            return available

        logger.warning(
            "All workers disabled. Re-enabling."
        )

        for worker in self.proxy_urls:
            worker["disabled_until"] = 0

        return self.proxy_urls

    def _select_worker(self):

        workers = self._available_workers()

        workers.sort(
            key=lambda worker: (
                worker["failures"],
                -worker["successes"],
            )
        )

        return workers[0]

    def _disable_worker(
        self,
        worker: dict,
        seconds: int,
    ):

        worker["disabled_until"] = (
            time.time() + seconds
        )

        logger.warning(
            "Worker %s disabled for %s seconds",
            worker["name"],
            seconds,
        )

    def _extract_text(
        self,
        response_json: dict,
    ) -> str:

        try:

            return (
                response_json["candidates"][0]
                ["content"]["parts"][0]["text"]
            )

        except Exception as e:

            logger.exception(
                "Invalid Gemini response structure"
            )

            raise RuntimeError(
                f"Invalid Gemini response: {response_json}"
            ) from e

    def _parse_response(
        self,
        response_json: dict,
        response_model: Type[T],
    ) -> T:

        text_content = self._extract_text(
            response_json
        )

        try:

            return (
                response_model
                .model_validate_json(
                    text_content
                )
            )

        except ValidationError:

            logger.warning(
                "Validation failed. "
                "Attempting JSON repair."
            )

            try:

                repaired_json = repair_json(
                    text_content
                )

                return (
                    response_model
                    .model_validate_json(
                        repaired_json
                    )
                )

            except Exception:

                logger.exception(
                    "JSON repair failed"
                )

                raise

    def _call_gemini(
        self,
        prompt: str,
        temperature: float,
        response_model: Type[T],
    ) -> T:

        model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        max_attempts = len(
            self.proxy_urls
        )

        errors = []

        for _ in range(max_attempts):

            worker = self._select_worker()

            logger.info(
                "Using worker: %s",
                worker["name"],
            )

            try:

                response = requests.post(
                    f"{worker['url']}/v1beta/models/{model}:generateContent",
                    json={
                        "contents": [
                            {
                                "parts": [
                                    {
                                        "text": prompt
                                    }
                                ]
                            }
                        ],
                        "generationConfig": {
                            "temperature": temperature,
                            "responseMimeType":
                                "application/json",
                        },
                    },
                    headers={
                        "Content-Type":
                            "application/json"
                    },
                    timeout=120,
                )

                if response.status_code == 503:

                    worker["failures"] += 1

                    errors.append(
                        f"{worker['name']}:503"
                    )

                    self._disable_worker(
                        worker,
                        300,
                    )

                    continue

                if response.status_code == 429:

                    worker["failures"] += 1

                    errors.append(
                        f"{worker['name']}:429"
                    )

                    self._disable_worker(
                        worker,
                        120,
                    )

                    continue

                response.raise_for_status()

                result = self._parse_response(
                    response.json(),
                    response_model,
                )

                worker["successes"] += 1
                worker["failures"] = 0

                logger.info(
                    "Worker %s succeeded",
                    worker["name"],
                )

                return result

            except ValidationError as e:

                worker[
                    "validation_failures"
                ] += 1

                errors.append(
                    f"{worker['name']}:validation"
                )

                logger.warning(
                    "Validation failure on %s",
                    worker["name"],
                )

                continue

            except Timeout as e:

                worker["failures"] += 1

                errors.append(
                    f"{worker['name']}:timeout"
                )

                self._disable_worker(
                    worker,
                    120,
                )

                logger.warning(
                    "Timeout on %s",
                    worker["name"],
                )

                continue

            except RequestException as e:

                worker["failures"] += 1

                errors.append(
                    f"{worker['name']}:request"
                )

                self._disable_worker(
                    worker,
                    60,
                )

                logger.warning(
                    "Request failure on %s",
                    worker["name"],
                )

                continue

            except Exception as e:

                worker["failures"] += 1

                errors.append(
                    f"{worker['name']}:{type(e).__name__}"
                )

                self._disable_worker(
                    worker,
                    60,
                )

                logger.exception(
                    "Unexpected worker failure"
                )

                continue

        raise RuntimeError(
            "All workers failed. "
            + " | ".join(errors)
        )

    def research(
        self,
        prompt: str,
    ) -> ResearchResponse:

        return self._call_gemini(
            prompt=prompt,
            temperature=0.7,
            response_model=ResearchResponse,
        )

    def content_ideas(
        self,
        prompt: str,
    ) -> ContentIdeasResponse:

        return self._call_gemini(
            prompt=prompt,
            temperature=0.8,
            response_model=ContentIdeasResponse,
        )

    def linkedin_posts(
        self,
        prompt: str,
    ) -> LinkedInPostsResponse:

        return self._call_gemini(
            prompt=prompt,
            temperature=0.8,
            response_model=LinkedInPostsResponse,
        )

    def get_status(self):

        now = time.time()

        return {
            "workers": [
                {
                    "name": worker["name"],
                    "successes": worker[
                        "successes"
                    ],
                    "failures": worker[
                        "failures"
                    ],
                    "validation_failures":
                        worker[
                            "validation_failures"
                        ],
                    "active":
                        worker["disabled_until"]
                        < now,
                }
                for worker in self.proxy_urls
            ]
        }