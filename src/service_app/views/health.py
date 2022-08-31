from aiohttp.web_request import Request
from aiohttp.web_response import Response


async def get_health(_: Request) -> Response:
    return Response()
