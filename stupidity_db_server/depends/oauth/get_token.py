__all__ = ("get_token",)

from typing import TYPE_CHECKING

from fastapi import Depends

from .. import get

if TYPE_CHECKING:
    from fastapi import Request
    from fastapi_discord import DiscordOAuthClient


def get_token(
    *,
    oauth: DiscordOAuthClient = Depends(get.oauth),
    request: Request
) -> str:
    return oauth.get_token(request)
