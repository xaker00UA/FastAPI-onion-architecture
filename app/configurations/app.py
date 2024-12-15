from fastapi import FastAPI
from .config import settings
from .server import Server


def create_app():
    app = FastAPI(
        debug=settings.debug,
        title=settings.title,
        description=settings.description,
        version=settings.version,
    )
    app = Server(app).get_app()

    return app
