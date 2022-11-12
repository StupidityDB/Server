__all__ = ("router",)

from typing import TYPE_CHECKING

from fastapi import APIRouter, Body, Depends
from fastapi.responses import ORJSONResponse
from fastapi_limiter.depends import RateLimiter

from ...annotations import UserId
from ...depends import get_db, oauth2

if TYPE_CHECKING:
    from fastapi_discord import User
    from asyncpg import Connection as PGConnection

router = APIRouter(
    prefix="/stupidity",
    tags=["stupidity"],
)


@router.get(
    "/",
    summary="Get a users stupidity.",
    description="Get a users stupidity.",
)
async def get_user_stupidity(
    *,
    db: PGConnection = Depends(get_db),
    user_id: int = UserId
) -> ORJSONResponse:
    ...


@router.put(
    "/",
    summary="Vote for a users stupidity.",
    description=(
        "Vote for a users stupidity. "
        "Returns the old stupidity rating if the user has already voted for this user."
    ),
    dependencies=[
        Depends(oauth2.requires_authentication),
        Depends(RateLimiter(times=5, minutes=1)),
    ]
)
async def vote_for_user_stupidity(
    db: PGConnection = Depends(get_db),
    user_id: int = UserId,
    rating: int = Body(
        description="The rating to rate the user.",
        ge=0,
        le=100
    ),
    user: User = Depends(oauth2.get_user())
) -> ORJSONResponse:
    ...
