# Préstamo de equipos tecnológicos — Django

Proyecto de Desarrollo de Aplicaciones Empresariales (Semana 02).
Project: `config`. Apps: `core` (semana 01) y `equipment` (esta semana).

## Problemática

En una institución educativa el préstamo de laptops, proyectores y otros
equipos se registra a mano. Cuesta saber qué está disponible y quién lo tiene,
y eso genera pérdidas, retrasos y confusión en las devoluciones.
La aplicación permite registrar equipos, préstamos y devoluciones.
La usan estudiantes, docentes y el personal encargado de los equipos.

## Requisitos funcionales

- Registrar equipos tecnológicos
- Registrar un préstamo de equipo
- Registrar la devolución / actualizar el estado (disponible o prestado)
- Consultar el listado de equipos disponibles
- Consultar quién tiene un equipo prestado

## App creada: `equipment`

- Listado: `http://127.0.0.1:8000/equipos/`
- Registro: `http://127.0.0.1:8000/equipos/nuevo/`
- Datos en una lista en memoria (`models.py`), no en base de datos.

La app `core` (semana 01) sigue disponible en `http://127.0.0.1:8000/` (catálogo de items).

## Requisitos de software

- Python
- Django 5.2.17

## Instalación

Crear y activar un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

Instalar dependencias y arrancar el servidor:

```bash
pip install -r requirements.txt
cd src
python manage.py runserver
```

## Nota sobre los datos (app equipment)

Los equipos se guardan en una lista en memoria (`models.py`), no en base de datos.
Los registros nuevos se pierden al reiniciar el servidor. Esto es esperado en esta semana.

## Recorrido Request → Response (app equipment)

Un Project de Django es el contenedor (`config`). Dentro conviven varias Apps.
`core` es el catálogo de items de la semana 01.
`equipment` es el préstamo de equipos de esta semana.
Ambas están en INSTALLED_APPS y cada una tiene su propia URL.

### Listado

1. **Request.** El navegador pide GET `http://127.0.0.1:8000/equipos/`.
2. **URL.** `config/urls.py` ve el prefijo `equipos/` y pasa a `equipment/urls.py`.
   Ahí `path('', ...)` llama a la vista `equipo_list`.
3. **View.** `equipo_list` en `equipment/views.py` toma la lista `equipos`.
4. **Model (datos estáticos).** No hay base de datos: los datos están en
   `equipment/models.py` (clase `Equipo` + lista `equipos`).
5. **Template.** Se renderiza `equipment/equipo_list.html`, que hereda de `base.html`.
6. **Response.** Django devuelve el HTML y el navegador muestra las tarjetas.

### Crear y volver al listado

1. **Request.** GET `/equipos/nuevo/` abre el formulario (`equipo_create` + `equipo_form.html`).
2. Al guardar, el navegador envía **POST** con los campos.
3. **View.** `equipo_create` valida con `EquipoForm`. Si está bien, hace
   `equipos.append(...)` (se agrega en memoria) y `redirect("equipo_list")`.
4. **Response.** El navegador carga otra vez `/equipos/` y el dato nuevo aparece.
   Si se reinicia el servidor, ese registro se pierde (lista en memoria).

### Cómo conviven `core` y `equipment`

| | core | equipment |
|---|---|---|
| Tema | Catálogo de items | Préstamo de equipos |
| URL | `/` | `/equipos/` y `/equipos/nuevo/` |
| Datos | Modelo `Item` (SQLite) | Lista `equipos` en memoria |
| Archivos | `src/core/` | `src/equipment/` |

El Project (`config`) las une: las registra en `INSTALLED_APPS` y las enruta en `config/urls.py`.
No se pisan porque cada app tiene su prefijo de URL.
`equipment` reutiliza `base.html` y el CSS de `core` (`{% extends "base.html" %}`).
