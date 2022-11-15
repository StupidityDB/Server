__all__ = ("DiscordUser",)

from pydantic import BaseModel


class DiscordUser(BaseModel):
    id: int
    username: str
    discriminator: int
    avatar_url: str
