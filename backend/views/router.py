from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.api.deps import SettingsMarker
from backend.config import Settings
from backend.views.deps import JinjaMarker

view_router = APIRouter(include_in_schema=False)


@view_router.get("/", response_class=HTMLResponse)
async def home_view(
    request: Request,
    templates: Jinja2Templates = Depends(JinjaMarker),
    settings: Settings = Depends(SettingsMarker),
) -> Response:
    return templates.TemplateResponse(
        "index.html",
        context={
            "request": request,
            "title": f"{settings.PROJECT_NAME} - {settings.DESCRIPTION}",
        },
    )
