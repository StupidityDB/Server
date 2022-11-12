__all__ = ()

from uvicorn import run as run_app

from . import StupidAPI

run_app(StupidAPI())
