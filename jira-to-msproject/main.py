#!/usr/bin/env python3
"""
Main entry point for Jira to MS Project exporter
"""

from jira_client import fetch_jira_issues
from msproject_client import export_to_msproject
from models import JiraIssue
from config import settings
import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('jira_export.log'),
            logging.StreamHandler()
        ]
    )

def main():
    configure_logging()
    logging.info("Starting Jira to MS Project export")

    try:
        # Fetch issues from Jira
        logging.info(f"Fetching issues from project {settings.JIRA_PROJECT_KEY}")
        issues = fetch_jira_issues()

        if not issues:
            logging.warning("No issues found in Jira")
            return

        # Export to MS Project
        logging.info(f"Exporting {len(issues)} issues to MS Project")
        export_to_msproject(issues)

        logging.info("Export completed successfully")

    except Exception as e:
        logging.error(f"Export failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()