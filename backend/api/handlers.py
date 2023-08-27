import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from backend.api.schemas import StatusResponseSchema

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=StatusResponseSchema(
            message=exc.detail,
        ).model_dump(),
    )
