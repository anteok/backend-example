from http import HTTPStatus

from tests.base import TestApp


class TestHealth(TestApp):
    async def test_route(self, client):
        response = await client.get("health")
        assert response.status == HTTPStatus.OK
