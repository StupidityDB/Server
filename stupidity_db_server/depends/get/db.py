__all__ = ("db",)

from typing import TYPE_CHECKING

from fastapi import Depends

from .app import app as get_app

if TYPE_CHECKING:
    from asyncpg import Connection as PostgresConnection

    from ... import StupidAPI


def db(*, app: StupidAPI = Depends(get_app)) -> PostgresConnection:
    return app.db
