import uvicorn
from fastapi import FastAPI, Depends, Body
from fastapi.responses import ORJSONResponse
from fastapi_discord import DiscordOAuthClient as DiscordOAuth2Client, User
from json5 import loads as decode_json5
from motor.motor_asyncio import AsyncIOMotorClient
from aioredis import from_url as redis_from_url
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from pathlib import Path


config = decode_json5((Path(__file__).parent / "config.json5").read_text())

db = AsyncIOMotorClient(config["MONGO_URI"])["StupidityDB"]

app = FastAPI(
    title="StupidityDB",
    description="A stupid database.",
    version="0.0.1",
    default_response_class=ORJSONResponse,
    docs_url=None,
    redoc_url="/docs",
)

oauth2 = DiscordOAuth2Client(
    client_id=config["CLIENT_ID"],
    client_secret=config["CLIENT_SECRET"],
    redirect_uri=config["REDIRECT_URI"],
)


@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis_from_url("redis://localhost", encoding="utf-8", decode_responses=True))
    await oauth2.init()


@app.get(
    "/users/{user_id}/stupidity",
    summary="Get a users stupidity.",
    description="Get a users stupidity.",
)
async def get_user_stupidity(user_id: int,) -> ORJSONResponse:
    average = await db.ratings.aggregate(
        [
            {"$match": {"rated": user_id}},
            {"$group": {"_id": None, "$avg": "$rating"}},
        ]
    )
    total_votes = await db.ratings.count_documents({"rated": user_id})
    return ORJSONResponse({"stupidity": average, "total_votes": total_votes})


@app.put(
    "/users/{user_id}/stupidity",
    summary="Vote for a users stupidity.",
    description=(
        "Vote for a users stupidity. "
        "Returns the old stupidity rating if the user has already voted for this user."
    ),
    dependencies=[
        Depends(oauth2.requires_authorization),
        Depends(oauth2.user),
        Depends(RateLimiter(times=5, minutes=1)),
    ]
)
async def vote_for_user_stupidity(
    user_id: int,
    rating: int = Body(description="The rating to rate the user.", ge=0, le=100),
    user: User = Depends(oauth2.user)
):
    existing = await db.ratings.find_one({"rater": user.id, "rated": user_id})

    if existing:
        await db.ratings.update_one({"_id": existing["_id"]}, {"$set": {"rating": rating}})
        return ORJSONResponse({"old": existing["rating"], "new": rating})

    await db.ratings.insert_one({"rater": user.id, "rated": user_id, "rating": rating})
    return ORJSONResponse({"old": None, "new": rating})


uvicorn.run(app, host="127.0.0.1")
