from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db, Base, engine
from backend.models import Usuario, Tarea, EstadoTarea
from backend.schemas import UsuarioCreate, TareaCreate, EstadoTareaCreate
from datetime import date

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Endpoints de usuarios
@app.get("/usuarios/")
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado"}

# Endpoints de tareas
@app.get("/tareas/")
def leer_tareas(usuario_id: str = None, db: Session = Depends(get_db)):
    if usuario_id:
        return db.query(Tarea).filter(Tarea.usuario_id == usuario_id, Tarea.id_estado != 2).all()
    return db.query(Tarea).filter(Tarea.id_estado != 2).all()

@app.post("/tareas/")
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    nueva_tarea = Tarea(**tarea.dict(), fecha=date.today())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@app.put("/usuarios/{usuario_id}")
def actualizar_usuario(usuario_id: str, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario_existente.nombre = usuario.nombre
    usuario_existente.edad = usuario.edad
    usuario_existente.correo = usuario.correo
    db.commit()
    return usuario_existente

@app.post("/tareas/")
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == tarea.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    nueva_tarea = Tarea(**tarea.dict(), fecha=date.today())
    db.add(nueva_tarea)
    db.commit()
    db.refresh(nueva_tarea)
    return nueva_tarea

@app.get("/tareas/{usuario_id}")
def tareas_por_usuario(usuario_id: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    tareas = db.query(Tarea).filter(Tarea.usuario_id == usuario_id, Tarea.id_estado != 2).all()
    return tareas

@app.get("/tareas/")
def leer_tareas(usuario_id: str = None, db: Session = Depends(get_db)):
    if usuario_id:
        return db.query(Tarea).filter(Tarea.usuario_id == usuario_id, Tarea.id_estado != 2).all()
    return db.query(Tarea).filter(Tarea.id_estado != 2).all()