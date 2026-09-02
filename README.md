# Desarrollo de Aplicaciones Empresariales — Sección D

Este es **el repositorio del curso**. Ábrelo en Cursor y trabaja aquí.

GitHub: https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D


## Semanas

| Semana | Contenido |
|---|---|
| [Semana 01](Semana_01/django_proyect/src) | App Django `core`: catálogo de items |
| [Semana 02](Semana_02/django_proyect/src) | App Django `equipment`: préstamo de equipos (datos en memoria) |
| [Semana 03](Semana_03/django_proyect/src) | ORM + SQLite: `equipment` persistente y app `prestamos` con CRUD |
| Semana 04 – 16 | Pendiente |

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

## Cómo está organizado

Cada carpeta `Semana_XX` es un laboratorio. `core` es el catálogo de la semana 01.
`equipment` es el inventario de equipos. `prestamos` es la gestión de préstamos
de la semana 03.
