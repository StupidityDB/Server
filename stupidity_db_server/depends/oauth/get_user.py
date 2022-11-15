__all__ = ("get_user",)

from datetime import datetime as DateTime, timezone as TimeZone

from asyncpg import Connection as PGConnection, Record
from fastapi import Depends, Request
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, Unauthorized

from stupidity_db_server.depends.get.db import db
from stupidity_db_server.depends.get.oauth import oauth
from stupidity_db_server.depends.oauth.types.discord_user import DiscordUser


async def get_user(
    *,
    db: PGConnection = Depends(db),
    oauth2: DiscordOAuth2Client = Depends(oauth),
    request: Request
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
