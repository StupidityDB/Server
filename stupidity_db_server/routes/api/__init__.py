__all__ = ("router",)

from fastapi import APIRouter

from . import users

router = APIRouter(
    prefix="/api"
)
router.include_router(users.router)
