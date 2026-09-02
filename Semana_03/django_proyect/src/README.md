# Préstamo de equipos tecnológicos — Django ORM y SQLite

Laboratorio Semana 03. Desarrollo de Aplicaciones Empresariales (sección D).

- **Project:** `config`
- **Apps:** `core` (semana 01), `equipment` (semana 02 persistente) y `prestamos` (esta semana)
- **Repositorio del curso:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

En la semana 02 los equipos vivían en una lista Python. Al reiniciar el servidor
se perdían. Esta semana los datos se guardan en SQLite con Django ORM.

---

## PARTE 1 — De la lista en memoria a Django ORM

### Ejercicio 1 — Recuperar y analizar la aplicación anterior

La app `equipment` de la semana 02 tenía:

| Pieza | Qué había |
|---|---|
| Entidad | `Equipo` (clase Python, no `models.Model`) |
| Datos | Lista `equipos` en `models.py` (mínimo 5 registros) |
| Views | `equipo_list` y `equipo_create` |
| URLs | `/equipos/` y `/equipos/nuevo/` |
| Formulario | `EquipoForm` (`forms.Form`) |
| Templates | `equipo_list.html` y `equipo_form.html` |

Qué pasaba al reiniciar: `equipos.append(...)` solo cambiaba la lista en RAM.
Al apagar `runserver` esa memoria se borra, así que el equipo nuevo desaparecía.

### Ejercicio 2 — Convertir la entidad en un Django Model

`Equipo` ahora hereda de `models.Model`. Los campos se mantienen:

| Campo | Tipo Django | ¿Obligatorio? |
|---|---|---|
| id | Auto (PK) | Sí |
| nombre | CharField(100) | Sí |
| tipo | CharField(50) | Sí |
| marca | CharField(50) | Sí |
| ubicacion | CharField(100) | Sí |
| estado | CharField con choices | Sí |
| descripcion | TextField(blank=True) | No |
| prestado_a | CharField(blank=True) | No |

`EquipoForm` pasó a ser `ModelForm`, para que `form.save()` escriba en la BD.

### Ejercicio 3 — Crear la estructura persistente

```bash
python manage.py makemigrations equipment
python manage.py migrate
python manage.py showmigrations
```

Resultado:

- `equipment.0001_initial` crea la tabla `equipment_equipo`
- `equipment.0002_seed_equipos` carga los 5 equipos de la semana 02
- `showmigrations` marca ambas con `[X]`

La migración **cambia la estructura** (columnas/tablas). El CRUD **cambia los
datos** (filas). No es lo mismo.

### Ejercicio 4 — Consulta mediante ORM

`equipo_list` ya no recorre una lista Python:

```python
equipos = Equipo.objects.all().order_by("id")
```

Eso es un QuerySet. Django ORM lo traduce a `SELECT ... FROM equipment_equipo`.

Listado: `http://127.0.0.1:8000/equipos/`

### Ejercicio 5 — Registro mediante ORM

`equipo_create` valida el POST y llama `form.save()`. Eso hace un `INSERT`.
Después redirige a `/equipos/`. Si se reinicia el servidor, el registro sigue
porque está en `db.sqlite3`.

Registro: `http://127.0.0.1:8000/equipos/nuevo/`

### Ejercicio 6 — Flujo de persistencia

**Consulta (READ)**

Request → URL `/equipos/` → View `equipo_list` → `Equipo.objects.all()`
→ Manager / QuerySet → Django ORM → `SELECT` en SQLite → View arma el context
→ Template `equipo_list.html` → Response HTML

**Creación (CREATE)**

Formulario POST → View `equipo_create` → `form.save()` → ORM → `INSERT`
en SQLite → `redirect` → listado

| Acción ORM | SQL conceptual |
|---|---|
| `objects.all()` / `filter()` / `order_by()` | SELECT |
| `form.save()` en un objeto nuevo | INSERT |
| `form.save()` sobre un objeto existente | UPDATE |
| `objeto.delete()` | DELETE |

