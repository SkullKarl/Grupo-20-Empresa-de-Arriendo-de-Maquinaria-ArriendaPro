from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

class ArriendoInput(BaseModel):
    cliente_id: UUID
    equipo_id: str
    cantidad: int = Field(ge=1)
    fecha_inicio: date
    fecha_fin: date

class Arriendo(ArriendoInput):
    id: UUID
    estado: Literal["activo", "devuelto"]