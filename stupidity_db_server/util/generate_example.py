__all__ = ("generate_example",)

from typing import Any

from fastapi import status as http_status


def generate_example(
    example: Any,
    /,
    *,
    status: int = http_status.HTTP_200_OK,
    content_type: str = "application/json"
) -> dict[int, dict[str, dict[str, dict[str, Any]]]]:
    return {
        status: {
            "content": {
                content_type: {
                    "example": example
                }
            }
        }
    }
