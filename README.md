# L00792192-equipo-01-cloudcoder

Proyecto integrador del curso — sistema **Directorio Académico** con arquitectura de tres capas: base de datos MySQL, API REST en Python/Flask y frontend en HTML + JavaScript puro, todo ejecutándose en GitHub Codespaces sin instalar nada localmente.

---

## Estructura del repositorio

```
equipo-01/
├── backend-directorio/         ← API REST: Flask + MySQL
│   ├── .devcontainer/
│   │   └── devcontainer.json   ← Python 3.12 + Docker
│   ├── directorio.sql          ← Esquema e inserción de datos iniciales
│   ├── ws_directorio.py        ← 10 endpoints CRUD (materias y docentes)
│   └── README.md
│
├── frontend-directorio/        ← Interfaz web: HTML + CSS + fetch()
│   ├── .devcontainer/
│   │   └── devcontainer.json   ← Python 3.12
│   ├── index.html              ← Página principal con formularios y tablas
│   ├── style.css               ← Estilos de la aplicación
│   └── README.md
│
└── openapi.yaml                ← Especificación OpenAPI 3.0 de la API
```

---

## Arquitectura general

```
┌──────────────────────────────────────────────────────────────┐
│  Codespace: frontend-directorio                              │
│                                                              │
│   index.html + style.css                                     │
│   python -m http.server 8080  →  Puerto 8080                 │
│                │                                             │
│                │  fetch() HTTP/JSON                          │
└────────────────┼─────────────────────────────────────────────┘
                 │
                 ▼  URL pública puerto 3000
┌──────────────────────────────────────────────────────────────┐
│  Codespace: backend-directorio                               │
│                                                              │
│   ws_directorio.py (Flask)  →  Puerto 3000                   │
│                │                                             │
│        mysql-connector-python                                │
│                │                                             │
│   MySQL en Docker           →  Puerto 3306                   │
└──────────────────────────────────────────────────────────────┘
```

---

## Tecnologías utilizadas

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Base de datos | MySQL (Docker) | latest |
| Backend | Python + Flask + flask-cors + mysql-connector-python | 3.12 |
| Frontend | HTML5 + CSS3 + JavaScript (fetch) | — |
| Entorno | GitHub Codespaces + Docker-in-Docker | — |
| Especificación | OpenAPI | 3.0.3 |

---

## Modelo de datos

```
materias                          docentes
────────────────────────          ────────────────────────────
id        INT PK AUTO_INCREMENT   id         INT PK AUTO_INCREMENT
clave     VARCHAR(20) UNIQUE      nombre     VARCHAR(100)
nombre    VARCHAR(100)            email      VARCHAR(100) UNIQUE
creditos  INT                     materia_id INT FK → materias.id
```

`docentes.materia_id` es nullable: un docente puede existir sin materia asignada.

---

## Puesta en marcha rápida

### 1 — Levantar el backend

```bash
# En el Codespace de backend-directorio:

docker run --name mysql-directorio \
  -e MYSQL_ROOT_PASSWORD=contrasena \
  -e MYSQL_DATABASE=directorio \
  -p 3306:3306 -d mysql:latest

# Espera ~15 segundos, luego carga el esquema:
docker exec -i mysql-directorio mysql -u root -pcontrasena directorio < directorio.sql

# Instala dependencias e inicia Flask:
pip install flask flask-cors mysql-connector-python
python ws_directorio.py
```

Expón el puerto **3000** como **Public** en la pestaña **Ports** de VS Code y copia la URL pública.

### 2 — Levantar el frontend

```bash
# En el Codespace de frontend-directorio:

# Edita index.html y reemplaza la constante API con la URL pública del backend:
# const API = 'https://<nombre-codespace>-3000.app.github.dev/api/v1';

python -m http.server 8080
```

Abre el puerto **8080** en la pestaña **Ports** → el directorio ya está disponible en el navegador.

---

## Endpoints de la API

Especificación completa en [`openapi.yaml`](./openapi.yaml).

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

Base URL: `http://localhost:3000/api/v1`

---

## Instrucciones detalladas

Cada subcarpeta tiene su propio README con los pasos completos:

- [`backend-directorio/README.md`](./backend-directorio/README.md) — levantar MySQL, instalar dependencias, arrancar Flask y probar con `curl`.
- [`frontend-directorio/README.md`](./frontend-directorio/README.md) — servir el frontend, conectar con el backend y usar la interfaz.

---

## Equipo

| Número de nómina | Rol |
|-----------------|-----|
| L00792192 | Desarrollo fullstack |