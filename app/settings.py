"""
Application settings
"""

import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

current_dir = os.path.dirname(__file__)

# Construct the absolute path of the .env file by joining the directory path with the filename
env_file_path = os.path.join(current_dir, '..', '.env')


class AppSettings(BaseSettings):
    """Base configuration for the app"""
    model_config = SettingsConfigDict(env_file=env_file_path)
    token: str = Field(description="The telegram API access token. Should be generated with @botfather")
