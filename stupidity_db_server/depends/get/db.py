from __future__ import annotations

__all__ = ("db",)

from typing import Any, TYPE_CHECKING

from fastapi import Depends

from .app import app as get_app

if TYPE_CHECKING:
    from asyncpg import Connection as PostgresConnection


def db(*, app: Any = Depends(get_app)) -> PostgresConnection:
    return app.db
