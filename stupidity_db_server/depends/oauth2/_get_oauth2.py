from __future__ import annotations

__all__ = ("_get_oauth2",)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client
    from fastapi import Request


def _get_oauth2(request: Request) -> DiscordOAuth2Client:
    return request.app.state.oauth2
