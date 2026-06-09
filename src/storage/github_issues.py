import os

from datetime import datetime

from github import Github

from dotenv import load_dotenv

load_dotenv()


class GitHubIssueStateManager:

    SPRINT_LABEL = "content-sprint"

    def __init__(self):

        github = Github(
            os.getenv(
                "GITHUB_TOKEN"
            )
        )

        self.repo = github.get_repo(
            f"{os.getenv('GITHUB_REPO_OWNER')}/"
            f"{os.getenv('GITHUB_REPO_NAME')}"
        )

    def create_sprint(self):

        sprint_id = (
            datetime.utcnow()
            .strftime("%Y-%m-%d")
        )

        issue = self.repo.create_issue(
            title=f"Sprint-{sprint_id}",
            body=f"""
Status: WAITING

Category:
Subject:
Topic:

CreatedAt:
{datetime.utcnow().isoformat()}
""",
            labels=[
                self.SPRINT_LABEL
            ],
        )

        return issue.number

    def get_latest_sprint(self):

        issues = list(
            self.repo.get_issues(
                state="open",
                labels=[
                    self.SPRINT_LABEL
                ],
            )
        )

        if not issues:
            return None

        issues.sort(
            key=lambda issue:
                issue.created_at,
            reverse=True,
        )

        return issues[0]

    def save_topic(
        self,
        category,
        subject,
        topic,
    ):

        issue = (
            self.get_latest_sprint()
        )

        if not issue:

            raise RuntimeError(
                "No active sprint found"
            )

        issue.edit(
            body=f"""
Status: PROCESSING

Category:
{category}

Subject:
{subject}

Topic:
{topic}

StartedAt:
{datetime.utcnow().isoformat()}
"""
        )

    def complete_sprint(self):

        issue = (
            self.get_latest_sprint()
        )

        if not issue:
            return

        issue.edit(
            body=f"""
{issue.body}

CompletedAt:
{datetime.utcnow().isoformat()}
""",
            state="closed",
        )

    def fail_sprint(
        self,
        reason: str,
    ):

        issue = (
            self.get_latest_sprint()
        )

        if not issue:
            return

        issue.edit(
            body=f"""
{issue.body}

Status: FAILED

Reason:
{reason}

FailedAt:
{datetime.utcnow().isoformat()}
""",
        )

    def get_status(self):

        issue = (
            self.get_latest_sprint()
        )

        if not issue:
            return None

        body = issue.body or ""

        if "Status: WAITING" in body:
            return "WAITING"

        if "Status: PROCESSING" in body:
            return "PROCESSING"

        if "Status: FAILED" in body:
            return "FAILED"

        return "UNKNOWN"
    