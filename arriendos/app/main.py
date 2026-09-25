from fastapi import FastAPI, Depends

from app.errors import registrar_manejadores
from app.security import verificar_api_key

from app.routes.clientes import router as clientes_router
from app.routes.arriendos import router as arriendos_router

app = FastAPI(
    title = "ArriendaPro",
    version = "1.0.0",
    description = "API REST para el sistema de arriendos"
)

registrar_manejadores(app)

app.include_router(
    clientes_router,
    dependencies = [Depends(verificar_api_key)],
)

app.include_router(
    arriendos_router,
    dependencies = [Depends(verificar_api_key)]
)