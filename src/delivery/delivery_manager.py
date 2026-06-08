from src.integrations.telegram import TelegramClient
from src.models.linkedin_posts import LinkedInPostsResponse


class DeliveryManager:

    def __init__(self):

        self.telegram = TelegramClient()

    def deliver(
        self,
        posts: LinkedInPostsResponse
    ):

        self.telegram.send_message(
            f"[SUCCESS] Generated {len(posts.posts)} LinkedIn Posts"
        )

        for index, post in enumerate(
            posts.posts,
            start=1
        ):

            message = f"""
POST #{index}

TYPE:
{post.content_type}

TITLE:
{post.title}

{post.body}
"""

            self.telegram.send_long_message(
                message
            )

        self.telegram.send_message(
            "[COMPLETED] Delivery Completed"
        )