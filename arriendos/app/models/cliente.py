from pydantic import BaseModel, EmailStr

class ClienteInput(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str | None = None

class Cliente(BaseModel):
    id: str
    nombre: str
    email: EmailStr
    telefono: str | None = None