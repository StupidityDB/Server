__all__ = ("generate_example",)

from typing import Any

from fastapi import status as http_status


def generate_example(
    example: Any, /, *, status: int = http_status.HTTP_200_OK, html: bool = False
) -> dict[int, dict[str, dict[str, dict[str, Any]]]]:
    return {
        status: {
            "description": "A users average stupidity and total vote count.",
            "content": {
                "text/html" if html else "application/json": {
                    "example": example
                }
            }
        }
    }
