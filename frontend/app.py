from flask import Flask, render_template, request, redirect, url_for
import requests
import json

app = Flask(__name__)
BASE_API_URL = "http://127.0.0.1:8000"

@app.route("/")
def index():
    try:
        # Obtener solo la lista de usuarios
        usuarios = requests.get(f"{BASE_API_URL}/usuarios/").json()
    except Exception as e:
        usuarios = []
        print("Error al obtener usuarios:", e)
    
    # No enviar tareas si no se ha seleccionado un usuario
    return render_template(
        "index.html",
        usuarios=usuarios,
        tareas=[],  # No mostrar tareas hasta seleccionar un usuario
        usuario_seleccionado=None
    )

@app.route("/asignar_tarea", methods=["POST"])
def asignar_tarea():
    tarea = {
        "id": f"tarea-{request.form['tarea'].replace(' ', '_')}",
        "usuario_id": request.form["usuario_id"],
        "tarea": request.form["tarea"],
        "id_estado": 1
    }
    print("Tarea enviada:", json.dumps(tarea, indent=4))
    try:
        response = requests.post(f"{BASE_API_URL}/tareas/", json=tarea)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error al asignar tarea:", e)
    return redirect(url_for("index"))


@app.route("/tareas_usuario", methods=["GET"])
def tareas_usuario():
    usuario_id = request.args.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("index"))  # Redirigir si no se selecciona usuario
    
    try:
        usuarios = requests.get(f"{BASE_API_URL}/usuarios/").json()
        tareas = requests.get(f"{BASE_API_URL}/tareas/{usuario_id}").json()
        usuario_seleccionado = next((u for u in usuarios if str(u["id"]) == usuario_id), None)
    except Exception as e:
        print("Error al obtener tareas:", e)
        tareas, usuarios, usuario_seleccionado = [], [], None

    return render_template("index.html", usuarios=usuarios, tareas=tareas, usuario_seleccionado=usuario_seleccionado)

@app.route("/completar_tarea", methods=["POST"])
def completar_tarea():
    tarea_id = request.form["tarea_id"]
    requests.put(f"{BASE_API_URL}/tareas/{tarea_id}/completar")
    return redirect(request.referrer)

@app.route("/tareas_completadas/<usuario_id>", methods=["GET"])
def tareas_completadas(usuario_id):
    tareas = requests.get(f"{BASE_API_URL}/tareas/completadas/{usuario_id}").json()
    return tareas

@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    """
    Agregar un nuevo usuario enviando la solicitud a FastAPI (/usuarios/).
    """
    usuario = {
        "id": request.form["id"],
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"]),
        "correo": request.form["correo"]
    }
    try:
        response = requests.post(f"{BASE_API_URL}/usuarios/", json=usuario)
        response.raise_for_status()  # Verificar si hubo errores en la respuesta
    except requests.RequestException as e:
        print("Error al agregar usuario:", e)
    return redirect(url_for("index"))

@app.route("/editar_usuario", methods=["POST"])
def editar_usuario():
    usuario = {
        "id": request.form["id"],
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"]),
        "correo": request.form["correo"]
    }
    # Llamar a la API para actualizar un usuario
    requests.put(f"{BASE_API_URL}/usuarios/{usuario['id']}", json=usuario)
    return redirect(url_for("index"))

@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    usuario_id = request.form["id"]
    # Llamar a la API para eliminar un usuario
    requests.delete(f"{BASE_API_URL}/usuarios/{usuario_id}")
    return redirect(url_for("index"))

@app.route("/eliminar_tarea/<tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    """
    Eliminar una tarea completada por su ID.
    """
    try:
        response = requests.delete(f"{BASE_API_URL}/tareas/{tarea_id}")
        response.raise_for_status()
        return "", 200  # Respuesta exitosa
    except requests.RequestException as e:
        print("Error al eliminar tarea:", e)
        return "Error al eliminar tarea", 500

if __name__ == "__main__":
    app.run(debug=True)
