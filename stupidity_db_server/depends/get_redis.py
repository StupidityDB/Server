from __future__ import annotations

__all__ = ("get_redis",)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aioredis import Redis as RedisConnection
    from fastapi import Request


def get_redis(request: Request) -> RedisConnection:
    return request.app.state.redis
