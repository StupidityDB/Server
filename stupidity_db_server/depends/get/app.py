__all__ = ("app",)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import Request
    from ... import StupidAPI


def app(*, request: Request) -> StupidAPI:
    return request.app
