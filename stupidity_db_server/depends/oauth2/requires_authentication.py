__all__ = ("requires_authentication",)

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, User as DiscordUser

from .get_oauth2 import get_oauth2


async def requires_authentication(
    oauth2: DiscordOAuth2Client = Depends(get_oauth2),
    bearer: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())
) -> DiscordUser:
    return await oauth2.requires_authorization(bearer)
