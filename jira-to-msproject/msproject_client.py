import win32com.client
from datetime import datetime
from typing import List
from models import JiraIssue
from config import settings
import logging
import os

def export_to_msproject(issues: List[JiraIssue]):
    """
    Export Jira issues to Microsoft Project
    """
    try:
        app = win32com.client.Dispatch("MSProject.Application")
        app.Visible = True

        # Create new project
        project = app.Projects.Add()

        # Set project properties
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        project.Name = f"Jira Export - {settings.JIRA_PROJECT_KEY} - {timestamp}"

        # Set project start date to earliest task date
        if issues:
            start_dates = [issue.start_date for issue in issues if issue.start_date]
            if start_dates:
                project.ProjectStart = min(start_dates)

        # Add tasks
        for issue in issues:
            try:
                task = project.Tasks.Add(issue.summary)
                if issue.start_date:
                    task.Start = issue.start_date
                if issue.due_date:
                    task.Finish = issue.due_date
                if issue.assignee:
                    task.ResourceNames = issue.assignee
                if issue.duration_days:
                    task.Duration = f"{issue.duration_days}d"

                logging.info(f"Added task: {issue.summary}")

            except Exception as e:
                logging.error(f"Failed to add task {issue.summary}: {str(e)}")

        # Save project
        output_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(output_dir, exist_ok=True)

        filename = f"Jira_Export_{settings.JIRA_PROJECT_KEY}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mpp"
        output_path = os.path.join(output_dir, filename)
        project.SaveAs(output_path)

        logging.info(f"Project saved to: {output_path}")

    except Exception as e:
        logging.error(f"MS Project export failed: {str(e)}")
        raise