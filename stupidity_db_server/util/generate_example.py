__all__ = ("generate_example",)

from fastapi import status


def generate_example(example: dict) -> dict:
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
