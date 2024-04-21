"""
Global variables
"""

from enum import Enum

from app.settings import AppSettings


class DefaultResponses(Enum):
    """Default responses of the app"""
    GREETING: str = "Hi, how can I help you?"

SETTINGS = AppSettings()
