from aiohttp import web
from dependency_injector.containers import Container

from src.service_app.routes import get_routes


def create_app() -> web.Application:
    app = web.Application()
    app.container = Container()
    app.add_routes(get_routes())
    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