---

## PARTE 2 — Gestión de préstamos (misma problemática, más entidades)

Sigue siendo el préstamo de equipos en una institución educativa. La semana 02
solo cubría el inventario. Aquí se agregan catálogos y el préstamo con detalle.

### Ejercicio 7 — Problemática

El préstamo de laptops, proyectores y accesorios se registra a mano. No hay
un catálogo de tipos de equipo, no se sabe en qué aula o laboratorio se usa,
tampoco quién lo pide con claridad, ni qué ítems salieron juntos en un mismo
préstamo.

Usuarios: estudiantes, docentes, personal de soporte y quien entrega/recibe
los equipos.

Proceso a mejorar: clasificar equipos, registrar espacios, identificar
solicitantes y dejar constancia del préstamo con cada ítem incluido.

### Ejercicio 8 — Requisitos funcionales

1. Registrar, listar, actualizar y eliminar categorías de equipo.
2. Registrar, listar, actualizar y eliminar espacios físicos.
3. Registrar, listar, actualizar y eliminar solicitantes.
4. Registrar un préstamo (código, solicitante, fechas y estado).
5. Listar préstamos y filtrarlos por estado (activo, devuelto, atrasado).
6. Actualizar un préstamo (por ejemplo, marcarlo como devuelto).
7. Eliminar un préstamo, con confirmación previa.
8. Agregar ítems (detalle) a un préstamo existente.
9. Listar, actualizar y eliminar esos detalles.
10. Consultar un resumen con totales en la pantalla inicial de la app.

### Ejercicio 9 — Modelo de datos

Cinco entidades. Tres independientes (sin ForeignKey) y dos relacionadas.

**Independientes**

| Entidad | Campos | PK | Por qué existe |
|---|---|---|---|
| Categoria | nombre, descripcion | id | Clasifica laptops, proyectores, accesorios |
| Espacio | nombre, edificio, piso, aforo | id | Aulas, biblioteca y laboratorios |
| Solicitante | nombre, codigo, rol, correo | id | Quién puede pedir un equipo |

**Relacionadas (1:N)**

| Entidad | Campos | PK | FK |
|---|---|---|---|
| Prestamo | codigo, nombre_solicitante, fecha_prestamo, fecha_estimada_devolucion, estado, observaciones | id | — |
| DetallePrestamo | nombre_equipo, cantidad, observacion | id | prestamo → Prestamo |

Un préstamo tiene varios detalles. El detalle no tiene sentido sin el préstamo,
por eso `on_delete=CASCADE`.

Categoria, Espacio y Solicitante quedan como catálogos independientes (el
laboratorio pide tres entidades sin relación). Prestamo guarda el nombre del
solicitante como texto, no como FK, para respetar esa regla.

### Ejercicio 10 — Diagrama

```
Categoria          Espacio           Solicitante
(independiente)    (independiente)   (independiente)


Prestamo  1 ──────── N  DetallePrestamo
  id                      id
  codigo                  prestamo_id  (FK)
  nombre_solicitante      nombre_equipo
  fechas / estado         cantidad
```

### Ejercicio 11 — App creada: `prestamos`

Registrada en `INSTALLED_APPS` y montada en `config/urls.py`:

- Inicio: `http://127.0.0.1:8000/prestamos/`
- Categorías: `/prestamos/categorias/`
- Espacios: `/prestamos/espacios/`
- Solicitantes: `/prestamos/solicitantes/`
- Préstamos: `/prestamos/registros/`
- Detalles: `/prestamos/detalles/`

### Ejercicio 12 — Models

Los cinco modelos están en `prestamos/models.py`.
`DetallePrestamo.prestamo` es el `ForeignKey` hacia `Prestamo`.

### Ejercicio 13 — Migraciones de la nueva app

```bash
python manage.py makemigrations prestamos
python manage.py migrate
python manage.py showmigrations
```

