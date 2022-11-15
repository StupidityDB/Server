from __future__ import annotations

__all__ = ("get_user",)

from datetime import datetime as DateTime, timezone as TimeZone
from typing import TYPE_CHECKING

from asyncpg import Connection as PostgresConnection
from fastapi import Depends
from fastapi_discord import Unauthorized

from .get_token import get_token
from .types import DiscordUser
from .. import get

if TYPE_CHECKING:
    from asyncpg import Record


async def get_user(
    *,
    db: PostgresConnection = Depends(get.db),
    token: str = Depends(get_token),
) -> DiscordUser:
    user_raw: Record | None = await db.fetchrow(
        """
        SELECT
            id, username, discriminator, avatar_url, token_expires_at
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
