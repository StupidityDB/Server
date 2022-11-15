__all__ = ()

from uvicorn import run as run_app

from . import StupidAPI


def main() -> None:
    run_app(StupidAPI())
