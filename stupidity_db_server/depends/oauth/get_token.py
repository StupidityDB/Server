from __future__ import annotations

__all__ = ("get_token",)

from fastapi import Depends, Request

from .. import get
from ...ductape import StupidOAuthClient


def get_token(
    *,
    oauth: StupidOAuthClient = Depends(get.oauth),
    request: Request
) -> str:
    return oauth.get_token(request)