- `prestamos.0001_initial` crea las cinco tablas
- `prestamos.0002_seed_datos` carga ejemplos (categorías, espacios, etc.)

### Ejercicio 14 — CREATE

Cada entidad tiene un formulario (`ModelForm`). POST válido → `form.save()`
(INSERT) → redirect al listado.

### Ejercicio 15 — READ

Cada listado usa QuerySet:

- `Categoria.objects.all().order_by("nombre")`
- `Espacio.objects.all().order_by("edificio", "nombre")`
- `Solicitante.objects.filter(rol=...)` (filtro por querystring)
- `Prestamo.objects.filter(estado=...).order_by("-fecha_prestamo")`
- `DetallePrestamo.objects.select_related("prestamo")`

### Ejercicio 16 — UPDATE

Editar carga el objeto con `get_object_or_404`, arma el formulario con
`instance=...` y en el POST llama `form.save()` (UPDATE).

### Ejercicio 17 — DELETE

El enlace abre una confirmación (GET). Solo el botón **Sí, eliminar** envía
POST y ejecuta `objeto.delete()` (DELETE). Luego redirige al listado.

### Publicar en GitHub

Actualizar `requirements.txt` y este README, hacer commit y push al
repositorio del curso.

---

## Cómo correrlo

```bash
cd Semana_03/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

URLs:

| Pantalla | URL |
|---|---|
| Catálogo `core` | `http://127.0.0.1:8000/` |
| Equipos | `http://127.0.0.1:8000/equipos/` |
| Nuevo equipo | `http://127.0.0.1:8000/equipos/nuevo/` |
| Gestión de préstamos | `http://127.0.0.1:8000/prestamos/` |

---

## Evidencia por integrante

### Mishel Rojas

- **Nombre:** Mishel Rojas
- **Título:** Persistencia con Django ORM y CRUD de préstamos
- **Qué hizo:** Convertir `Equipo` a Model, migraciones SQLite, app `prestamos`
  con cinco entidades, relación ForeignKey y CRUD completo.
- **Código:** `src/equipment/` y `src/prestamos/`
- **Explicación:** Las Views ya no usan listas en memoria. Leen y escriben con
  el ORM (`objects.all()`, `filter()`, `save()`, `delete()`). SQLite guarda
  los cambios aunque se reinicie el servidor.
- **Casos de prueba:**

| # | Qué hago | Qué espero | Resultado |
|---|---|---|---|
| 1 | Abro `/equipos/` | Veo los 5 equipos sembrados | Cumplido |
| 2 | Registro un equipo nuevo y reinicio el servidor | El equipo sigue en el listado | Cumplido |
| 3 | Abro `/prestamos/` | Veo totales de las 5 entidades | Cumplido |
| 4 | Filtro solicitantes por rol=docente | Solo aparecen docentes | Cumplido |
| 5 | Filtro préstamos activos | Solo estado activo | Cumplido |
| 6 | Edito un préstamo y lo marco devuelto | El listado muestra el nuevo estado | Cumplido |
| 7 | Intento eliminar un detalle y cancelo | El registro no se borra | Cumplido |
| 8 | Confirmo eliminar un detalle (POST) | Desaparece del listado | Cumplido |

---

## Conclusiones

1. Una lista Python no sirve como persistencia: se pierde al reiniciar. Un
   Model + SQLite sí guarda los datos.
2. Django ORM evita escribir SQL a mano. `all`/`filter` son SELECT, `save` es
   INSERT o UPDATE, `delete` es DELETE.
3. `makemigrations` / `migrate` cambian la **estructura** de la base. El CRUD
   cambia las **filas**.
4. ForeignKey modela el 1:N entre préstamo y detalle. Las otras tres entidades
   quedan independientes, como pide el laboratorio.
5. El flujo completo de esta semana es:

Request → URL → View → Model → Manager/QuerySet → ORM → SQLite → Template → Response
