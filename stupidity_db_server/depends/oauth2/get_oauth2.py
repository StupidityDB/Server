__all__ = ("get_oauth2",)

from fastapi import Request
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client


def get_oauth2(request: Request) -> DiscordOAuth2Client:
    return request.app.oauth2
