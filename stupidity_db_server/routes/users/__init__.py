__all__ = ("router",)

from fastapi import APIRouter

from . import reviews, stupidity

router = APIRouter(
    prefix="/users/{user-id}",
    tags=["users"],
)
router.include_router(reviews.router)
router.include_router(stupidity.router)
