__all__ = ("router",)

from asyncpg import Connection as PGConnection
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi_discord import User
from fastapi_limiter.depends import RateLimiter

from ....annotations import UserId
from ....depends import get_db, oauth2
from ....util import generate_example

router = APIRouter(
    tags=["Stupidity"]
)


@router.get(
    "/{user_id}/stupidity",
    summary="Get a users average stupidity.",
    description="This endpoint returns the average stupidity and total voted count of a user.",
    response_description="The users average stupidity and total voted count.",
    responses=generate_example(
        {
            "average_stupidity": 36.7,
            "total_votes": 356
        }
    )
)
async def get_user_stupidity(
    *,
    db: PGConnection = Depends(get_db),
    target_id: int = UserId
) -> ORJSONResponse:
    result = await db.fetch(
        "SELECT AVG(rating) AS average, COUNT(*) AS total FROM stupidity WHERE rated = $1",
        target_id
    )

    return ORJSONResponse(
        {
            "average_stupidity": result[0]["average"],
            "total_votes": result[0]["total"]
        }
    )


@router.put(
    "/{user_id}/stupidity",
    summary="Vote for a users stupidity.",
    description=(
        "This endpoint lets you vote for a users stupidity. It Returns the old stupidity "
        "rating if the user has already voted for this user. Or None if the user has not."
    ),
    response_description="The users old and new stupidity rating.",
    dependencies=[
        Depends(RateLimiter(times=5, minutes=1))
    ],
    status_code=status.HTTP_201_CREATED,
    responses=generate_example(
        {
            "old_rating": 69,
            "new_rating": 31
        },
        status=status.HTTP_201_CREATED
    )
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
        le=100
    )
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
            "old_rating": old_rating,
            "new_rating": rating
        }
    )


@router.delete(
    "/{user_id}/stupidity",
    summary="Remove a user stupidity vote.",
    description=(
        "This endpoint lets you remove a vote that you have sent to a user. "
        "It returns the old stupidity rating (Now of which is deleted.)."
    ),
    response_description=(
        "The users old stupidity rating. Will be None if the successfully_deleted "
        "key is False."
    ),
    dependencies=[
        Depends(oauth2.requires_authentication),
        Depends(RateLimiter(times=5, minutes=1)),
    ],
    responses=generate_example(
        {
            "successfully_deleted": True,
            "old_rating": 31
        }
    )
)
async def remove_user_stupidity_vote(
    *,
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
            "successfully_deleted": old_rating is not None,
            "old_rating": old_rating
        }
    )
