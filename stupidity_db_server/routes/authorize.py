__all__ = ("router",)

from fastapi import APIRouter, Depends, status
from inspect import cleandoc
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client

from ..depends import oauth2
from ..util import generate_example

router = APIRouter(
    prefix="/authorize",
    tags=["Authorize"],
)


@router.get(
    "/",
    summary="Link your Discord account.",
    description="Link your Discord account.",
    response_description="Redirect to the Discord OAuth2 authorization page.",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=RedirectResponse,
)
async def authorize(
    *,
    oauth2_: DiscordOAuth2Client = Depends(oauth2.get_oauth2),
) -> RedirectResponse:
    return RedirectResponse(oauth2_.oauth_login_url)


@router.get(
    "/success",
    summary="Success page after linking your Discord account.",
    description="Success page after linking your Discord account.",
    response_description="The success page after linking your Discord account.",
    response_class=HTMLResponse,
    responses=generate_example(
        cleandoc(
            """
            <h1>Success!</h1>
            <p>You are now authorized.</p>
            """
        )
    ),
)
async def authorize_success() -> HTMLResponse:
    return HTMLResponse(
        cleandoc(
            """
            <h1>Success!</h1>
            <p>You are now authorized.</p>
            """
        )
    )
