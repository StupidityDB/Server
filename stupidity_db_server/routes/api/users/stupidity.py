from __future__ import annotations

__all__ = ("router",)

from typing import TYPE_CHECKING

from asyncpg import Connection as PostgresConnection
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from fastapi_limiter.depends import RateLimiter

from ....depends import get, oauth, params
from ....utils import generate_example, generate_examples

if TYPE_CHECKING:
    from asyncpg import Record

router = APIRouter(
    tags=["Stupidity"]
)


@router.get(
    "/stupidity",
    summary="Get a users average stupidity.",
    description="This endpoint returns the average stupidity and total voted count of a user.",
    response_description="The users average stupidity and total received vote count.",
    responses=generate_examples(
        {
            status.HTTP_200_OK: {
                "detail": "User found.",
                "average_stupidity": 36.7,
                "total_votes": 356
            },
            status.HTTP_404_NOT_FOUND: {
                "detail": "User not found."
            }
        }
    )
)
async def get_user_stupidity(
    *,
    db: PostgresConnection = Depends(get.db),
    target_id: int = Depends(params.user_id),
) -> ORJSONResponse:
    result: Record = await db.fetchrow(
        """
        SELECT
            AVG(rating) AS average,
            COUNT(*) AS total
        FROM
            stupidity_table
        WHERE
            rated = $1
        """,
        target_id
    )

    total_votes = result["total"]

    if not total_votes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return ORJSONResponse(
        {
            "detail": "User found.",
            "average_stupidity": round(result["average"], 1),
            "total_votes": total_votes
        }
    )


@router.put(
    "/stupidity",
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
            "detail": "Successfully voted for the user's stupidity.",
            "old_rating": 69,
            "new_rating": 31
        },
        status_code=status.HTTP_201_CREATED
    )
)
async def vote_for_user_stupidity(
    *,
    db: PostgresConnection = Depends(get.db),
    user: oauth.DiscordUser = Depends(oauth.get_user),
    target_id: int = Depends(params.user_id),
    rating: int = Body(
        description="The rating to rate the user's stupidity.",
        example=69,
        embed=True,
        ge=0,
        le=100
    )
) -> ORJSONResponse:
    old_rating: int | None = await db.fetchval(
        """
        SELECT
            rating
        FROM
            stupidity_table
        WHERE
            rater = $1 AND
            rated = $2
        """,
        user.id,
        target_id
    )

    await db.execute(
        """
        INSERT INTO stupidity_table
            (rated, rater, rating)
        VALUES
            ($1, $2, $3)
        ON CONFLICT
            (rated, rater)
        DO UPDATE SET
            rating = $3
        """,
        target_id,
        user.id,
        rating
    )

    return ORJSONResponse(
        {
            "detail": "Successfully voted for the user's stupidity.",
            "old_rating": old_rating,
            "new_rating": rating
        }
    )


@router.delete(
    "/stupidity",
    summary="Remove a user stupidity vote.",
    description=(
        "This endpoint lets you remove a vote that you have sent to a user. "
        "It returns the old stupidity rating (Now of which is deleted.)."
    ),
    response_description="The users old stupidity rating.",
    dependencies=[
        Depends(RateLimiter(times=5, minutes=1))
    ],
    responses=generate_examples(
        {
            status.HTTP_200_OK: {
                "detail": "Successfully removed vote for user's stupidity.",
                "old_rating": 31
            },
            status.HTTP_404_NOT_FOUND: {
                "detail": "User not found."
            }
        }
    )
)
async def remove_user_stupidity_vote(
    *,
    db: PostgresConnection = Depends(get.db),
    user: oauth.DiscordUser = Depends(oauth.get_user),
    target_id: int = Depends(params.user_id)
) -> ORJSONResponse:
    old_rating: int = await db.fetchval(
        """
        DELETE FROM
            stupidity_table
        WHERE
            rater = $1 AND
            rated = $2
        RETURNING
            rating
        """,
        user.id,
        target_id
    )

    if not old_rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vote not found."
        )

    return ORJSONResponse(
        {
            "detail": "Successfully removed vote for user's stupidity.",
            "old_rating": old_rating
        }
    )
