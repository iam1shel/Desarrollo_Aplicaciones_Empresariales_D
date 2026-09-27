# Préstamo de equipos — Motor de plantillas (Laboratorio 06)

Laboratorio Semana 06. Desarrollo de Aplicaciones Empresariales (sección D).

- **Project:** `config`
- **Apps:** `core`, `equipment` y `prestamos`
- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

Esta semana **no se crean Views ni URLs nuevas**. Se retoma la aplicación de
Semana 05 y se refactorizan los Templates que ya existían: herencia con
`base.html`, filtros, comentarios y `{% include %}`.

Flujo (igual que antes; cambia solo el Template):

Navegador → URL ya existente → `urls.py` → View ya existente → ORM → SQLite → Template (`extends` / `include` / filtros) → Response

El Django Admin de la Semana 05 sigue en `/admin/`. Las pantallas públicas
siguen en sus mismas URLs.

---

## Laboratorio 06 - Motor de plantillas

**Objetivo.** Reutilizar una estructura común y aplicar la sintaxis de
plantillas sin cambiar el CRUD.

### Qué se refactorizó

| Pieza | Dónde |
|---|---|
| Base común (nav, `block content`, pie) | `core/templates/base.html` |
| Filtros `upper`, `date`, `length` | Listado y detalle de equipos; préstamos y autorizaciones |
| Comentarios `{# #}` | `base.html`, detalle de equipo, formularios, solicitantes |
| `{% include %}` del estado | `equipment/_estado_equipo.html` (listado y detalle) |
| `{% include %}` del N:M | `prestamos/_autorizacion.html` (solicitante, espacio y autorizaciones) |
| `{% include %}` de Editar/Eliminar | `includes/acciones.html` (listados CRUD de `prestamos`) |

### Entidades de la investigación propia (`prestamos`)

1. `Categoria`
2. `Espacio`
3. `Solicitante`
4. `Prestamo`
5. `DetallePrestamo`
6. `PerfilSolicitante` (se ve dentro del solicitante, relación 1:1)
7. `AutorizacionEspacio` (modelo intermedio N:M)

---

## PARTE 1 — Templates de equipos (Semana 4/5)

### Ejercicio 1 — Auditoría

En Semana 05 los Templates de `equipment` **ya usaban** `{% extends "base.html" %}`.
No había pie de página, ni filtros de fecha, ni `{% include %}`.

### Ejercicio 2 — `base.html`

`base.html` define el encabezado, el menú y el pie. El bloque
`{% block content %}` queda para cada pantalla. Las Views no se tocaron.

### Ejercicios 3 y 4 — Herencia

Siguen heredando de `base.html`, sin cambiar la View:

- `equipment/equipo_list.html`
- `equipment/equipo_form.html`
- `equipment/equipo_detail.html`
- `core/item_list.html`

### Ejercicio 5 — Filtros

- `{{ equipos|length }}` en el listado
- `{{ equipo.tipo|upper }}` y `{{ equipo.marca|upper }}`
- `{{ equipo.get_estado_display|upper }}` en el fragmento del estado
- `{{ equipo.ficha.fecha_adquisicion|date:"d/m/Y" }}` en el detalle (1:1)

### Ejercicio 6 — Comentario

En `equipo_detail.html`, un comentario explica que `ficha` es el acceso
directo del OneToOne.

### Ejercicio 7 — `include`

`equipment/_estado_equipo.html` se inserta en el listado y en el detalle.
Así el badge de estado no está copiado en dos archivos.

### Ejercicio 8 — Auto-escape

Si en el formulario de equipo se guarda un texto con `<script>`, Django lo
muestra escapado (`&lt;script&gt;`) en el HTML. El Admin de la Semana 05 ya
protegía el panel `/admin/`; esta refactorización hace lo mismo en las
pantallas públicas, y además comparte menú, pie y fragmentos.

---

## PARTE 2 — Templates de la investigación propia

### Ejercicio 9 — Auditoría

Las siete entidades ya tenían Template (el perfil 1:1 se muestra dentro del
solicitante). Todas heredaban `base.html`. Para este laboratorio se
profundizó en el listado de préstamos (filtro `date`) y en las pantallas que
muestran la relación N:M (`solicitante_list` y `autorizacion_list`).

### Checklist

1. Los listados heredan `base.html` y definen `{% block content %}`.
2. La relación N:M sigue viéndose después de la migración (`Biblioteca`, estado).
3. Filtros: `date:"d/m/Y"` en préstamos y autorizaciones; `upper` en el estado; `length` en el detalle del préstamo.
4. Comentario en `solicitante_list.html` sobre perfil 1:1 y `autorizaciones`.
5. `{% include "prestamos/_autorizacion.html" %}` en solicitantes, espacios y autorizaciones.
6. El CRUD no cambió: las mismas URLs de crear, listar, editar y eliminar.
7. Un valor `<script>alert(1)</script>` en la descripción de una categoría sale escapado en `/prestamos/categorias/`.
8. Esas pantallas siguen fuera de `/admin/`.
9. El Admin evita programar el panel interno. La herencia evita repetir el HTML público: un cambio de menú o de pie se hace una sola vez en `base.html`.

### Ejercicio 10 — Resto de Templates

También heredan `base.html`: inicio de préstamos, categorías, espacios,
detalles, formulario compartido y confirmación de borrado.

### Ejercicio 11 — `include` del N:M

`prestamos/_autorizacion.html` es el fragmento del modelo intermedio.
`includes/acciones.html` reutiliza Editar y Eliminar entre los listados.

### Ejercicio 12 — Seguridad

El formulario existente de categorías (y el resto, que usan `form.html`)
escapa el texto al renderizar. No se usa `|safe`.

### Ejercicio 13 — Flujo

Las URLs públicas siguen igual. `/admin/` sigue administrando los mismos modelos.

---

## Cómo correrlo

```bash
cd Semana_06/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| Pantalla | URL |
|---|---|
| Equipos (filtros + include del estado) | `http://127.0.0.1:8000/equipos/` |
| Detalle con relaciones y fechas | `http://127.0.0.1:8000/equipos/1/` |
| Préstamos | `http://127.0.0.1:8000/prestamos/` |
| Solicitantes (1:1 y N:M) | `http://127.0.0.1:8000/prestamos/solicitantes/` |
| Autorizaciones (through) | `http://127.0.0.1:8000/prestamos/autorizaciones/` |
| Admin (sin cambios de Semana 05) | `http://127.0.0.1:8000/admin/` |

---

## Conclusiones

1. `{% extends %}` y `{% block %}` separan la estructura común del contenido de cada pantalla.
2. Los filtros dan formato en el Template (`date`, `upper`, `length`) sin tocar la View.
3. `{% include %}` evita copiar el mismo HTML en dos pantallas.
4. El auto-escape es la defensa por defecto contra XSS en las páginas públicas.
5. El Admin y los Templates públicos resuelven cosas distintas: el panel interno y la interfaz del usuario.
