# L00792192-equipo-01-cloudcoder

Proyecto integrador del curso — sistema **Directorio Académico** con arquitectura de tres capas: base de datos MySQL, API REST en Python/Flask y frontend en HTML + JavaScript puro, todo ejecutándose en un único GitHub Codespace.

---

## Estructura del repositorio

```
L00792192-equipo-01-cloudcoder/
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

Todo corre en **un solo Codespace**. El frontend se sirve sobre HTTPS, por lo que el puerto del backend debe exponerse como público para que el navegador pueda alcanzarlo.

```
Navegador (HTTPS)
      │
      │  puerto 8080 público
      ▼
┌──────────────────────────────────────────────────┐
│              GitHub Codespace                    │
│                                                  │
│  python -m http.server 8080                      │
│  └── frontend-directorio/                        │
│       ├── index.html                             │
│       └── style.css                              │
│                    │                             │
│                    │ fetch() HTTPS               │
│                    │ puerto 3000 público         │
│                    ▼                             │
│  python backend-directorio/ws_directorio.py      │
│  Flask → puerto 3000                             │
│                    │                             │
│          mysql-connector-python                  │
│                    │                             │
│  docker: mysql → puerto 3306                     │
└──────────────────────────────────────────────────┘
```

> **Importante:** aunque backend y frontend están en el mismo Codespace, el
> navegador bloquea peticiones `fetch()` de HTTPS a `http://localhost`
> (Mixed Content). Por eso el puerto 3000 debe ser **Public** y se debe usar
> su URL pública en `index.html`.

---

## Tecnologías utilizadas

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Base de datos | MySQL (Docker) | latest |
| Backend | Python + Flask + flask-cors + mysql-connector-python | 3.12 |
| Frontend | HTML5 + CSS3 + JavaScript (fetch) | — |
| Entorno | GitHub Codespaces + Docker | — |
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

Todos los comandos se ejecutan desde la **raíz del workspace**.

### Terminal 1 — Base de datos y backend

```bash
# 1. Levantar MySQL en Docker
docker run --name mysql-directorio \
  -e MYSQL_ROOT_PASSWORD=contrasena \
  -e MYSQL_DATABASE=directorio \
  -p 3306:3306 -d mysql:latest

# 2. Espera ~15 segundos, luego carga el esquema
docker exec -i mysql-directorio mysql -u root -pcontrasena directorio \
  < backend-directorio/directorio.sql

# 3. Instalar dependencias
pip install flask flask-cors mysql-connector-python

# 4. Iniciar Flask
python backend-directorio/ws_directorio.py
```

### Exponer el puerto 3000 como público

En la pestaña **Ports** de VS Code:
- Puerto **3000** → clic derecho → **Port Visibility → Public**
- Copia la URL pública: `https://<nombre-codespace>-3000.app.github.dev`

### Terminal 2 — Frontend

```bash
# Servir el frontend desde la raíz apuntando a la subcarpeta
python -m http.server 8080 --directory frontend-directorio
```

### Configurar la URL del backend en index.html

Edita `frontend-directorio/index.html` y reemplaza la constante `API`:

```javascript
const API = 'https://<nombre-codespace>-3000.app.github.dev/api/v1';
```

Abre el puerto **8080** en la pestaña **Ports** → **Open in Browser**.

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

Base URL: `https://<nombre-codespace>-3000.app.github.dev/api/v1`

---

## Instrucciones detalladas

- [`backend-directorio/README.md`](./backend-directorio/README.md) — levantar MySQL, instalar dependencias, arrancar Flask, exponer el puerto y probar con `curl`.
- [`frontend-directorio/README.md`](./frontend-directorio/README.md) — servir el frontend, configurar la URL pública del backend y usar la interfaz.

---

## Equipo

| Número de nómina | Rol |
|-----------------|-----|
| L00792192 | Desarrollo fullstack |