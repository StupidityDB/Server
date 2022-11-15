__all__ = ("redis",)

from aioredis import Redis as RedisConnection
from fastapi import Request


def redis(*, request: Request) -> RedisConnection:
    return request.app.redis
