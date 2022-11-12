__all__ = ("generate_example",)

from fastapi import status
from typing import Any


def generate_example(example: Any) -> dict[int, dict[str, dict[str, dict[str, Any]]]]:
    return {
        status.HTTP_200_OK: {
            "description": "A users average stupidity and total vote count.",
            "content": {
                "application/json": {
                    "example": example
                }
            }
        }
    }
