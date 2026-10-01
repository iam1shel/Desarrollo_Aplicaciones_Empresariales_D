# Préstamo de equipos — ORM avanzado (Laboratorio 07)

Laboratorio Semana 07. Desarrollo de Aplicaciones Empresariales (sección D).

- **Project:** `config`
- **Apps:** `core`, `equipment` y `prestamos`
- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

Parte de la aplicación de Semana 06. No se crean entidades nuevas. Se agregan dos campos enteros, dos operaciones con `transaction.atomic()` y `F()`, dos reportes y dos QuerySets.

Las dependencias siguen siendo las de `requirements.txt`: Django 5.2.17, asgiref, sqlparse y tzdata. El laboratorio no instala paquetes nuevos; transacciones, `F()`, `aggregate` y `annotate` vienen con Django.

---

## Modelos que participan

### Parte 1 — `equipment`

| Pieza | Dónde |
|---|---|
| Entidad principal | `Equipo` |
| OneToOne | `FichaTecnica` |
| 1:N | `Mantenimiento` |
| N:M con `through` | `Equipo` ↔ `Accesorio` mediante `AsignacionAccesorio` |
| Estado | `Equipo.estado` (no cambia al asignar un accesorio) |
| Número del intermedio | `AsignacionAccesorio.cantidad` |
| Entero que se descuenta | `Accesorio.existencias` |

### Parte 2 — `prestamos`

`Categoria`, `Espacio`, `Solicitante`, `Prestamo`, `DetallePrestamo`, `PerfilSolicitante` y `AutorizacionEspacio`.

| Pieza | Dónde |
|---|---|
| Entero que se descuenta | `Espacio.cupos_disponibles` |
| Capacidad física, sin descuento | `Espacio.aforo` |
| Estado | `Prestamo.estado` y `AutorizacionEspacio.estado` |
| Intermedio N:M | `AutorizacionEspacio` (fechas y estado; el total es un conteo) |

---

## Operación transaccional — Parte 1

`/equipos/asignar/` crea un `AsignacionAccesorio` con estado `vigente` y descuenta `Accesorio.existencias` con `F("existencias") - cantidad`, dentro de `transaction.atomic()`.

Si `existencias` es menor que la cantidad pedida, la vista lanza una excepción fuera del bloque atómico. El rollback borra la asignación recién insertada y deja las existencias como estaban. El mensaje se ve en el template. Si alcanza, redirige al detalle del equipo (Post/Redirect/Get).

El Admin puede crear asignaciones directo y **no** descuenta existencias. La evidencia de la transacción se toma en `/equipos/asignar/`.

## Operación transaccional — Parte 2

`/prestamos/autorizar/` crea un `AutorizacionEspacio` y descuenta 1 de `Espacio.cupos_disponibles` con `F()`, dentro de `transaction.atomic()`.

Si el cupo es 0, la excepción provoca rollback: no queda la autorización y el cupo no cambia. `aforo` no se modifica. Si hay cupo, redirige al listado de autorizaciones.

El alta antigua `/prestamos/autorizaciones/nuevo/` sigue guardando solo el formulario, sin descontar cupos. La evidencia de `F()` se toma en `/prestamos/autorizar/`.

---

## Reportes

| Pantalla | URL | Consultas |
|---|---|---|
| Equipos | `/equipos/reporte/` | `aggregate(Sum("cantidad"))` de `AsignacionAccesorio`; `annotate(Count("mantenimientos"))` por `Equipo`; `values("estado").annotate(...)` con conteo y suma de unidades. `floatformat` sobre las unidades. |
| Préstamos | `/prestamos/reporte/` | `aggregate(Count)` de `AutorizacionEspacio`; `annotate(Count("autorizaciones"))` por `Espacio`; `values("estado").annotate(Count)` ordenado de mayor a menor. `floatformat` sobre el total. |

## QuerySets

`EquipoQuerySet.as_manager()`:

- `disponibles()` — `estado="disponible"`
- `con_ficha()` — tiene `FichaTecnica`

Se encadenan en el listado (`?filtro=disponibles_con_ficha`) y en el reporte de equipos.

`PrestamoQuerySet.as_manager()`:

- `activos()` — `estado="activo"`
- `del_mes()` — `fecha_prestamo` del mes en curso

El inicio de préstamos usa los dos métodos. El listado los usa con `?estado=activo` y `?mes=actual`, y también encadenados.

## Implementado y probado

**Implementado en el código**

