import os
from datetime import datetime

from github import Github

from dotenv import load_dotenv

load_dotenv()


class GitHubIssueStateManager:

    def __init__(self):

        github = Github(os.getenv("GITHUB_TOKEN"))

        self.repo = github.get_repo(
            f"{os.getenv('GITHUB_REPO_OWNER')}/{os.getenv('GITHUB_REPO_NAME')}"
        )

    def create_sprint(self):

        sprint_id = datetime.now().strftime("%Y-%m-%d")

        issue = self.repo.create_issue(
            title=f"Sprint-{sprint_id}",
            body=f"""
Status: WAITING

Category:
Subject:
Topic:

CreatedAt:
{datetime.now().isoformat()}
""",
        )

        return issue.number

    def get_latest_sprint(self):

        issues = list(self.repo.get_issues(state="open"))

        sprint_issues = [issue for issue in issues if issue.title.startswith("Sprint-")]

        if not sprint_issues:
            return None

        return sprint_issues[0]

    def save_topic(self, category, subject, topic):

        issue = self.get_latest_sprint()

        issue.edit(
            body=f"""
Status: PROCESSING

Category:
{category}

Subject:
{subject}

Topic:
{topic}
"""
        )

    def complete_sprint(self):

        issue = self.get_latest_sprint()

        issue.edit(state="closed")

    def get_status(self):

        issue = self.get_latest_sprint()

        if not issue:
            return None

        body = issue.body

        if "WAITING" in body:
            return "WAITING"

        if "PROCESSING" in body:
            return "PROCESSING"

        return "UNKNOWN"
