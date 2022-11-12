__all__ = ("StupidAPI",)

from pathlib import Path

from aioredis import Redis as RedisConnection
from asyncpg import Connection as PGConnection, connect as connect_to_postgres
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, Unauthorized
from fastapi_discord.exceptions import ClientSessionNotInitialized
from fastapi_limiter import FastAPILimiter
from json5 import loads as decode_json5

from .routes import router as api_router

config = decode_json5((Path(__file__).parent / "config.json5").read_text())


class StupidAPI(FastAPI):
    db: PGConnection = None
    redis = RedisConnection.from_url("redis://localhost:6379", decode_responses=True)
    oauth2 = DiscordOAuth2Client(
        client_id=config["CLIENT_ID"],
        client_secret=config["CLIENT_SECRET"],
        redirect_uri=config["REDIRECT_URI"]
    )

    def __init__(self) -> None:
        super().__init__(
            title="StupidityDB",
            description="A stupid(ity) database.",
            version="0.0.1",
            default_response_class=ORJSONResponse,
            redoc_url=None
        )
        self.add_event_handler("startup", self.on_start)
        self.include_router(api_router)

        self.exception_handler(Unauthorized)(self.handle_unauthorized)
        self.exception_handler(ClientSessionNotInitialized)(self.handle_session_not_initialized)

    async def on_start(self) -> None:
        self.db = await connect_to_postgres(
            user="stupidity_db_user",
            password="stupidity_db_password",
            database="stupidity_db",
            host="127.0.0.1"
        )
        await FastAPILimiter.init(self.redis)
        await self.oauth2.init()

    @staticmethod
    async def handle_unauthorized(_: Request, __: Unauthorized, /) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=401,
            content={
                "detail": "You're unauthorized."
            }
        )

    @staticmethod
    async def handle_session_not_initialized(
        _: Request,
        __: ClientSessionNotInitialized,
        /
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error."
            }
        )
