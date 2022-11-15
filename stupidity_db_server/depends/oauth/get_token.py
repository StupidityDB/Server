from __future__ import annotations

__all__ = ("get_token",)

from typing import TYPE_CHECKING

from fastapi import Depends

from .. import get

if TYPE_CHECKING:
    from fastapi import Request

    from ...ductape import StupidOAuthClient


def get_token(
    *,
    oauth: StupidOAuthClient = Depends(get.oauth),
    request: Request
) -> str:
    return oauth.get_token(request)
