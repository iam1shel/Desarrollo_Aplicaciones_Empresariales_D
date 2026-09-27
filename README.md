# Desarrollo de Aplicaciones Empresariales — Sección D

Este es **el repositorio del curso**. Ábrelo en Cursor y trabaja aquí.

GitHub: https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D


## Semanas

| Semana | Contenido |
|---|---|
| [Semana 01](Semana_01/django_proyect/src) | App Django `core`: catálogo de items |
| [Semana 02](Semana_02/django_proyect/src) | App Django `equipment`: préstamo de equipos (datos en memoria) |
| [Semana 03](Semana_03/django_proyect/src) | ORM + SQLite: `equipment` persistente y app `prestamos` con CRUD |
| [Semana 04](Semana_04/django_proyect/src) | Relaciones 1:1, 1:N y N:M (`through`) sobre equipos y préstamos |
| [Semana 05](Semana_05/django_proyect/src) | Django Admin: ModelAdmin, list_display, search, filtros e inlines |
| [Semana 06](Semana_06/django_proyect/src) | Motor de plantillas: herencia, filtros, comentarios e include |
| Semana 07 – 16 | Pendiente |

## Semana 01

Catálogo de items (`core`). Listado en `/` y API en `/api/items/`.

```bash
cd Semana_01/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

## Semana 02

Problemática: en una institución educativa el préstamo de laptops, proyectores
y otros equipos se registra a mano. La app `equipment` permite registrar equipos
y ver el listado.

- Listado: `http://127.0.0.1:8000/equipos/`
- Registro: `http://127.0.0.1:8000/equipos/nuevo/`

## Semana 03

Misma problemática (préstamo de equipos), ahora con persistencia en SQLite.

- Equipos (ORM): `http://127.0.0.1:8000/equipos/`
- Gestión de préstamos: `http://127.0.0.1:8000/prestamos/`

Apps: `equipment` (Model + migraciones) y `prestamos` (5 entidades, ForeignKey
préstamo→detalle, CRUD completo).

```bash
cd Semana_03/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

## Semana 04

Misma problemática, ahora con los tres tipos de relación de Django.

- Equipos + ficha 1:1: `http://127.0.0.1:8000/equipos/`
- Detalle (1:1, mantenimientos 1:N, accesorios N:M): `http://127.0.0.1:8000/equipos/1/`
- Autorizaciones (CRUD del through): `http://127.0.0.1:8000/prestamos/autorizaciones/`

```bash
cd Semana_04/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

## Semana 05

Misma aplicación de Semana 04, ahora con el panel `/admin/`.

```bash
cd Semana_05/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Login Admin: `http://127.0.0.1:8000/admin/`
- Solicitantes (StackedInline 1:1 + TabularInline N:M): `http://127.0.0.1:8000/admin/prestamos/solicitante/`

## Semana 06

Misma aplicación de Semana 05. Los Templates públicos pasan a compartir
`base.html` (menú y pie), usan filtros (`date`, `upper`, `length`),
comentarios `{# #}` e `{% include %}` para el estado del equipo, la
autorización N:M y los botones Editar/Eliminar. Las Views y las URLs no cambian.

```bash
cd Semana_06/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

- Equipos: `http://127.0.0.1:8000/equipos/`
- Detalle (1:1, 1:N, N:M): `http://127.0.0.1:8000/equipos/1/`
- Préstamos: `http://127.0.0.1:8000/prestamos/`
- Autorizaciones: `http://127.0.0.1:8000/prestamos/autorizaciones/`

## Cómo está organizado

Cada carpeta `Semana_XX` es un laboratorio. `core` es el catálogo de la semana 01.
`equipment` es el inventario de equipos. `prestamos` es la gestión de préstamos
de la semana 03. En la semana 04 esas mismas apps ganan relaciones 1:1, 1:N y N:M.
En la semana 05 se administran desde Django Admin, sin crear modelos nuevos.
En la semana 06 esos mismos Templates se refactorizan con herencia, filtros e include.
