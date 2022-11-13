__all__ = ("router",)

from inspect import cleandoc

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client

from ..depends import oauth2
from ..util import generate_example

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
    responses=generate_example(
        cleandoc(
            """
            <h1>Success!</h1>
            <p>You are have authorized StupidityDB successfully.</p>
            """
        ),
        html=True
    )
)
async def authorize_success(
    *,
    oauth2_: DiscordOAuth2Client = Depends(oauth2.get_oauth2),
    code: str | None = Query(
        default=None,
        description="The authorization code returned by Discord.",
        example="Waf3Tvx8kdos5hta3gcJ8GndJSoBqI"
    )
) -> HTMLResponse:
    if code is None:
        return HTMLResponse(
            content=cleandoc(
                """
                <h1>Error!</h1>
                <p>You did not provide an authorization code.</p>
                """
            ),
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    token, refresh_token = await oauth2_.get_access_token(code)
    # Now what?
    return HTMLResponse(
        cleandoc(
            """
            <h1>Success!</h1>
            <p>You are have authorized StupidityDB successfully.</p>
            """
        )
    )
