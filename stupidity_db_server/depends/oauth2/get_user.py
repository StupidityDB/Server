from __future__ import annotations

__all__ = ("get_user",)

from typing import TYPE_CHECKING

from fastapi import Depends

from ._get_oauth2 import _get_oauth2

if TYPE_CHECKING:
    from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, User as DiscordUser
    from fastapi import Request


async def get_user(
    request: Request, oauth2: DiscordOAuth2Client = Depends(_get_oauth2)
) -> DiscordUser:
    return await oauth2.user(request)
