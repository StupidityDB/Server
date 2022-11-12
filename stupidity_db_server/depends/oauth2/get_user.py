from __future__ import annotations

__all__ = ("get_user",)

from typing import TYPE_CHECKING

from fastapi import Depends

from .get_oauth2 import get_oauth2

if TYPE_CHECKING:
    from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, User as DiscordUser
    from fastapi import Request


async def get_user(
    request: Request, oauth2: DiscordOAuth2Client = Depends(get_oauth2)
) -> DiscordUser:
    return await oauth2.user(request)
