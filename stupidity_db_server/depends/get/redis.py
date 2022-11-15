from __future__ import annotations

__all__ = ("redis",)

from typing import Any, TYPE_CHECKING

from fastapi import Depends

from .app import app as get_app

if TYPE_CHECKING:
    from aioredis import Redis as RedisConnection


def redis(*, app: Any = Depends(get_app)) -> RedisConnection:
    return app.redis
