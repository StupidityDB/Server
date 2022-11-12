__all__ = ()

from uvicorn import run as run_app

from . import StupidAPI

app = StupidAPI()

run_app(app, reload=True)
