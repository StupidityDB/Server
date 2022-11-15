from __future__ import annotations

__all__ = ("app",)

from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    from ... import StupidAPI


def app(*, request: Request) -> StupidAPI:
    return request.app
