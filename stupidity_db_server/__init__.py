__all__ = ("StupidAPI",)

from pathlib import Path
from typing import TYPE_CHECKING

from aioredis import Redis as RedisConnection
from asyncpg import Connection as PostgresConnection, connect as connect_to_postgres
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_discord import DiscordOAuthClient, Unauthorized
from fastapi_limiter import FastAPILimiter
from json5 import loads as decode_json5

from .routes import router

if TYPE_CHECKING:
    from fastapi import Request


class StupidAPI(FastAPI):
    db: PostgresConnection
    redis: RedisConnection
    oauth: DiscordOAuthClient

    def __init__(self) -> None:
        super().__init__(
            title="StupidityDB",
            description="A stupid(ity) database.",
            version="0.0.1",
            default_response_class=ORJSONResponse,
            redoc_url=None,
            on_startup=(
                self.on_start,
            ),
            on_shutdown=(
                self.db.close,
                self.redis.close
            ),
            exception_handlers={
                Unauthorized: self.handle_unauthorized
            }
        )

        self.include_router(router)

    async def on_start(self) -> None:
        config = decode_json5(
            (Path(__file__).parent / "config.json5").read_text()
        )

        self.db = await connect_to_postgres(
            user="stupidity_db_user",
            password="stupidity_db_password",
            database="stupidity_db",
            host="127.0.0.1"
        )

        self.redis = RedisConnection.from_url(
            "redis://localhost:6379",
            decode_responses=True
        )

        self.oauth = DiscordOAuthClient(
            client_id=config["CLIENT_ID"],
            client_secret=config["CLIENT_SECRET"],
            redirect_uri=config["REDIRECT_URI"]
        )
        await self.oauth.init()

        await FastAPILimiter.init(self.redis)

    @staticmethod
    async def handle_unauthorized(_: Request, __: Unauthorized, /) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=401,
            content={
                "detail": "You're unauthorized."
            }
        )
