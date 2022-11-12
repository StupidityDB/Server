__all__ = ("UserId",)

from fastapi import Path

UserId = Path(
    alias="user-id",
    description="The user's Discord ID.",
    example=512640455834337290
)
