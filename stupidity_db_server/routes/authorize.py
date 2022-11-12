__all__ = ("router",)

from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client
from ..depends import oauth2

router = APIRouter(
    prefix="/authorize",
    tags=["authorize"],
)


@router.get(
    "/",
    summary="Link your Discord account.",
    description="Link your Discord account.",
    status_code=status.HTTP_302_FOUND
)
async def authorize(
    *,
    oauth2_: DiscordOAuth2Client = Depends(oauth2.get_oauth2)
) -> RedirectResponse:
    return RedirectResponse(oauth2_.oauth_login_url)


@router.get(
    "/success",
    summary="Success page after linking your Discord account.",
    description="Success page after linking your Discord account."
)
async def authorize_success() -> HTMLResponse:
    return HTMLResponse(
        "<h1>Success!</h1>"
        "<p>You can now use the API.</p>"
    )
