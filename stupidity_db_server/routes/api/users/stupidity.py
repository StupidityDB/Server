__all__ = ("router",)

from asyncpg import Connection as PGConnection
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi_discord import User
from fastapi_limiter.depends import RateLimiter

from ....annotations import UserId
from ....util import generate_example
from ....depends import get_db, oauth2

router = APIRouter(
    prefix="/stupidity",
    tags=["Stupidity"],
)


@router.get(
    "/",
    summary="Get a users average stupidity.",
    description="Get a users average stupidity. Also returns the total vote count.",
    response_description="The users average stupidity and total vote count.",
    responses=generate_example(
        {
            "average-stupidity": 36.7,
            "total-votes": 356,
        }
    ),
)
async def get_user_stupidity(
    *,
    db: PGConnection = Depends(get_db),
    target_id: int = UserId
) -> ORJSONResponse:
    average_stupidity, total_votes = await db.fetch(
        "SELECT AVG(rating) AS average, COUNT(*) AS count FROM stupidity WHERE rated = $1",
        target_id
    )

    return ORJSONResponse(
        {
            "average-stupidity": average_stupidity,
            "total-votes": total_votes
        }
    )


@router.put(
    "/",
    summary="Vote for a users stupidity.",
    description=(
        "Vote for a users stupidity. "
        "Returns the old stupidity rating if the user has already voted for this user."
    ),
    response_description="The users old and new stupidity rating.",
    dependencies=[
        Depends(oauth2.requires_authentication),
        Depends(RateLimiter(times=5, minutes=1)),
    ],
    status_code=status.HTTP_201_CREATED,
    responses=generate_example(
        {
            "old-rating": 69,
            "new-rating": 31,
        }
    ),
)
async def vote_for_user_stupidity(
    *,
    db: PGConnection = Depends(get_db),
    user: User = Depends(oauth2.get_user),
    target_id: int = UserId,
    rating: int = Body(
        description="The rating to rate the user's stupidity.",
        example=69,
        embed=True,
        ge=0,
        le=100,
    ),
) -> ORJSONResponse:
    old_rating = await db.fetchval(
        "SELECT rating FROM stupidity WHERE rater = $1 AND rated = $2",
        user.id,
        target_id
    )

    await db.execute(
        """
        INSERT INTO stupidity (rated, rater, rating) VALUES ($1, $2, $3)
        ON CONFLICT (rated, rater) DO UPDATE 
            SET rating = $3
        """,
        target_id,
        user.id,
        rating
    )

    return ORJSONResponse(
        {
            "old-rating": old_rating,
            "new-rating": rating,
        }
    )


@router.delete(
    "/",
    summary="Remove a users stupidity vote.",
    description="Remove a vote to a users stupidity. Returns the old stupidity rating (Now gone.).",
    response_description=(
        "The users old stupidity rating. Will be none if the successfully-deleted "
        "key is False."
    ),
    dependencies=[
        Depends(oauth2.requires_authentication),
        Depends(RateLimiter(times=5, minutes=1)),
    ],
    responses=generate_example(
        {
            "successfully-deleted": True,
            "old-rating": 31,
        }
    )
)
async def remove_user_stupidity_vote(
    db: PGConnection = Depends(get_db),
    user: User = Depends(oauth2.get_user),
    target_id: int = UserId,
) -> ORJSONResponse:
    old_rating = await db.execute(
        "DELETE FROM stupidity WHERE rater = $1 AND rated = $2 RETURNING rating",
        user.id,
        target_id
    )

    return ORJSONResponse(
        {
            "successfully-deleted": old_rating is not None,
            "old-rating": old_rating,
        }
    )
