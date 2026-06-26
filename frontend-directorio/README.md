# frontend-directorio

Interfaz web para el Directorio Académico — gestión de materias y docentes.  
Construida con **HTML + CSS + JavaScript puro** (`fetch`), sin frameworks ni dependencias.  
Se sirve con `python -m http.server 8080` desde el Codespace.

---

## Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                  GitHub Codespace                   │
│                                                     │
│  ┌──────────────────────┐   HTTP/JSON               │
│  │  Navegador           │◄─────────────────────►   │
│  │  index.html          │       Flask :3000         │
│  │  style.css           │  (backend-directorio /    │
│  │  fetch() → /api/v1/  │   otro Codespace)         │
│  └──────────────────────┘                           │
│           ▲                                         │
│           │  python -m http.server 8080             │
└───────────┼─────────────────────────────────────────┘
            │
     Puerto 8080 (VS Code → Ports)
```

---

## Requisitos previos

- El **backend** (`ws_directorio.py`) debe estar corriendo y accesible.
- Si el backend corre en el **mismo Codespace**, no necesitas cambiar nada.
- Si corre en un **Codespace separado**, necesitas su URL pública (ver Paso 3).

---

## Paso 1 — Abrir el Codespace

1. Haz clic en el botón verde **Code** → pestaña **Codespaces**.
2. Selecciona **Create codespace on main**.
3. Espera ~30 segundos. Python ya estará disponible (no necesitas instalar nada).
4. Verifica con:

```bash
python --version
```

---

## Paso 2 — Servir el frontend

En el terminal integrado de VS Code:

```bash
python -m http.server 8080
```

Luego, en la pestaña **Ports** de VS Code:

1. Localiza el puerto **8080**.
2. Haz clic en el ícono de globo 🌐 o en **Open in Browser**.
3. El Directorio Académico abrirá en tu navegador.

> Deja esta terminal corriendo. Si la cierras, el servidor se detiene.

---

## Paso 3 — Conectar con el backend

### Opción A: backend en el mismo Codespace (puerto 3000)

No necesitas cambiar nada. La URL por defecto en `index.html` ya apunta a `localhost:3000`:

```javascript
const API = 'http://localhost:3000/api/v1';
```

### Opción B: backend en otro Codespace

1. En el Codespace del backend, abre la pestaña **Ports**.
2. Localiza el puerto **3000** → clic derecho → **Port Visibility → Public**.
3. Copia la URL pública (formato: `https://<nombre-codespace>-3000.app.github.dev`).
4. Edita `index.html` y reemplaza la línea de `API`:

```javascript
const API = 'https://<nombre-codespace>-3000.app.github.dev/api/v1';
```

5. Guarda el archivo. El navegador tomará el cambio en la siguiente recarga.

> **Nota de seguridad:** regresa la visibilidad del puerto a **Private** cuando termines las pruebas.

---

## Paso 4 — Usar la aplicación

### Pantalla de Materias

| Acción | Cómo hacerlo |
|--------|-------------|
| Ver todas las materias | Se cargan automáticamente al abrir la página |
| Agregar una materia | Llena el formulario superior y haz clic en **Guardar** |
| Editar una materia | Haz clic en **✏️ Editar** en la fila correspondiente; los datos se cargan en el formulario |
| Eliminar una materia | Haz clic en **🗑️**; se pedirá confirmación |
| Actualizar la lista | Haz clic en **↻ Actualizar** |

### Pantalla de Docentes

| Acción | Cómo hacerlo |
|--------|-------------|
| Ver todos los docentes | Se cargan automáticamente al abrir la página |
| Agregar un docente | Llena el formulario y selecciona una materia del desplegable (opcional) |
| Editar un docente | Haz clic en **✏️ Editar** en la fila correspondiente |
| Eliminar un docente | Haz clic en **🗑️**; se pedirá confirmación |

> El selector de materia en el formulario de docentes se llena automáticamente con las materias registradas en la base de datos.

---

## Estructura de archivos

```
frontend-directorio/
├── .devcontainer/
│   └── devcontainer.json   ← Configura Python 3.12 en el Codespace
├── index.html              ← Página principal: estructura HTML + lógica fetch()
├── style.css               ← Todos los estilos visuales de la aplicación
└── README.md               ← Este archivo
```

### Responsabilidad de cada archivo

| Archivo | Contenido |
|---------|-----------|
| `index.html` | Estructura HTML, navegación por pestañas, tablas, formularios y funciones `fetch()` para consumir la API |
| `style.css` | Variables de color, tipografía, layout, botones, tabla, toasts y estados de carga |

---

## Referencia rápida de la API consumida

El frontend llama a estos endpoints del backend (`/api/v1`):

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

**La tabla aparece vacía o con error de conexión**  
Verifica que el backend esté corriendo (`python ws_directorio.py` en el Codespace del backend) y que el puerto 3000 esté accesible. Si usas Opción B, revisa que el puerto sea **Public** y que la URL en `index.html` sea la correcta.

**Error de CORS en la consola del navegador**  
El backend incluye `flask-cors` habilitado para todos los orígenes. Si ves este error, asegúrate de que `ws_directorio.py` esté corriendo (no una versión anterior sin CORS).

**El selector de materia en Docentes aparece vacío**  
Las materias se cargan primero al iniciar la página. Si la tabla de materias muestra error, el selector también quedará vacío. Resuelve la conexión al backend y recarga la página.

**Cambié la URL de la API pero sigue fallando**  
Haz una recarga forzada del navegador (`Ctrl + Shift + R` o `Cmd + Shift + R` en Mac) para limpiar el caché.