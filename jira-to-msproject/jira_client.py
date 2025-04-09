import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from typing import List
from config import settings
from models import JiraIssue
import logging

def fetch_jira_issues() -> List[JiraIssue]:
    """
    Fetch issues from Jira using REST API
    """
    url = f"https://{settings.JIRA_DOMAIN}/rest/api/3/search"
    auth = HTTPBasicAuth(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}

    jql = f"project={settings.JIRA_PROJECT_KEY} AND status NOT IN (Done, Closed)"
    params = {
        "jql": jql,
        "maxResults": settings.MAX_RESULTS,
        "fields": "summary,assignee,duedate,created,status,issuetype"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=auth,
            params=params,
            timeout=30
        )
        response.raise_for_status()

        issues = []
        for item in response.json().get("issues", []):
            try:
                issues.append(JiraIssue.from_api_response(item))
            except Exception as e:
                logging.warning(f"Skipping issue {item.get('id')}: {str(e)}")

        return issues

    except requests.exceptions.RequestException as e:
        logging.error(f"Jira API request failed: {str(e)}")
        raise

def format_jira_date(date_str: str) -> datetime:
    """Parse Jira date string into datetime object"""
    return datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")