from __future__ import annotations

__all__ = ("router",)

from asyncio import gather as await_parallel
from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from typing import TYPE_CHECKING

from asyncpg import Connection as PostgresConnection
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi_discord.exceptions import InvalidToken

from ..depends import get, oauth
from ..ductape import StupidOAuthClient
from ..utils import generate_examples

if TYPE_CHECKING:
    from asyncpg import Record

router = APIRouter(
    prefix="/authorize",
    tags=["Authorization"]
)


@router.get(
    "/",
    summary="Authorize with Discord.",
    description="This endpoint will redirect you to Discord's OAuth page.",
    response_description="Redirect to the Discord OAuth page.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse
)
async def authorize(
    *,
    auth: StupidOAuthClient = Depends(get.oauth)
) -> RedirectResponse:
    return RedirectResponse(auth.oauth_login_url)


@router.get(
    "/callback",
    summary="Callback for Discord OAuth.",
    description="You will be redirected here after authorizing with Discord.",
    response_description="You access token.",
    responses=generate_examples(
        {
            status.HTTP_200_OK: {
                "detail": "Successful.",
                "token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            },
            status.HTTP_401_UNAUTHORIZED: {
                "detail": "The provided authorization code is invalid."
            }
        }
    )
)
async def authorize_callback(
    *,
    db: PostgresConnection = Depends(get.db),
    auth: StupidOAuthClient = Depends(get.oauth),
    code: str = Query(
        description="The authorization code returned by Discord.",
        example="Waf3Tvx8kdos5hta3gcJ8GndJSoBqI"
    )
) -> ORJSONResponse:
    try:
        access_token, renew_token, expires_in = await auth.get_access_token(code)

    except InvalidToken:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The provided authorization code is invalid."
        )

    user = oauth.DiscordUser(**await auth.get_user_raw(access_token))

    await await_parallel(
        db.execute(
            """
            INSERT INTO users
                (id, username, discriminator, avatar_url, token, token_expires_at, renew_token)
            VALUES
                ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT
                (id)
            DO UPDATE SET
                username = $2,
                discriminator = $3,
                avatar_url = $4,
                token = $5,
                token_expires_at = $6,
                renew_token = $7
            """,
            user.id,
            user.username,
            user.discriminator,
            user.avatar_url,
            access_token,
            DateTime.now(TimeZone.utc) + TimeDelta(seconds=expires_in),
            renew_token
        ),
        db.execute(
            """
            INSERT INTO token_history
                (token, id)
            VALUES
                ($1, $2)
            """,
            access_token,
            user.id
        )
    )

    return ORJSONResponse(
        {
            "detail": "Successful.",
            "token": access_token
        }
    )


@router.post(
    "/renew",
    summary="Renew the access token.",
    description="This endpoint will renew the access token for the user.",
    response_description="The renewed access token.",
    responses=generate_examples(
        {
            status.HTTP_200_OK: {
                "detail": "Successful.",
                "new_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            },
            status.HTTP_401_UNAUTHORIZED: {
                "detail": "The provided token is invalid."
            }
        }
    )
)
async def renew_token(
    *,
    db: PostgresConnection = Depends(get.db),
    auth: StupidOAuthClient = Depends(get.oauth),
    token: str = Body(
        description="The access token.",
        example="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        embed=True
    )
) -> ORJSONResponse:
    user_id: int | None = await db.fetchval(
        """
        SELECT
            id
        FROM
            token_history
        WHERE
            token = $1
        """,
        token
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The provided token is invalid."
        )

    user_data: Record = await db.fetchrow(
        """
        SELECT
            token, token_expires_at, renew_token
        FROM
            users
        WHERE
            id = $1
        """,
        user_id
    )

    if DateTime.now(TimeZone.utc) < user_data["token_expires_at"]:
        # Token is still valid.
        return ORJSONResponse(
            {
                "detail": "Successful.",
                "new_token": user_data["token"]
            }
        )

    access_token, renew_token, expires_in = await auth.refresh_access_token(
        user_data["renew_token"]
    )

    await await_parallel(
        db.execute(
            """
            UPDATE
                users
            SET
                token = $1,
                token_expires_at = $2,
                renew_token = $3
            WHERE
                id = $4
            """,
            access_token,
            DateTime.now(TimeZone.utc) + TimeDelta(seconds=expires_in),
            renew_token,
            user_id
        ),
        db.execute(
            """
            INSERT INTO token_history
                (token, id)
            VALUES
                ($1, $2)
            """,
            user_data["token"],
            user_id
        )
    )

    return ORJSONResponse(
        {
            "detail": "Successful.",
            "new_token": access_token
        }
    )
