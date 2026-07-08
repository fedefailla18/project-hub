from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class ProjectStatus(BaseModel):
    name: str
    path: str
    stack: str
    status: str
    health_score: Literal["green", "yellow", "red"]
    health_summary: str
    branch: str
    last_commit_hash: str
    last_commit_message: str
    last_commit_date: str
    last_commit_age_days: int
    uncommitted_files: list[str]
    is_dirty: bool
    has_claude_md: bool
    has_gemini_md: bool
    has_roadmap: bool
    dev_server_running: bool | None  # None if project has no dev port


class WorkspaceState(BaseModel):
    scanned_at: datetime
    projects: list[ProjectStatus]

    @property
    def red_projects(self) -> list[ProjectStatus]:
        return [p for p in self.projects if p.health_score == "red"]

    @property
    def dirty_projects(self) -> list[ProjectStatus]:
        return [p for p in self.projects if p.is_dirty]
