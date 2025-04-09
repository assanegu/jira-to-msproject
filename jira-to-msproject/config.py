import os
from dotenv import load_dotenv
from pydantic import BaseSettings

class Settings(BaseSettings):
    JIRA_EMAIL: str
    JIRA_API_TOKEN: str
    JIRA_DOMAIN: str
    JIRA_PROJECT_KEY: str
    MAX_RESULTS: int = 200
    DEFAULT_TASK_DURATION_DAYS: int = 1

    class Config:
        env_file = ".env"

# Load environment variables
load_dotenv()
settings = Settings()