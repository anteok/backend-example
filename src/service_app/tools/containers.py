from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource, Provider
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


class MainContainer(DeclarativeContainer):
    """Dependency injection container."""

    config = Configuration(yaml_files=["src/config.yaml"])

    sql_engine: Provider[AsyncEngine] = Resource(
        create_async_engine,
        url=config.service_app.connections.postgres.url,
        pool_size=config.service_app.connections.postgres.max_connections,
        max_overflow=0,
    )
    # db_session = sessionmaker(sql_engine, expire_on_commit=False, class_=AsyncSession)
