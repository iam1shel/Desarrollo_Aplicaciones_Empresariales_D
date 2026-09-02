# Catálogo de items — Django

Laboratorio Semana 01. Desarrollo de Aplicaciones Empresariales (sección D).

- **Project:** `config`
- **App:** `core` (catálogo de items)
- **Repositorio del curso:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

Este laboratorio es el catálogo web de items: modelo `Item` en SQLite,
listado en `/` y API en `/api/items/` que el buscador consume con JavaScript.

---

## Cómo correrlo

```bash
cd Semana_01/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

- Listado: `http://127.0.0.1:8000/`
- API: `http://127.0.0.1:8000/api/items/`
