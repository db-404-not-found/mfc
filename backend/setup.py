from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
from backend.views.deps import JinjaMarker
from backend.views.router import view_router

PROJECT_ROOT = Path("./backend").resolve()
print(PROJECT_ROOT)


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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
    app.include_router(view_router)
    app.exception_handler(HTTPException)(http_exception_handler)

    app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "static"), name="static")

    templates = Jinja2Templates(directory=PROJECT_ROOT / "templates")

    app.dependency_overrides.update(
        {
            SettingsMarker: lambda: settings,
            DatabaseEngineMarker: lambda: engine,
            DatabaseSessionMarker: lambda: session_factory,
            DatabaseHolderMarker: create_holder(session_factory=session_factory),
            JinjaMarker: lambda: templates,
        }
    )

    return app
