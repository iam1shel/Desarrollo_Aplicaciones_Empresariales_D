# Préstamo de equipos — relaciones Django (1:1, 1:N, N:M)

Laboratorio Semana 04. Desarrollo de Aplicaciones Empresariales (sección D).

- **Project:** `config`
- **Apps:** `core`, `equipment` (relaciones sobre `Equipo`) y `prestamos` (investigación propia ampliada)
- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

En la semana 03 los datos ya vivían en SQLite. Esta semana el Model gana
cardinalidad: `OneToOneField`, `ForeignKey` y `ManyToManyField(through=...)`.

Flujo:

Request → URL → View → Model (con relaciones) → Manager / QuerySet → Django ORM → SQLite → Template → Response

---

## PARTE 1 — Relaciones sobre la app de la Semana 3 (`equipment`)

### Ejercicio 1 — Recuperar la aplicación

Entidad principal: **`Equipo`**.

| Pieza | Estado en Semana 3 |
|---|---|
| Model | `Equipo` (`models.Model`) en SQLite |
| Views | `equipo_list`, `equipo_create` |
| Templates | `equipo_list.html`, `equipo_form.html` |
| Migraciones | `equipment.0001_initial` y `0002_seed_equipos` |

Esa entidad es el punto de partida de las tres relaciones de esta sesión.

### Ejercicio 2 — Relación uno a uno

Nueva entidad: **`FichaTecnica`**.

- `equipo = OneToOneField(Equipo, on_delete=CASCADE, related_name="ficha")`
- Campos propios: número de serie, fechas de adquisición/garantía, especificaciones
- `on_delete=CASCADE`: si se borra el equipo, la ficha no tiene sentido
- No son “más campos de Equipo”: la ficha es opcional y concentra datos de
  inventario técnico que no todo registro tiene el día uno

### Ejercicio 3 — Relación uno a muchos

Nueva entidad: **`Mantenimiento`**.

- `equipo = ForeignKey(Equipo, on_delete=CASCADE, related_name="mantenimientos")`
- El lado “muchos” es `Mantenimiento` (un equipo tiene varios servicios)
- La FK se declara ahí porque cada fila de mantenimiento apunta a **un** equipo
- `CASCADE`: al retirar un equipo del inventario se pierden sus órdenes de
  mantenimiento asociadas

### Ejercicio 4 — Relación muchos a muchos con `through`

Entidades: **`Equipo`** y **`Accesorio`**. Modelo intermedio: **`AsignacionAccesorio`**.

```python
equipos = models.ManyToManyField(Equipo, through="AsignacionAccesorio", related_name="accesorios")
```

Atributos propios de la relación (no del equipo ni del accesorio):

- `cantidad`
- `fecha_asignacion`
- `estado` (vigente / devuelto / perdido)

Un cargador HDMI puede usarse con varios equipos a lo largo del tiempo, y un
equipo puede llevar varios accesorios. Lo que se presta juntos es la asignación.

### Ejercicio 5 — Migraciones

```bash
python manage.py makemigrations equipment
python manage.py migrate
python manage.py showmigrations equipment
```

- `0003_accesorio_asignacionaccesorio_...` crea ficha, mantenimiento, accesorio y through
- `0004_seed_relaciones` carga ejemplos (Laptop 01 con ficha, 2 mantenimientos y cargador)

### Ejercicio 6 — Consultar desde la View

- Listado: `Equipo.objects.select_related("ficha")` (1:1, JOIN)
- Detalle: `select_related("ficha").prefetch_related("mantenimientos", "asignaciones_accesorio__accesorio")`

`select_related` = JOIN (FK / OneToOne). `prefetch_related` = consulta extra para
el lado inverso o el through, evita N+1.

URLs:

- Listado: `http://127.0.0.1:8000/equipos/`
- Detalle con relaciones: `http://127.0.0.1:8000/equipos/<id>/`

### Ejercicio 7 — Templates

En `equipo_detail.html`:

- Acceso directo 1:1: `equipo.ficha.numero_serie`
- Acceso inverso 1:N: `equipo.mantenimientos.all`
- Recorrido del through: `equipo.asignaciones_accesorio.all` → `asg.accesorio.nombre`, `asg.cantidad`, `asg.estado`

### Ejercicio 8 — Flujo de la relación 1:1

1. Request GET `/equipos/1/`
2. URL `equipment.urls` → `equipo_detail`
3. View: `select_related("ficha")` pide el ORM
4. Model `Equipo` + `FichaTecnica` (OneToOne)
5. ORM → SQL conceptual: `SELECT ... FROM equipment_equipo LEFT OUTER JOIN equipment_fichatecnica ...`
6. SQLite devuelve la fila del equipo y su ficha
7. View arma `{"equipo": equipo}`
8. Template usa `equipo.ficha.numero_serie`
9. Response HTML

| Acción ORM | SQL conceptual |
|---|---|
| `select_related("ficha")` | SELECT + JOIN |
| `prefetch_related("mantenimientos")` | SELECT extra por FK inversa |
| `form.save()` (objeto nuevo) | INSERT |
| `form.save()` (existente) | UPDATE |
| `objeto.delete()` | DELETE |

---

## PARTE 2 — Ampliación de la investigación propia (`prestamos`)

Misma problemática: préstamo de equipos en una institución educativa.
Las cinco entidades de la semana 03 se mantienen.

### Ejercicio 9 — Auditoría frente a los criterios

