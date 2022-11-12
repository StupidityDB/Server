__all__ = ("get_db",)

from asyncpg import Connection as PGConnection
from fastapi import Request


def get_db(request: Request) -> PGConnection:
    return request.app.db
