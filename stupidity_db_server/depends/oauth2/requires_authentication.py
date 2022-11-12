from __future__ import annotations

__all__ = ("requires_authentication",)

from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ._get_oauth2 import _get_oauth2

if TYPE_CHECKING:
    from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, User as DiscordUser


async def requires_authentication(
    oauth2: DiscordOAuth2Client = Depends(_get_oauth2),
    bearer: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())
) -> DiscordUser:
    return await oauth2.requires_authorization(bearer)
