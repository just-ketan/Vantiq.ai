from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.exceptions import (
    UploadException,
    AuthException,
)
from schemas.error import (
    ErrorEnvelope,
    ErrorResponse,
)


def build_error_response(
    status_code: int,
    exc,
):
    return JSONResponse(
        status_code=status_code,
        content=ErrorEnvelope(
            error=ErrorResponse(
                code=exc.error_code.value,
                message=exc.message,
            )
        ).model_dump(),
    )


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(UploadException)
    async def upload_exception_handler(
        request: Request,
        exc: UploadException,
    ):
        mapping = {
            "INVALID_FILE_TYPE": 400,
            "FILE_TOO_LARGE": 400,
            "UPLOAD_NOT_FOUND": 404,
        }

        return build_error_response(
            mapping.get(exc.error_code.value, 400),
            exc,
        )


    @app.exception_handler(AuthException)
    async def auth_exception_handler(
        request: Request,
        exc: AuthException,
    ):
        mapping = {
            "INVALID_CREDENTIALS": 401,
            "UNAUTHORIZED": 401,
        }

        return build_error_response(
            mapping.get(exc.error_code.value, 401),
            exc,
        )