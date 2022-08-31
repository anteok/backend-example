import pytest

from src.service_app.service import create_app


@pytest.mark.asyncio
class TestApp:
    @pytest.fixture
    def app(self):
        app = create_app()
        yield app

    @pytest.fixture
    def client(self, app, aiohttp_client, loop):
        return loop.run_until_complete(aiohttp_client(app))
