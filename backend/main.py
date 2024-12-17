from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db, Base, engine
from backend.models import Usuario, Tarea
from backend.schemas import UsuarioCreate, TareaCreate
from datetime import date


# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ----------------------- Endpoints de Usuarios -----------------------

@app.get("/usuarios/")
def leer_usuarios(db: Session = Depends(get_db)):
    """Obtener todos los usuarios."""
    return db.query(Usuario).all()


@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: str, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Actualizar información de un usuario."""
    usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario_existente.nombre = usuario.nombre
    usuario_existente.edad = usuario.edad
    usuario_existente.correo = usuario.correo
    db.commit()
    db.refresh(usuario_existente)
    return {"message": "Usuario actualizado correctamente", "usuario": usuario_existente}


@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """Eliminar un usuario por su ID."""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}



# ----------------------- Endpoints de Tareas -----------------------

@app.get("/tareas/")
def leer_tareas(usuario_id: str = None, db: Session = Depends(get_db)):
    """
    Obtener todas las tareas pendientes (id_estado != 2).
    Si se proporciona un usuario_id, filtra las tareas pendientes de ese usuario.
    """
    query = db.query(Tarea).filter(Tarea.id_estado != 2)
    if usuario_id:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        query = query.filter(Tarea.usuario_id == usuario_id)
    return query.all()


@app.get("/tareas/{usuario_id}")
def tareas_por_usuario(usuario_id: str, db: Session = Depends(get_db)):
    """
    Obtener tareas pendientes de un usuario específico.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    tareas = db.query(Tarea).filter(Tarea.usuario_id == usuario_id, Tarea.id_estado != 2).all()
    return tareas


@app.post("/tareas/")
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == tarea.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    nueva_tarea = Tarea(
        id=tarea.id,
        usuario_id=tarea.usuario_id,
        tarea=tarea.tarea,
        fecha=date.today(),
        id_estado=tarea.id_estado
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea


@app.put("/tareas/{tarea_id}/completar")
def completar_tarea(tarea_id: str, db: Session = Depends(get_db)):
    """
    Completar una tarea (actualizar el id_estado a 2).
    """
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    tarea.id_estado = 2  # Estado 'completada'
    db.commit()
    db.refresh(tarea)
    return {"message": "Tarea completada", "tarea": tarea}


@app.get("/tareas/todas/{usuario_id}")
def obtener_todas_tareas(usuario_id: str, db: Session = Depends(get_db)):
    """
    Obtener todas las tareas (pendientes y completadas) de un usuario.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    tareas = db.query(Tarea).filter(Tarea.usuario_id == usuario_id).all()
    return tareas

@app.get("/tareas/completadas/{usuario_id}")
def obtener_tareas_completadas(usuario_id: str, db: Session = Depends(get_db)):
    """
    Obtener todas las tareas completadas (id_estado = 2) de un usuario específico.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    tareas = db.query(Tarea).filter(Tarea.usuario_id == usuario_id, Tarea.id_estado == 2).all()
    return tareas

@app.post("/tareas/{usuario_id}")
def crear_tarea_usuario(usuario_id: str, tarea: TareaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva tarea para un usuario específico.
    """
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    nueva_tarea = Tarea(
        id=f"tarea-{tarea.tarea.replace(' ', '_')}",
        usuario_id=usuario_id,
        tarea=tarea.tarea,
        id_estado=1,  # Estado pendiente
        fecha=date.today()
    )
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: str, db: Session = Depends(get_db)):
    """
    Eliminar una tarea por su ID.
    """
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(tarea)
    db.commit()
    return {"message": "Tarea eliminada correctamente"}