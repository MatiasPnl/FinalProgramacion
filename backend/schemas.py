from pydantic import BaseModel
from typing import Optional

class UsuarioCreate(BaseModel):
    id: str
    nombre: str
    edad: int
    correo: str

class TareaCreate(BaseModel):
    id: str
    usuario_id: str
    tarea: str
    id_estado: int

class EstadoTareaCreate(BaseModel):
    id: int
    estado: str
