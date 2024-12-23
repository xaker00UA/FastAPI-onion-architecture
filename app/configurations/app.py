from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from .config import settings
from .server import Server


def create_app():
    app = FastAPI(
        debug=settings.debug,
        title=settings.title,
        description=settings.description,
        version=settings.version,
        default_response_class=ORJSONResponse,
    )
    app = Server(app).get_app()

    return app
