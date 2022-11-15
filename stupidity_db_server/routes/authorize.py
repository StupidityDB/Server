__all__ = ("router",)

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

from asyncpg import Connection as PGConnection
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import HTMLResponse, ORJSONResponse, RedirectResponse
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client
from fastapi_discord.exceptions import InvalidToken

from ..depends import get_db, oauth2
from ..util import generate_examples

router = APIRouter(
    prefix="/authorize",
    tags=["Authorization"]
)


@router.get(
    "/",
    summary="Authorize with Discord.",
    description="This endpoint will redirect you to Discord's OAuth2 authorization page.",
    response_description="Redirect to the Discord OAuth2 authorization page.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse
)
async def authorize(
    *,
    oauth2_: DiscordOAuth2Client = Depends(oauth2.get_oauth2)
) -> RedirectResponse:
    return RedirectResponse(oauth2_.oauth_login_url)


@router.get(
    "/callback",
    summary="Callback for Discord OAuth2.",
    description="You will be redirected here after authorizing with Discord.",
    response_description="HTML page with information about the authorization.",
    response_class=HTMLResponse,
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
    db: PGConnection = Depends(get_db),
    oauth2_: DiscordOAuth2Client = Depends(oauth2.get_oauth2),
    code: str | None = Query(
        default=None,
        description="The authorization code returned by Discord.",
        example="Waf3Tvx8kdos5hta3gcJ8GndJSoBqI"
    )
) -> ORJSONResponse:
    if code is None:
        return ORJSONResponse(
            {
                "detail": "No authorization code was provided."
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        token, refresh_token = await oauth2_.get_access_token(code)
    except InvalidToken:
        return ORJSONResponse(
            {
                "detail": "The provided authorization code is invalid."
            },
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    user_raw = await oauth2_.request("/users/@me", token=token)
    token_expires = DateTime.now(TimeZone.utc) + TimeDelta(seconds=user_raw.pop("expires_in"))
    user = oauth2.DiscordUser(**user_raw)

    await db.execute(
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
        token,
        token_expires,
        refresh_token
    )

    return ORJSONResponse(
        {
            "detail": "Successful.",
            "token": token
        }
    )
