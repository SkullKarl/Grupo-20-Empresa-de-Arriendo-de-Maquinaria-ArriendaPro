import os
import secrets

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(
    name = "X-API-Key",
    scheme_name = "ApiKeyAuth",
    auto_error = False,
)

def verificar_api_key(
        api_key: str | None = Security(api_key_header)
):
    clave_esperada = os.getenv("ARRIENDOS_API_KEY")

    if not clave_esperada:
        raise HTTPException(
            status_code = 503,
            detail = "La autenticación del servicio no está configurada"
        )

    if api_key is None or not secrets.compare_digest(
        api_key,
        clave_esperada,
    ):
        raise HTTPException(
            status_code = 401,
            detail = "API Key ausente o inválida",
            headers = {"WWW-Authenticate": "APIKey"},
        )