| Criterio | Cumple | Cómo |
|---|---|---|
| 1. Mismo dominio y mismas 5 entidades | Directo | `Categoria`, `Espacio`, `Solicitante`, `Prestamo`, `DetallePrestamo` |
| 2. ForeignKey se mantiene | Directo | `DetallePrestamo.prestamo` con `related_name="detalles"` y `CASCADE` (el detalle no existe sin el préstamo) |
| 3. OneToOneField nuevo | Extiende | `PerfilSolicitante` (ficha de contacto). No son más campos de `Solicitante`: el perfil es opcional y concentra DNI/teléfono/área |
| 4. ManyToManyField con through | Extiende | `Solicitante` ↔ `Espacio` vía `AutorizacionEspacio` (`fecha_inicio`, `fecha_fin`, `estado` pertenecen a la autorización) |
| 5. Justificación de negocio | Directo | Ver párrafos abajo |
| 6. Mínimo 7 entidades | Directo | 5 originales + `PerfilSolicitante` + `AutorizacionEspacio` |
| 7. Migraciones aplicadas | Directo | `prestamos.0003_...` y `0004_seed_relaciones` |
| 8. Vista/template con datos relacionados | Directo | Listado de solicitantes y de espacios |
| 9. CRUD del modelo intermedio | Directo | `/prestamos/autorizaciones/` |

**Justificación 1:N (ya existía).** Un préstamo (`Prestamo`) agrupa varios ítems
que salen juntos. `DetallePrestamo` es el lado muchos: cada fila apunta a un
solo préstamo. `CASCADE` porque borrar el préstamo invalida sus líneas.

**Justificación 1:1.** El perfil institucional no es el solicitante mismo: una
persona puede estar registrada (código + rol) antes de completar DNI, teléfono
o ciclo. La ficha vive o muere con el solicitante (`CASCADE`).

**Justificación N:M.** No todo estudiante puede sacar equipos de cualquier aula.
La autorización cruza persona y espacio, y guarda vigencia (`fecha_inicio`,
`fecha_fin`) y `estado`. Esos tres datos no caben en `Solicitante` ni en `Espacio`.

### Ejercicio 10 — Modelos nuevos

Ver `prestamos/models.py`:

- `PerfilSolicitante.solicitante` → `OneToOneField(..., related_name="perfil")`
- `Solicitante.espacios` → `ManyToManyField(Espacio, through="AutorizacionEspacio")`
- `AutorizacionEspacio` con FK a ambos lados

### Ejercicio 11 — Migrar

```bash
python manage.py makemigrations prestamos
python manage.py migrate
python manage.py showmigrations prestamos
```

### Ejercicio 12 — Consultar y mostrar

- Solicitantes: `select_related("perfil").prefetch_related("autorizaciones__espacio")`
- Espacios: `prefetch_related("autorizaciones__solicitante")` (acceso inverso)
- Template: `solicitante.perfil.documento_identidad` y `solicitante.autorizaciones.all`

### Ejercicio 13 — CRUD del through

`/prestamos/autorizaciones/` crea, edita y elimina `AutorizacionEspacio`
(solicitante, espacio, fechas y estado), no solo asocia IDs.

### Ejercicio 14 — GitHub

Repositorio: https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

---

## Cómo correrlo

```bash
cd Semana_04/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

| Pantalla | URL |
|---|---|
| Equipos + ficha 1:1 | `http://127.0.0.1:8000/equipos/` |
| Detalle con 1:1, 1:N y N:M | `http://127.0.0.1:8000/equipos/1/` |
| Préstamos | `http://127.0.0.1:8000/prestamos/` |
| Solicitantes con perfil | `http://127.0.0.1:8000/prestamos/solicitantes/` |
| CRUD autorizaciones | `http://127.0.0.1:8000/prestamos/autorizaciones/` |

---

## Evidencia por integrante

### Mishel Rojas

- **Nombre:** Mishel Rojas
- **Título:** Relaciones 1:1, 1:N y N:M con Django ORM
- **Qué hizo:** `FichaTecnica`, `Mantenimiento` y `AsignacionAccesorio` sobre
  `Equipo`; `PerfilSolicitante` y `AutorizacionEspacio` sobre la investigación
  propia; Views con `select_related`/`prefetch_related` y CRUD del through.
- **Código:** `src/equipment/` y `src/prestamos/`
- **Explicación:** La relación se define en el Model, la View la consulta con
  el ORM y el Template la presenta (acceso directo, inverso y through).
- **Casos de prueba:**

| # | Qué hago | Qué espero | Resultado |
|---|---|---|---|
| 1 | Abro `/equipos/` | Veo serie de Laptop 01 vía `equipo.ficha` | Cumplido |
| 2 | Abro `/equipos/1/` | Ficha, mantenimientos y cargador | Cumplido |
| 3 | Abro `/prestamos/solicitantes/` | Perfil de Ana y sus espacios | Cumplido |
| 4 | Abro `/prestamos/espacios/` | Acceso inverso de autorizados | Cumplido |
| 5 | Registro una autorización y la edito a revocada | El listado muestra el nuevo estado | Cumplido |
| 6 | Confirmo eliminar esa autorización | Desaparece del listado | Cumplido |

---

## Conclusiones

1. `OneToOneField` modela una ficha que existe como máximo una vez por registro.
2. `ForeignKey` se declara en el lado muchos. `related_name` es el acceso inverso.
3. `ManyToManyField(through=...)` sirve cuando la relación tiene datos propios
   (cantidad, fechas, estado).
4. `select_related` hace JOIN (1:1 / FK). `prefetch_related` evita N+1 en 1:N y N:M.
5. El CRUD del through edita la relación, no solo las entidades de los extremos.
