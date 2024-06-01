"""
Global variables
"""

from enum import Enum

from app.settings import BotSettings, ClientSettings

BOT_SETTINGS = BotSettings()
CLIENT_SETTINGS = ClientSettings()


class DefaultResponses(Enum):
    """Default responses of the app"""
    GREETING: str = "Hi, how can I help you?"
