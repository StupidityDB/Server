__all__ = ("oauth",)

from typing import TYPE_CHECKING

from fastapi import Depends

from .app import app as get_app

if TYPE_CHECKING:
    from ...ductape import StupidOAuthClient

    from ... import StupidAPI


def db(*, app: StupidAPI = Depends(get_app)) -> StupidOAuthClient:
    return app.oauth
