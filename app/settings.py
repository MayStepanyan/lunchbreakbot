"""
Application settings
"""

import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

current_dir = os.path.dirname(__file__)

# Construct the absolute path of the .env file by joining the directory path with the filename
env_file_path = os.path.join(current_dir, '..', '.env')


class EnvVarsBase(BaseSettings):
    """Base configuration that reads from a .env file"""
    model_config = SettingsConfigDict(env_file=env_file_path, extra='ignore')


class BotSettings(EnvVarsBase):
    """Base configuration for the app"""
    token: str = Field(description="The telegram API access token. Should be generated with @botfather")


class ClientSettings(EnvVarsBase):
    """Configurations for the client that connects with DB"""
    host: str = Field(description="The host for Redis DB connection")
    port: int = Field(description="The port for Redis DB connection")
