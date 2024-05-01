from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .. import init_app


def create_app():
    """Application configuration
    Args:
        config_name (Object): Object containing the application configuration

    Returns:
        Object: Instance of application
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        # Trailing slash causes CORS failures from these supported domains
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    init_app(app)

    return app
