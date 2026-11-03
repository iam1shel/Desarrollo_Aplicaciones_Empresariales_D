# Préstamo de equipos — Introducción a React con Vite (Laboratorio 09)

Laboratorio Semana 09. Desarrollo de Aplicaciones Empresariales (sección D).

- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D
- **Backend:** [`src/`](src), el proyecto Django de la Semana 08 sin cambios (`config`, `core`, `equipment`, `prestamos` y la API REST bajo `/api/`)
- **Frontend:** [`frontend/`](frontend), proyecto nuevo de React creado con `npm create vite@latest frontend -- --template react`
- **Capturas:** [`capturas/`](capturas)

React no reemplaza a Django: lo complementa. Lo que en un Template se escribía con `{{ }}`, `{% for %}` y `{% if %}`, en `App.jsx` se escribe con llaves, `map()` y condicionales de JavaScript. Esta semana los datos están escritos a mano con la misma forma que el JSON de la API de la Semana 08; en la Semana 12 se reemplazan por llamadas a esa API.

## Cómo correrlo

```bash
cd Semana_09/django_proyect/frontend
npm install
npm run dev
```

Abrir http://localhost:5173/. Instrucciones completas y descripción de la interfaz en [`frontend/README.md`](frontend/README.md).

El backend no hace falta para esta semana. Si se quiere comparar con la API real:

```bash
cd Semana_09/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

## Equivalencias Python/Django y Node.js/React

| Elemento | Python y Django | Node.js y React |
|---|---|---|
| Lenguaje | Python | JavaScript (con JSX) |
| Gestor de paquetes | `pip` | `npm` |
| Archivo de dependencias | `requirements.txt` | `package.json` (y `package-lock.json` con las versiones exactas) |
| Carpeta de dependencias | `venv/` (entorno virtual) | `node_modules/` |
| Servidor de desarrollo | `python manage.py runserver` (puerto 8000) | `npm run dev` (Vite, puerto 5173) |

## Tabla de equivalencias con la clase (cafetería)

| Concepto de clase | Parte 1 — aplicación de las Semanas 4 a 8 | Parte 2 — investigación propia |
|---|---|---|
| Lista de productos (id, nombre, precio, stock) | `accesorios`: id, nombre, tipo y existencias (5 registros) | `espacios`: id, nombre, edificio, piso, aforo y cupos_disponibles (5 registros); además `solicitantes` |
| Dato que activa un mensaje (stock 0 → Agotado) | `existencias === 0` → «Agotado»; 1 o 2 → «¡Últimas unidades!» | `cupos_disponibles === 0` → «Sin cupos»; de 1 a 3 → «¡Últimos cupos!» |
| Relación 1:N anidada (pedidos con detalles) | Cada `equipo` con su arreglo `asignaciones_accesorio` (1:N hacia el modelo intermedio) y total de unidades en uso | Cada `solicitante` con su arreglo `autorizaciones` (modelo intermedio `AutorizacionEspacio`) y conteo de vigentes |
| Forma de los datos (`GET /api/productos/`) | `GET /api/accesorios/` y `GET /api/equipos/` | `GET /api/espacios/` y `GET /api/solicitantes/` |

Los modelos de la Semana 08 no tienen campos `DecimalField`, así que la API no devuelve decimales como texto. Los números (`existencias`, `aforo`, `cupos_disponibles`) llegan como enteros y las fechas como texto `AAAA-MM-DD`; `toFixed()` se usa en los porcentajes calculados (participación en el stock, equipos disponibles y ocupación).

Los registros salen de `db.sqlite3` de la Semana 08. Para ejercitar todos los mensajes se agregaron tres registros a mano: el accesorio «Adaptador USB-C a HDMI» (0 existencias), los espacios «Sala 105» y «Auditorio», y la solicitante «Lucía Ramos» (sin perfil ni autorizaciones). En los espacios, los cupos disponibles se escribieron con valores distintos, porque en la base los tres valen 0. El equipo «Prueba XSS» de la base no se copió.

## Template de Django frente a React

Un Template de la Semana 6 se procesa en el servidor: Django ejecuta la View, consulta la base y devuelve HTML ya armado; cada clic pide una página nueva. En React, el navegador recibe una sola página (`index.html`) y JavaScript dibuja la interfaz a partir de los datos; al cambiar un dato, React actualiza solo lo necesario sin recargar (se comprobó con la recarga en caliente de Vite). Para conectar esta interfaz con la API de la Semana 8 falta: pedir los datos con `fetch` en lugar de escribirlos a mano, guardarlos en el estado del componente (`useState` y `useEffect`), mostrar mensajes de carga y de error, y habilitar CORS en Django (por ejemplo con `django-cors-headers`) para que `localhost:5173` pueda llamar a `127.0.0.1:8000`.

## Verificación

- `npm run lint`: sin advertencias ni errores (código de salida 0).
- `npm run build`: genera `dist/` sin errores (17 módulos).
- Consola del navegador: 0 advertencias o errores, incluidas las advertencias de `key`.
- `node_modules/` y `dist/` están en `frontend/.gitignore` y no se suben al repositorio.
