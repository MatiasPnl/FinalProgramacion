from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from backend.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=False)
    correo = Column(String(100), nullable=False)

    # Relación one-to-many
    tareas = relationship("Tarea", back_populates="usuario", cascade="all, delete-orphan")

class EstadoTarea(Base):
    __tablename__ = "estados_tareas"
    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50), nullable=False)

class Tarea(Base):
    __tablename__ = "tareas"
    
    # Columnas
    id = Column(String, primary_key=True, index=True)
    usuario_id = Column(String, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    tarea = Column(String(100), nullable=False)
    fecha = Column(Date, nullable=False)
    id_estado = Column(Integer, ForeignKey("estados_tareas.id"), nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="tareas")  # Sin delete-orphan
    estado_tarea = relationship("EstadoTarea", lazy="joined")
