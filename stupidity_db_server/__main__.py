__all__ = ()

from uvicorn import run as run_app

from . import StupidAPI


def __main__() -> None:
    run_app(StupidAPI())
