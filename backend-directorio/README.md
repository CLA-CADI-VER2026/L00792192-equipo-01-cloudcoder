# backend-directorio

API REST para el Directorio Académico — gestión de materias y docentes.  
Construida con **Flask + MySQL**, corre en el puerto **3000** dentro de un GitHub Codespace.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                  GitHub Codespace                   │
│                                                     │
│  ┌─────────────┐  HTTP/JSON  ┌───────────────────┐  │
│  │ curl /      │◄───────────►│  Flask :3000      │  │
│  │ Postman /   │             │  ws_directorio.py │  │
│  │ Frontend    │             └────────┬──────────┘  │
│  └─────────────┘                     │              │
│                          mysql-connector-python      │
│                                      │              │
│                          ┌───────────▼──────────┐   │
│                          │  MySQL en Docker     │   │
│                          │  (contenedor :3306)  │   │
│                          └──────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## Requisitos previos

El Codespace ya tiene Python 3.12 y Docker disponibles gracias al `devcontainer.json`.  
No necesitas instalar nada en tu máquina local.

---

## Paso 1 — Abrir el Codespace

1. Haz clic en el botón verde **Code** → pestaña **Codespaces**.
2. Selecciona **Create codespace on main**.
3. Espera ~60 segundos mientras se configura el entorno (Python 3.12 + Docker).
4. Verifica que Docker esté disponible:

```bash
docker --version
```

---

## Paso 2 — Levantar MySQL en Docker

```bash
docker run --name mysql-directorio \
  -e MYSQL_ROOT_PASSWORD=contrasena \
  -e MYSQL_DATABASE=directorio \
  -p 3306:3306 \
  -d mysql:latest
```

| Parámetro | Significado |
|-----------|-------------|
| `--name mysql-directorio` | Nombre del contenedor |
| `MYSQL_ROOT_PASSWORD` | Contraseña del usuario `root` |
| `MYSQL_DATABASE=directorio` | Crea la base de datos automáticamente |
| `-p 3306:3306` | Expone el puerto al Codespace |
| `-d` | Ejecuta en segundo plano |

Verifica que el contenedor esté corriendo:

```bash
docker ps
```

---

## Paso 3 — Crear las tablas e insertar datos iniciales

Espera ~15 segundos para que MySQL termine de iniciar, luego ejecuta:

```bash
docker exec -i mysql-directorio mysql -u root -pcontrasena directorio < directorio.sql
```

Para verificar que las tablas y datos estén listos:

```bash
docker exec -it mysql-directorio mysql -u root -pcontrasena -e "USE directorio; SELECT * FROM materias; SELECT * FROM docentes;"
```

---

## Paso 4 — Instalar dependencias Python

```bash
pip install flask flask-cors mysql-connector-python
```

| Paquete | Propósito |
|---------|-----------|
| `flask` | Microframework web para construir la API REST |
| `flask-cors` | Habilita CORS para que el frontend pueda consumir la API |
| `mysql-connector-python` | Driver oficial para conectar Python con MySQL |

---

## Paso 5 — Iniciar el servidor

```bash
python ws_directorio.py
```

El servidor queda corriendo en `http://localhost:3000`. Deberías ver:

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:3000
```

---

## Paso 6 — Probar los endpoints con `curl`

Abre una **segunda terminal** (el servidor debe seguir corriendo en la primera).

### Materias

```bash
# Listar todas
curl -X GET http://localhost:3000/api/v1/materias

# Obtener una por id
curl -X GET http://localhost:3000/api/v1/materias/1

# Crear
curl -X POST http://localhost:3000/api/v1/materias \
  -H "Content-Type: application/json" \
  -d '{"clave": "TC3001", "nombre": "Bases de Datos", "creditos": 4}'

# Actualizar
curl -X PUT http://localhost:3000/api/v1/materias/1 \
  -H "Content-Type: application/json" \
  -d '{"clave": "TC1028", "nombre": "Programación en Python", "creditos": 6}'

# Eliminar
curl -X DELETE http://localhost:3000/api/v1/materias/4
```

### Docentes

```bash
# Listar todos
curl -X GET http://localhost:3000/api/v1/docentes

# Obtener uno por id
curl -X GET http://localhost:3000/api/v1/docentes/1

# Crear
curl -X POST http://localhost:3000/api/v1/docentes \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Laura Martínez", "email": "laura.martinez@tec.mx", "materia_id": 1}'

# Actualizar
curl -X PUT http://localhost:3000/api/v1/docentes/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Laura Martínez Ramos", "email": "laura.martinez@tec.mx", "materia_id": 2}'

# Eliminar
curl -X DELETE http://localhost:3000/api/v1/docentes/3
```

---

## Paso 7 — Exponer el puerto para el frontend (opcional)

Si el frontend corre en un Codespace separado, debes hacer el puerto 3000 público:

1. En VS Code, abre la pestaña **Ports**.
2. Localiza el puerto **3000**.
3. Haz clic derecho → **Port Visibility → Public**.
4. Copia la URL pública (formato: `https://<nombre-codespace>-3000.app.github.dev`).
5. Usa esa URL como `API_BASE` en el `index.html` del frontend.

> **Nota de seguridad:** regresa la visibilidad a **Private** cuando termines las pruebas.

---

## Referencia de la API

La especificación completa está en [`openapi.yaml`](../openapi.yaml).  
Puedes visualizarla en [https://oas-validation.com](https://oas-validation.com) pegando el contenido del archivo.

### Resumen de endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/materias` | Lista todas las materias |
| GET | `/api/v1/materias/{id}` | Obtiene una materia |
| POST | `/api/v1/materias` | Crea una materia |
| PUT | `/api/v1/materias/{id}` | Actualiza una materia |
| DELETE | `/api/v1/materias/{id}` | Elimina una materia |
| GET | `/api/v1/docentes` | Lista todos los docentes |
| GET | `/api/v1/docentes/{id}` | Obtiene un docente |
| POST | `/api/v1/docentes` | Crea un docente |
| PUT | `/api/v1/docentes/{id}` | Actualiza un docente |
| DELETE | `/api/v1/docentes/{id}` | Elimina un docente |

Todas las respuestas de error siguen el esquema:

```json
{
  "code": "NOT_FOUND",
  "message": "Materia con id 99 no encontrada."
}
```

---

## Variables de entorno (opcional)

Por defecto el servidor usa los valores del Codespace. Si necesitas conectarte a otra instancia de MySQL puedes sobreescribirlos:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `DB_HOST` | `127.0.0.1` | Host de MySQL |
| `DB_PORT` | `3306` | Puerto de MySQL |
| `DB_USER` | `root` | Usuario |
| `DB_PASSWORD` | `contrasena` | Contraseña |
| `DB_NAME` | `directorio` | Base de datos |

Ejemplo:

```bash
DB_PASSWORD=mipass python ws_directorio.py
```

---

## Estructura de archivos

```
backend-directorio/
├── .devcontainer/
│   └── devcontainer.json   ← Configura Python 3.12 + Docker en el Codespace
├── directorio.sql          ← Script SQL: crea tablas e inserta datos iniciales
├── ws_directorio.py        ← API REST con Flask (10 endpoints CRUD)
└── README.md               ← Este archivo
```