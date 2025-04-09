from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class JiraIssue(BaseModel):
    id: str
    key: str
    summary: str
    assignee: Optional[str] = "Unassigned"
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    duration_days: int = 1
    status: str
    issue_type: str

    @classmethod
    def from_api_response(cls, data: dict):
        fields = data.get("fields", {})

        # Parse dates
        start_date = None
        if fields.get("created"):
            start_date = datetime.strptime(fields["created"][:19], "%Y-%m-%dT%H:%M:%S")

        due_date = None
        if fields.get("duedate"):
            due_date = datetime.strptime(fields["duedate"], "%Y-%m-%d")

        # Calculate duration
        duration = 1
        if start_date and due_date:
            duration = max(1, (due_date - start_date).days)

        return cls(
            id=data.get("id"),
            key=data.get("key"),
            summary=fields.get("summary", "Untitled Task"),
            assignee=fields.get("assignee", {}).get("displayName", "Unassigned"),
            start_date=start_date,
            due_date=due_date,
            duration_days=duration,
            status=fields.get("status", {}).get("name", "Unknown"),
            issue_type=fields.get("issuetype", {}).get("name", "Task")
        )