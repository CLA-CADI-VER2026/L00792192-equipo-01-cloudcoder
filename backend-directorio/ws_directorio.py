import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import IntegrityError, Error as MySQLError

app = Flask(__name__)
CORS(app, origins="*")

# -----------------------------------------------------------------------------
# CONEXIÓN A LA BASE DE DATOS
# Usa variables de entorno; si no están definidas usa los valores por defecto
# del Codespace (MySQL corriendo en Docker en el mismo host).
# -----------------------------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "contrasena"),
        database=os.environ.get("DB_NAME", "directorio"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def make_error(code, message, status):
    """Respuesta de error unificada según el schema Error del YAML."""
    return jsonify({"code": code, "message": message}), status


# =============================================================================
# ENDPOINTS: MATERIAS
# =============================================================================

# GET /api/v1/materias  →  lista todas las materias
@app.route("/api/v1/materias", methods=["GET"])
def get_materias():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, clave, nombre, creditos FROM materias")
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultado), 200
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# GET /api/v1/materias/<id>  →  obtiene una materia por id
@app.route("/api/v1/materias/<int:id>", methods=["GET"])
def get_materia(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, clave, nombre, creditos FROM materias WHERE id = %s",
            (id,)
        )
        materia = cursor.fetchone()
        cursor.close()
        conn.close()
        if not materia:
            return make_error("NOT_FOUND", f"Materia con id {id} no encontrada.", 404)
        return jsonify(materia), 200
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# POST /api/v1/materias  →  crea una nueva materia
@app.route("/api/v1/materias", methods=["POST"])
def create_materia():
    data = request.get_json() or {}
    clave   = data.get("clave", "").strip()
    nombre  = data.get("nombre", "").strip()
    creditos = data.get("creditos")

    if not clave or not nombre:
        return make_error("BAD_REQUEST", "Los campos 'clave' y 'nombre' son obligatorios.", 400)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO materias (clave, nombre, creditos) VALUES (%s, %s, %s)",
            (clave, nombre, creditos)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, clave, nombre, creditos FROM materias WHERE id = %s",
            (nuevo_id,)
        )
        materia = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(materia), 201
    except IntegrityError as e:
        return make_error("BAD_REQUEST", f"La clave ya existe o datos inválidos: {str(e)}", 400)
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# PUT /api/v1/materias/<id>  →  actualiza una materia existente
@app.route("/api/v1/materias/<int:id>", methods=["PUT"])
def update_materia(id):
    data = request.get_json() or {}
    clave   = data.get("clave", "").strip()
    nombre  = data.get("nombre", "").strip()
    creditos = data.get("creditos")

    if not clave or not nombre:
        return make_error("BAD_REQUEST", "Los campos 'clave' y 'nombre' son obligatorios.", 400)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM materias WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return make_error("NOT_FOUND", f"Materia con id {id} no encontrada.", 404)

        cursor.execute(
            "UPDATE materias SET clave = %s, nombre = %s, creditos = %s WHERE id = %s",
            (clave, nombre, creditos, id)
        )
        conn.commit()

        cursor.execute(
            "SELECT id, clave, nombre, creditos FROM materias WHERE id = %s",
            (id,)
        )
        materia = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(materia), 200
    except IntegrityError as e:
        return make_error("BAD_REQUEST", f"La clave ya existe o datos inválidos: {str(e)}", 400)
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# DELETE /api/v1/materias/<id>  →  elimina una materia
@app.route("/api/v1/materias/<int:id>", methods=["DELETE"])
def delete_materia(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM materias WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return make_error("NOT_FOUND", f"Materia con id {id} no encontrada.", 404)

        cursor.execute("DELETE FROM materias WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return "", 204
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# =============================================================================
# ENDPOINTS: DOCENTES
# =============================================================================

# GET /api/v1/docentes  →  lista todos los docentes
@app.route("/api/v1/docentes", methods=["GET"])
def get_docentes():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre, email, materia_id FROM docentes"
        )
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(resultado), 200
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# GET /api/v1/docentes/<id>  →  obtiene un docente por id
@app.route("/api/v1/docentes/<int:id>", methods=["GET"])
def get_docente(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nombre, email, materia_id FROM docentes WHERE id = %s",
            (id,)
        )
        docente = cursor.fetchone()
        cursor.close()
        conn.close()
        if not docente:
            return make_error("NOT_FOUND", f"Docente con id {id} no encontrado.", 404)
        return jsonify(docente), 200
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# POST /api/v1/docentes  →  crea un nuevo docente
@app.route("/api/v1/docentes", methods=["POST"])
def create_docente():
    data = request.get_json() or {}
    nombre     = data.get("nombre", "").strip()
    email      = data.get("email", "").strip()
    materia_id = data.get("materia_id")   # opcional (FK nullable)

    if not nombre or not email:
        return make_error("BAD_REQUEST", "Los campos 'nombre' y 'email' son obligatorios.", 400)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO docentes (nombre, email, materia_id) VALUES (%s, %s, %s)",
            (nombre, email, materia_id)
        )
        conn.commit()
        nuevo_id = cursor.lastrowid

        cursor.execute(
            "SELECT id, nombre, email, materia_id FROM docentes WHERE id = %s",
            (nuevo_id,)
        )
        docente = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(docente), 201
    except IntegrityError as e:
        return make_error("BAD_REQUEST", f"Email duplicado o materia_id inválido: {str(e)}", 400)
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# PUT /api/v1/docentes/<id>  →  actualiza un docente existente
@app.route("/api/v1/docentes/<int:id>", methods=["PUT"])
def update_docente(id):
    data = request.get_json() or {}
    nombre     = data.get("nombre", "").strip()
    email      = data.get("email", "").strip()
    materia_id = data.get("materia_id")

    if not nombre or not email:
        return make_error("BAD_REQUEST", "Los campos 'nombre' y 'email' son obligatorios.", 400)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM docentes WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return make_error("NOT_FOUND", f"Docente con id {id} no encontrado.", 404)

        cursor.execute(
            "UPDATE docentes SET nombre = %s, email = %s, materia_id = %s WHERE id = %s",
            (nombre, email, materia_id, id)
        )
        conn.commit()

        cursor.execute(
            "SELECT id, nombre, email, materia_id FROM docentes WHERE id = %s",
            (id,)
        )
        docente = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(docente), 200
    except IntegrityError as e:
        return make_error("BAD_REQUEST", f"Email duplicado o materia_id inválido: {str(e)}", 400)
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# DELETE /api/v1/docentes/<id>  →  elimina un docente
@app.route("/api/v1/docentes/<int:id>", methods=["DELETE"])
def delete_docente(id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM docentes WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return make_error("NOT_FOUND", f"Docente con id {id} no encontrado.", 404)

        cursor.execute("DELETE FROM docentes WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return "", 204
    except MySQLError as e:
        return make_error("INTERNAL_SERVER_ERROR", str(e), 500)


# =============================================================================
# ARRANQUE
# =============================================================================
if __name__ == "__main__":
    # Puerto 3000 tal como define el servidor base del openapi.yaml
    app.run(host="0.0.0.0", port=3000, debug=True)