- `Accesorio.existencias` y la asignación en `/equipos/asignar/`, con `transaction.atomic()` y `F()`.
- `Espacio.cupos_disponibles` y la autorización en `/prestamos/autorizar/`, con `transaction.atomic()` y `F()`. `aforo` no se descuenta.
- Reportes en `/equipos/reporte/` y `/prestamos/reporte/` (`aggregate`, `annotate`, `values().annotate()`).
- `Equipo.disponibles()`, `Equipo.con_ficha()`, `Prestamo.activos()` y `Prestamo.del_mes()`.
- Consultas optimizadas que ya estaban y se conservan: el listado de equipos usa `select_related("ficha")`; el detalle de equipo usa `select_related("ficha")` y `prefetch_related`; el listado de autorizaciones usa `select_related("solicitante", "espacio")`; el listado de solicitantes usa `select_related("perfil")` y `prefetch_related("autorizaciones__espacio")`.

**Probado en navegador y en el shell**

- Asignación de accesorio exitosa, y rollback cuando las existencias no alcanzan.
- Autorización de espacio exitosa, y rollback cuando no hay cupos.
- Los dos reportes, revisados en el shell y en el navegador.
- Equipos con ficha: las consultas bajaron de 7 a 1 al usar `select_related("ficha")`.
- Autorizaciones con solicitante y espacio: las consultas bajaron de 9 a 1 al usar `select_related("solicitante", "espacio")`.

Esas dos mediciones corresponden a los listados. El detalle de equipo y el listado de solicitantes siguen optimizados en las vistas; no son las cifras de 7→1 ni de 9→1.

## N+1

`DEBUG` ya está en `True`. La medición se hace en el shell, sin quitar `select_related` ni `prefetch_related` de las vistas.

---

## Cómo correrlo

```bash
cd Semana_07/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

Si esta carpeta se copió desde Semana 06 y ya tiene `src/db.sqlite3`, basta `migrate` para agregar `existencias` y `cupos_disponibles`. Esos campos nacen en 0.

| Pantalla | URL |
|---|---|
| Asignar accesorio | http://127.0.0.1:8000/equipos/asignar/ |
| Reporte de equipos | http://127.0.0.1:8000/equipos/reporte/ |
| Autorizar espacio | http://127.0.0.1:8000/prestamos/autorizar/ |
| Reporte de préstamos | http://127.0.0.1:8000/prestamos/reporte/ |
| Admin | http://127.0.0.1:8000/admin/ |
| Equipos disponibles con ficha | http://127.0.0.1:8000/equipos/?filtro=disponibles_con_ficha |
| Préstamos activos de este mes | http://127.0.0.1:8000/prestamos/registros/?estado=activo&mes=actual |

`migrate` aplica las migraciones históricas y las dos nuevas: `equipment.0005_accesorio_existencias` y `prestamos.0005_espacio_cupos_disponibles`. `existencias` y `cupos_disponibles` quedan en 0 hasta que se editen en el Admin.

Para usar la operación de equipos, carga existencias en el accesorio y entra a `/equipos/asignar/`. Una cantidad menor o igual al saldo crea la asignación, descuenta con `F()` y redirige al detalle. Una cantidad mayor muestra el error y no deja la fila nueva. El estado del equipo no cambia.

Para usar la operación de préstamos, carga cupos en el espacio y entra a `/prestamos/autorizar/`. Con cupo disponible se crea la autorización, se resta 1 y redirige al listado. Con cupo 0 no se guarda la autorización y el aforo sigue igual. El alta antigua `/prestamos/autorizaciones/nuevo/` no descuenta cupos.

Los reportes se abren en `/equipos/reporte/` y `/prestamos/reporte/`. En el shell, los mismos totales salen con `aggregate()`, `annotate()` y `values().annotate()` sobre `AsignacionAccesorio`, `Equipo`, `AutorizacionEspacio` y `Espacio`.

Los QuerySets se usan así: `Equipo.objects.disponibles().con_ficha()` y `Prestamo.objects.activos().del_mes()`. En el navegador, los filtros de las tablas de arriba llaman a esos métodos.

## Datos que hay que completar en el Admin

La semilla ya trae 5 equipos, 2 mantenimientos y 2 asignaciones. Los accesorios quedan con `existencias = 0` y los espacios con `cupos_disponibles = 0`. No borres lo que ya existe. Agrega solo lo que falta.

**Parte 1, para llegar a 3 mantenimientos y 8 asignaciones**

1. En Accesorio, pon existencias antes de probar el éxito. Por ejemplo: Cargador Lenovo 65W = 4, Cable HDMI 2 m = 6. Crea además un accesorio «Control remoto» con existencias 1, para el caso que falla.
2. En Mantenimiento, agrega un tercer registro (cualquier equipo, fecha y tipo distintos de los dos que ya tiene Laptop 01).
3. En Asignación de accesorio, agrega filas hasta tener 8 en total. Varía `cantidad` (1, 2, 3) y `estado` (`vigente`, `devuelto`, `perdido`). Estas filas del Admin no descuentan existencias; sirven para el reporte. La captura de la transacción se hace después, en `/equipos/asignar/`.

Con 2 asignaciones sembradas, faltan 6. Un reparto posible:

| Equipo | Accesorio | Cantidad | Estado |
|---|---|---|---|
| Laptop 01 | Cable HDMI 2 m | 2 | vigente |
| Laptop 02 | Cargador Lenovo 65W | 1 | vigente |
| Proyector 01 | Control remoto | 1 | perdido |
| Tablet 01 | Cable HDMI 2 m | 3 | devuelto |
| Mouse 01 | Control remoto | 1 | vigente |
| Laptop 02 | Cable HDMI 2 m | 2 | devuelto |

**Parte 2**

1. En Espacio, deja Biblioteca con `cupos_disponibles = 2` (éxito) y Aula 201 con `0` (rollback). No cambies `aforo`.
2. El préstamo sembrado es de agosto 2026. `del_mes()` usa el mes de hoy. Para ver un préstamo «de este mes», crea uno con `fecha_prestamo` dentro del mes actual.

## Medir N+1 en el shell

Desde `Semana_07/django_proyect/src`, con el servidor detenido:

```bash
python manage.py shell
```

Listado de equipos con ficha (probado: 7 consultas sin optimizar, 1 con `select_related`):

```python
from django.db import connection, reset_queries
from equipment.models import Equipo

