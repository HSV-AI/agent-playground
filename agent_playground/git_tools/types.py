from pydantic import BaseModel, Field
from typing import List, Optional

class FileChange(BaseModel):
    """Represents a single file change in a Git diff."""
    path: str = Field(description="The path of the changed file.")
    status: str = Field(description="The status of the file change (e.g., 'A' for added, 'M' for modified, 'D' for deleted).")
    insertions: int = Field(description="Number of lines inserted in the file.")
    deletions: int = Field(description="Number of lines deleted from the file.")

class GitDiffSummary(BaseModel):
    """Summary of changes between two Git references."""
    current_branch: str = Field(description="The name of the current Git branch.")
    target_branch: str = Field(description="The name of the target Git branch (e.g., 'main' or 'master').")
    commit_count: int = Field(description="The number of commits between the current and target branch.")
    file_changes: List[FileChange] = Field(description="A list of individual file changes.")
    summary_message: str = Field(description="A human-readable summary of the changes.")

class MergeRequestSuggestion(BaseModel):
    """Suggested content for a merge request."""
    title: str = Field(description="A concise title for the merge request.")
    description: str = Field(description="A detailed description of the changes and their purpose.", )
    suggested_reviewers: Optional[str] = Field(default=None, description="Comma-separated list of suggested reviewers for the merge request.")
    diff_summary: GitDiffSummary = Field(description="The summary of changes included in this merge request.")
    error_message: str = Field(default="", description="An error message if the merge request suggestion failed, otherwise empty.")
