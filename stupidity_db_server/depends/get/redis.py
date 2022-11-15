from __future__ import annotations

__all__ = ("redis",)

from typing import TYPE_CHECKING

from fastapi import Depends

from .app import app as get_app

if TYPE_CHECKING:
    from aioredis import Redis as RedisConnection

    from ... import StupidAPI


def redis(*, app: StupidAPI = Depends(get_app)) -> RedisConnection:
    return app.redis
