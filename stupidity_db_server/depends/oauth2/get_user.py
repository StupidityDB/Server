__all__ = ("get_user",)

from datetime import datetime as DateTime, timezone as TimeZone

from asyncpg import Connection as PGConnection, Record
from fastapi import Depends, Request
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, Unauthorized

from .discord_user import DiscordUser
from .get_oauth2 import get_oauth2
from ..get_db import get_db


async def get_user(
    *,
    request: Request,
    db: PGConnection = Depends(get_db),
    oauth2: DiscordOAuth2Client = Depends(get_oauth2)
) -> DiscordUser:
    token: str = oauth2.get_token(request)
    user_raw: Record | None = await db.fetchrow(
        """
        SELECT 
            (id, username, discriminator, avatar_url, token_expires_at) 
        FROM 
            users 
        WHERE
            token = $1
        """,
        token
    )

    if not user_raw or user_raw["token_expires_at"] < DateTime.now(TimeZone.utc):
        raise Unauthorized

    return DiscordUser(**user_raw)
