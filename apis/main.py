"""Application entrypoint - runs the ASGI server."""

import uvicorn

from app import create_app

app = create_app()


def run() -> None:
    """Run the development server."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    run()
