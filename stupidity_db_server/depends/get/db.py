__all__ = ("db",)

from asyncpg import Connection as PostgresConnection
from fastapi import Request


def db(*, request: Request) -> PostgresConnection:
    return request.app.db
