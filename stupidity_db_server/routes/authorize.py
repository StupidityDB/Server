__all__ = ("router",)

from inspect import cleandoc

from fastapi import APIRouter, Depends, status
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
    "/success",
    summary="Success page after linking your Discord account.",
    description="This endpoint says that you have successfully linked your Discord account.",
    response_description="Success page after linking your Discord account.",
    response_class=HTMLResponse,
    responses=generate_example(
        cleandoc(
            """
            <h1>Success!</h1>
            <p>You are have authorized StupidityDB successsfully.</p>
            """
        ),
        html=True
    )
)
async def authorize_success() -> HTMLResponse:
    return HTMLResponse(
        cleandoc(
            """
            <h1>Success!</h1>
            <p>You are have authorized StupidityDB successsfully.</p>
            """
        )
    )
