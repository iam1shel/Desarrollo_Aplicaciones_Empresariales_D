# Desarrollo de Aplicaciones Empresariales — Sección D

Bienvenido al repositorio de Mishel. Aquí están los laboratorios del curso
**Desarrollo de Aplicaciones Empresariales**, de la semana 2 a la 16.

## Semanas

| Semana | Contenido |
|---|---|
| [Semana 02](Semana_02/django_proyect/src) | App Django `equipment`: préstamo de equipos tecnológicos |
| Semana 03 – 16 | Pendiente |

## Semana 02

Problemática: en una institución educativa el préstamo de laptops, proyectores
y otros equipos se registra a mano. La app `equipment` permite registrar equipos
y ver el listado.

- Listado: `http://127.0.0.1:8000/equipos/`
- Registro: `http://127.0.0.1:8000/equipos/nuevo/`

Cómo correrlo:

```bash
cd Semana_02/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py runserver
```

## Cómo está organizado

Cada carpeta `Semana_XX` es un laboratorio. `core` es la app de la semana 01
(catálogo de items) y convive en el mismo Project con `equipment`.
