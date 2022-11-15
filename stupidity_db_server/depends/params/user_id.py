__all__ = ("user_id",)

from math import log10

from fastapi import HTTPException, Path


def user_id(
    target_id: int = Path(
        alias="user_id",
        description="The user's Discord ID.",
        example=512640455834337290
    )
) -> int:
    if not 19 >= int(log10(target_id) + 1) >= 17:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID."
        )

    return target_id
