__all__ = ('user_id',)

from fastapi import HTTPException, Path


def user_id(
    user_id: int = Path(
        description="The user's Discord ID.",
        example=512640455834337290
    )
) -> int:
    if not 17 >= len(str(user_id)) <= 19:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )

    return user_id
