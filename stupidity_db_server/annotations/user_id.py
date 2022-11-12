__all__ = ("UserId",)

from fastapi import Path

UserId = Path(
    alias="user-id",
    title="The user's Discord ID",
    min_length=17,
    max_length=19,
    example=512640455834337290,
)
