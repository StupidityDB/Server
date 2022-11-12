__all__ = ("get_redis",)

from aioredis import Redis as RedisConnection
from fastapi import Request


def get_redis(request: Request) -> RedisConnection:
    return request.app.state.redis