reset_queries()
for equipo in Equipo.objects.all():
    _ = getattr(equipo, "ficha", None)
print("ANTES", len(connection.queries))

reset_queries()
for equipo in Equipo.objects.select_related("ficha"):
    _ = getattr(equipo, "ficha", None)
print("DESPUES", len(connection.queries))
```

Listado de autorizaciones con solicitante y espacio (probado: 9 consultas sin optimizar, 1 con `select_related`):

```python
from django.db import connection, reset_queries
from prestamos.models import AutorizacionEspacio

reset_queries()
for autorizacion in AutorizacionEspacio.objects.all():
    _ = autorizacion.solicitante.nombre
    _ = autorizacion.espacio.nombre
print("ANTES", len(connection.queries))

reset_queries()
for autorizacion in AutorizacionEspacio.objects.select_related("solicitante", "espacio"):
    _ = autorizacion.solicitante.nombre
    _ = autorizacion.espacio.nombre
print("DESPUES", len(connection.queries))
```

Detalle de un equipo (optimización que permanece en `equipo_detail`):

```python
from django.db import connection, reset_queries
from equipment.models import Equipo

reset_queries()
equipo = Equipo.objects.get(nombre="Laptop 01")
_ = equipo.ficha.numero_serie
list(equipo.mantenimientos.all())
for asignacion in equipo.asignaciones_accesorio.all():
    _ = asignacion.accesorio.nombre
print("ANTES", len(connection.queries))

reset_queries()
equipo = (
    Equipo.objects.select_related("ficha")
    .prefetch_related("mantenimientos", "asignaciones_accesorio__accesorio")
    .get(nombre="Laptop 01")
)
_ = equipo.ficha.numero_serie
list(equipo.mantenimientos.all())
for asignacion in equipo.asignaciones_accesorio.all():
    _ = asignacion.accesorio.nombre
print("DESPUES", len(connection.queries))
```

Parte 2, listado de solicitantes:

```python
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, reset_queries
from prestamos.models import Solicitante

reset_queries()
for persona in Solicitante.objects.all():
    try:
        _ = persona.perfil.documento_identidad
    except ObjectDoesNotExist:
        pass
    for autorizacion in persona.autorizaciones.all():
        _ = autorizacion.espacio.nombre
print("ANTES", len(connection.queries))

reset_queries()
personas = Solicitante.objects.select_related("perfil").prefetch_related(
    "autorizaciones__espacio"
)
for persona in personas:
    try:
        _ = persona.perfil.documento_identidad
    except ObjectDoesNotExist:
        pass
    for autorizacion in persona.autorizaciones.all():
        _ = autorizacion.espacio.nombre
print("DESPUES", len(connection.queries))
```

`select_related` sirve cuando el registro relacionado es uno solo y se llega por una llave directa (`ficha`, `perfil`). `prefetch_related` sirve cuando hay una colección (`mantenimientos`, `autorizaciones`) o el otro lado de un many-to-many.
