from aiohttp import web
from aiohttp.web_routedef import RouteDef

from src.service_app.views.health import get_health


def get_routes() -> list[RouteDef]:
    return [
        web.get("/health", get_health),
    ]
