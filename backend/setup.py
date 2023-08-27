from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine

from backend.api.deps import (
    DatabaseEngineMarker,
    DatabaseHolderMarker,
    DatabaseSessionMarker,
    SettingsMarker,
)
from backend.api.handlers import http_exception_handler
from backend.api.router import api_router
from backend.config import Settings
from backend.db.engine import (
    build_db_connection_uri,
    create_engine,
    create_holder,
    create_session_factory,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield

    engine: AsyncEngine = app.dependency_overrides[DatabaseEngineMarker]()
    await engine.dispose()


def setup_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        lifespan=lifespan,
    )

    engine = create_engine(
        connection_uri=build_db_connection_uri(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
        )
    )

    session_factory = create_session_factory(engine=engine)

    app.include_router(api_router)
    app.exception_handler(HTTPException)(http_exception_handler)

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseSessionMarker: lambda: session_factory,
            DatabaseHolderMarker: create_holder(session_factory=session_factory),
        }
    )

    return app
