# frontend-directorio

Interfaz web para el Directorio Académico — gestión de materias y docentes.  
Construida con **HTML + CSS + JavaScript puro** (`fetch`), sin frameworks ni dependencias.  
Se sirve con `python -m http.server 8080` desde la raíz del Codespace.

---

## Arquitectura

```
Navegador
   │  HTTPS (puerto 8080 público de Codespaces)
   ▼
┌─────────────────────────────────────────────────────┐
│                  GitHub Codespace                   │
│                                                     │
│  python -m http.server 8080                         │
│  └── frontend-directorio/                           │
│       ├── index.html                                │
│       └── style.css                                 │
│                                                     │
│  fetch() → URL pública puerto 3000 (HTTPS)          │
│       │                                             │
│  Flask :3000  (ws_directorio.py)                    │
│       │                                             │
│  MySQL en Docker :3306                              │
└─────────────────────────────────────────────────────┘
```

> **Por qué se necesita la URL pública del puerto 3000:**  
> El frontend se sirve sobre HTTPS desde Codespaces. Los navegadores bloquean
> peticiones `fetch()` a `http://localhost` desde páginas HTTPS (Mixed Content).
> Aunque Flask y el frontend estén en el **mismo Codespace**, el puerto 3000
> debe exponerse como público para que el navegador pueda alcanzarlo por HTTPS.

> Todos los comandos se ejecutan desde la **raíz del workspace**:  
> `/workspaces/L00792192-equipo-01-cloudcoder`

---

## Paso 1 — Abrir el Codespace

1. Haz clic en el botón verde **Code** → pestaña **Codespaces**.
2. Selecciona **Create codespace on main**.
3. Espera ~30 segundos. Python ya estará disponible.
4. Verifica con:

```bash
python --version
```

---

## Paso 2 — Asegúrate de que el backend esté corriendo

El frontend depende de la API REST. Antes de servir el frontend, verifica que Flask esté activo en el puerto 3000 y que el puerto sea **público**. Sigue los pasos del [`backend-directorio/README.md`](../backend-directorio/README.md).

---

## Paso 3 — Configurar la URL del backend en index.html

Dado que el frontend se sirve sobre HTTPS, debes usar la URL pública del puerto 3000 en lugar de `localhost`.

1. En VS Code, abre la pestaña **Ports**.
2. Localiza el puerto **3000** → verifica que su visibilidad sea **Public**.
3. Copia la URL pública (formato: `https://<nombre-codespace>-3000.app.github.dev`).
4. Abre `frontend-directorio/index.html` y edita la línea de la constante `API`:

```javascript
// Reemplaza esta línea:
const API = 'http://localhost:3000/api/v1';

// Por la URL pública del puerto 3000, por ejemplo:
const API = 'https://zany-garbanzo-4jv65pwgjj4h744r-3000.app.github.dev/api/v1';
```

> El nombre del Codespace (`zany-garbanzo-...`) es el mismo que aparece en la URL
> del puerto 8080 — solo cambia el número de puerto al final.

---

## Paso 4 — Servir el frontend

```bash
python -m http.server 8080 --directory frontend-directorio
```

Luego, en la pestaña **Ports** de VS Code:

1. Localiza el puerto **8080**.
2. Haz clic en el ícono de globo 🌐 o en **Open in Browser**.
3. El Directorio Académico abrirá en tu navegador.

> Deja esta terminal corriendo. Si la cierras, el servidor se detiene.

---

## Paso 5 — Usar la aplicación

### Pantalla de Materias

| Acción | Cómo hacerlo |
|--------|-------------|
| Ver todas las materias | Se cargan automáticamente al abrir la página |
| Agregar una materia | Llena el formulario superior y haz clic en **Guardar** |
| Editar una materia | Haz clic en **✏️ Editar**; los datos se cargan en el formulario |
| Eliminar una materia | Haz clic en **🗑️**; se pedirá confirmación |
| Actualizar la lista | Haz clic en **↻ Actualizar** |

### Pantalla de Docentes

| Acción | Cómo hacerlo |
|--------|-------------|
| Ver todos los docentes | Se cargan automáticamente al abrir la página |
| Agregar un docente | Llena el formulario y selecciona una materia del desplegable (opcional) |
| Editar un docente | Haz clic en **✏️ Editar** en la fila correspondiente |
| Eliminar un docente | Haz clic en **🗑️**; se pedirá confirmación |

> El selector de materia en el formulario de docentes se llena automáticamente con las materias registradas.

---

## Estructura de archivos

```
frontend-directorio/
├── .devcontainer/
│   └── devcontainer.json   ← Configura Python 3.12 en el Codespace
├── index.html              ← Página principal: HTML + lógica fetch()
├── style.css               ← Todos los estilos visuales de la aplicación
└── README.md               ← Este archivo
```

| Archivo | Contenido |
|---------|-----------|
| `index.html` | Estructura HTML, navegación por pestañas, tablas, formularios y funciones `fetch()` para consumir la API |
| `style.css` | Variables de color, tipografía, layout, botones, tabla, toasts y estados de carga |

---

## Referencia rápida de la API consumida

| Método | Ruta | Cuándo se llama |
|--------|------|----------------|
| GET | `/materias` | Al cargar la página y al actualizar |
| GET | `/materias/{id}` | Al hacer clic en Editar |
| POST | `/materias` | Al guardar una materia nueva |
| PUT | `/materias/{id}` | Al guardar cambios de una materia editada |
| DELETE | `/materias/{id}` | Al confirmar la eliminación |
| GET | `/docentes` | Al cargar la página y al actualizar |
| GET | `/docentes/{id}` | Al hacer clic en Editar |
| POST | `/docentes` | Al guardar un docente nuevo |
| PUT | `/docentes/{id}` | Al guardar cambios de un docente editado |
| DELETE | `/docentes/{id}` | Al confirmar la eliminación |

---

## Solución de problemas frecuentes

**Error: `NetworkError when attempting to fetch resource`**  
El navegador está bloqueando la petición a `localhost` desde una página HTTPS. Asegúrate de haber configurado la URL pública del puerto 3000 en `index.html` (Paso 3) y de que el puerto 3000 sea **Public** en la pestaña Ports.

**La tabla aparece vacía después de configurar la URL**  
Verifica que Flask esté corriendo (`python backend-directorio/ws_directorio.py`) y que MySQL esté activo (`docker ps`). Haz una recarga forzada con **Ctrl + Shift + R**.

**El selector de materia en Docentes aparece vacío**  
Las materias se cargan primero al iniciar. Si la tabla de materias muestra error, el selector también quedará vacío. Resuelve la conexión al backend y recarga la página.

**`style.css` da 404**  
Asegúrate de ejecutar el servidor con `--directory frontend-directorio` desde la raíz del workspace, no desde dentro de la carpeta.

**Cambié la URL pero sigue fallando**  
Haz una recarga forzada del navegador: **Ctrl + Shift + R** (o **Cmd + Shift + R** en Mac).