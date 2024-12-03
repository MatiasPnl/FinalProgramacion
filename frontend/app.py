from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# URL base de la API
BASE_API_URL = "http://127.0.0.1:8000"

@app.route("/")
def index():
    # Obtener usuarios y tareas desde la API
    usuarios = requests.get(f"{BASE_API_URL}/usuarios/").json()
    tareas = requests.get(f"{BASE_API_URL}/tareas/").json()
    return render_template("index.html", usuarios=usuarios, tareas=tareas)

@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():
    usuario = {
        "id": request.form["id"],
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"]),
        "correo": request.form["correo"]
    }
    # Llamar a la API para crear un nuevo usuario
    requests.post(f"{BASE_API_URL}/usuarios/", json=usuario)
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

@app.route("/asignar_tarea", methods=["POST"])
def asignar_tarea():
    tarea = {
        "id": f"tarea-{request.form['tarea']}",
        "usuario_id": request.form["usuario_id"],
        "tarea": request.form["tarea"],
        "id_estado": 1  # Estado pendiente
    }
    # Llamar a la API para asignar una tarea
    requests.post(f"{BASE_API_URL}/tareas/", json=tarea)
    return redirect(url_for("index"))

@app.route("/tareas_usuario", methods=["GET"])
def tareas_usuario():
    usuario_id = request.args.get("usuario_id")
    # Obtener las tareas de un usuario específico desde la API
    tareas = requests.get(f"{BASE_API_URL}/tareas/{usuario_id}").json()
    usuarios = requests.get(f"{BASE_API_URL}/usuarios/").json()
    return render_template("index.html", usuarios=usuarios, tareas=tareas)

if __name__ == "__main__":
    app.run(debug=True)
