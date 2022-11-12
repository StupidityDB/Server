__all__ = ("get_user",)

from fastapi import Depends, Request
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, User as DiscordUser

from .get_oauth2 import get_oauth2


async def get_user(
    *, request: Request, oauth2: DiscordOAuth2Client = Depends(get_oauth2)
) -> DiscordUser:
    return await oauth2.user(request)
