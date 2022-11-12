from __future__ import annotations

__all__ = ("get_db",)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asyncpg import Connection as PGConnection
    from fastapi import Request


def get_db(request: Request) -> PGConnection:
    return request.app.state.db
