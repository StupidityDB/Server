__all__ = ("router",)

from fastapi import APIRouter

from . import api, authorize

router = APIRouter()
router.include_router(authorize.router)
router.include_router(api.router)
