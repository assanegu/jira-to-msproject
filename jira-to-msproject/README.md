# Jira to Microsoft Project Exporter

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python tool that exports Jira issues to Microsoft Project format (.mpp), preserving task details, dates, and assignments.

## Features

-  Export Jira issues to MS Project with a single command
-  Preserve task names, assignees, start dates, and due dates
-  Automatic duration calculation
-  Configurable through environment variables
-  Logging for troubleshooting
-  Handles pagination for large projects

## Prerequisites

Before using this tool, ensure you have:

- Python 3.8 or higher
- Microsoft Project installed (2016 or newer recommended)
- Jira Cloud account with API access
- Permission to access the Jira project you want to export

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/jira-to-msproject.git
   cd jira-to-msproject
   
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   
3. Set up your environment variables:
   ```bash
    JIRA_EMAIL=your.email@company.com
    JIRA_API_TOKEN=your_api_token_here
    JIRA_DOMAIN=your-domain.atlassian.net
    JIRA_PROJECT_KEY=PROJ


## Usage

### Basic Export
   ```bash
     python main.py
   ```

This will:

Fetch all active issues from your Jira project
Create a new MS Project file
Save it in the exports directory with a timestamp
Advanced Options

You can modify these in config.py:

MAX_RESULTS: Change the maximum number of issues to fetch (default: 200)
DEFAULT_TASK_DURATION_DAYS: Default duration when dates aren't available (default: 1)
Output

MS Project files are saved in /exports directory
Logs are written to jira_export.log
Configuration

## Environment Variables

```
| Variable          | Description                                      | Required |
|-------------------|--------------------------------------------------|----------|
| `JIRA_EMAIL`     | Email for Jira account                           | Yes      |
| `JIRA_API_TOKEN` | Jira API token                                   | Yes      |
| `JIRA_DOMAIN`    | Your Jira domain (e.g., company.atlassian.net)   | Yes      |
| `JIRA_PROJECT_KEY` | Project key to export (e.g., PROJ)              | Yes      |
```

Jira Query Customization

Modify the JQL query in jira_client.py to change which issues are exported:


jql = f"project={settings.JIRA_PROJECT_KEY} AND status NOT IN (Done, Closed)"

