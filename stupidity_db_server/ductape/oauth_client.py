__all__ = ("StupidOAuthClient",)

from typing import TypedDict

from fastapi_discord import DiscordOAuthClient
from fastapi_discord.exceptions import InvalidToken


class TokenResponse(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


def get_tokens(response: TokenResponse) -> tuple[str, str]:
    access_token, refresh_token = response.get("access_token"), response.get("refresh_token")

    if not any((access_token, refresh_token)):
        raise InvalidToken("Tokens cannot be empty.")

    return access_token, refresh_token


class StupidOAuthClient(DiscordOAuthClient):
    async def get_access_token(self, code: str) -> tuple[str, str, int]:
        response = await self.get_token_response(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            }
        )
        access_token, refresh_token = get_tokens(response)
        return access_token, refresh_token, response["expires_in"]

    async def refresh_access_token(self, refresh_token: str) -> tuple[str, str, int]:
        response = await self.get_token_response(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }
        )
        access_token, refresh_token = get_tokens(response)
        return access_token, refresh_token, response["expires_in"]
