__all__ = ()

from uvicorn import run as run_fastapi

from . import StupidAPI

app = StupidAPI()

run_fastapi(app, reload=True)
