from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

def registrar_manejadores(app):

    @app.exception_handler(StarletteHTTPException)
    async def manejar_error_http(
            request: Request,
            exc: StarletteHTTPException
    ):
        codigos = {
            400: "BAD_REQUEST",
            401: "UNAUTHORIZED",
            403: "FORBIDDEN",
            404: "NOT_FOUND",
            405: "METHOD_NOT_ALLOWED",
            409: "CONFLICT",
            503: "SERVICE_UNAVAILABLE"
        }

        return JSONResponse(
            status_code = exc.status_code,
            content={
                "error": codigos.get(exc.status_code, "HTTP_ERROR"),
                "message": str(exc.detail),
            },
            headers = exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def manejar_error_validacion(
            request: Request,
            exc: RequestValidationError
    ):
        return JSONResponse(
            status_code = 400,
            content = {
                "error": "VALIDATION_ERROR",
                "message": "Los datos enviados no cumplen con el contrato de la API"
            }
        )