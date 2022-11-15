__all__ = ("oauth",)

from fastapi import Request
from fastapi_discord import DiscordOAuthClient


def oauth(*, request: Request) -> DiscordOAuthClient:
    return request.app.oauth2
