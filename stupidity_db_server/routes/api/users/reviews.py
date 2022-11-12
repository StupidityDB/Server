__all__ = ("router",)

from fastapi import APIRouter

router = APIRouter(
    prefix="/reviews/{review_id}",
    tags=["Reviews"]
)
