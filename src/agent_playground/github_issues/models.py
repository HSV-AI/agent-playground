from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class GitHubIssue(BaseModel):
    """Represents a single GitHub issue."""
    title: str = Field(description="The title of the GitHub issue.")
    url: str = Field(description="The URL of the GitHub issue.")
    state: str = Field(description="The current state of the issue (e.g., 'open', 'closed').")
    updated_at: datetime = Field(description="The last time the issue was updated.")
    labels: List[str] = Field(description="A list of labels associated with the issue.")
    author: str = Field(description="The GitHub username of the issue author.")

class GitHubIssueReport(BaseModel):
    """A report of GitHub issues."""
    issues: List[GitHubIssue] = Field(description="A list of GitHub issues found.")
    repository: str = Field(description="The name of the repository the issues were fetched from.")
    owner: str = Field(description="The owner of the repository.")
    report_summary: str = Field(description="A summary of the issues found and reported.")
    error_message: str = Field(default="", description="An error message if the report generation failed, otherwise empty.")
