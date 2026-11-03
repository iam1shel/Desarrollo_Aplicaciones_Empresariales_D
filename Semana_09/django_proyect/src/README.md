# Préstamo de equipos — Backend Django y API REST (base del Laboratorio 09)

Backend de la Semana 09. Es la misma aplicación del Laboratorio 08, sin cambios: en la Semana 09 el trabajo nuevo está en [`../frontend`](../frontend) (React + Vite) y se resume en [`../README.md`](../README.md). Lo que sigue documenta la API de la Semana 08, cuya forma de respuesta copian los arreglos de `frontend/src/App.jsx`.

- **Project:** `config`
- **Apps:** `core`, `equipment` y `prestamos`
- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

Parte de la aplicación de Semana 07. No se crean entidades ni migraciones nuevas: los mismos modelos, relaciones y QuerySets personalizados se exponen como una API REST que responde JSON bajo `/api/`. Los Templates, el Admin y las operaciones transaccionales de semanas anteriores siguen funcionando igual.

Dependencia nueva: `djangorestframework==3.18.3` (agregada a `requirements.txt` y `'rest_framework'` en `INSTALLED_APPS`).

---

## Archivos nuevos o modificados

| Archivo | Contenido |
|---|---|
| `config/settings.py` | `'rest_framework'` en `INSTALLED_APPS` |
| `config/api_urls.py` | `DefaultRouter` con los seis recursos y las dos vistas genéricas del ejercicio 4 |
| `config/urls.py` | `path('api/', include('config.api_urls'))` |
| `equipment/serializers.py` | `AccesorioSerializer` (con `validate_nombre`) y `EquipoSerializer` anidado |
| `equipment/api_views.py` | Vistas genéricas, `AccesorioViewSet` y `EquipoViewSet` |
| `prestamos/serializers.py` | `CategoriaSerializer`, `EspacioSerializer` (con `validate_aforo`), `SolicitanteSerializer` y `PrestamoSerializer` anidados |
| `prestamos/api_views.py` | `CategoriaViewSet`, `EspacioViewSet`, `SolicitanteViewSet` y `PrestamoViewSet` |
| `equipment/tests.py`, `prestamos/tests.py` | Pruebas de la API (códigos de estado, filtros, acciones y número de consultas) |
| `core/templates/base.html` | Enlace «API» en el menú y pie «Semana 08» |

---

## Tabla de equivalencias

| Concepto de clase (cafetería) | Parte 1 — `equipment` | Parte 2 — `prestamos` |
|---|---|---|
| Recurso simple con regla de negocio (`Producto`, precio > 0) | `Accesorio`: el nombre tiene al menos 3 caracteres y no se repite (las existencias se llevan en un solo registro) | `Espacio`: el aforo es de al menos una persona |
| Recurso con relaciones, solo lectura (`Pedido` con detalles) | `Equipo` con `ficha` (1:1), `mantenimientos` (1:N) y `asignaciones_accesorio` (N:M con `through`) | `Solicitante` con `perfil` (1:1) y `autorizaciones` (N:M con `through`); además `Prestamo` con `detalles` (1:N) |
| Campo de estado para `?estado=` | `Equipo.estado` | `Prestamo.estado` (y `?rol=` en solicitantes) |
| Método del QuerySet personalizado (`pagados()`) | `EquipoQuerySet.disponibles()` y `con_ficha()` | `PrestamoQuerySet.activos()` y `del_mes()` |

---

## Recursos de la API

Raíz navegable: http://127.0.0.1:8000/api/

| URL | ViewSet / vista | Métodos | Extras |
|---|---|---|---|
| `/api/accesorios/` | `AccesorioViewSet` (`ModelViewSet`) | GET, POST, PUT, PATCH, DELETE | `?search=` (nombre, tipo), `?ordering=` (nombre, tipo, existencias) |
| `/api/equipos/` | `EquipoViewSet` (`ReadOnlyModelViewSet`) | GET | `?estado=`, acción `/api/equipos/disponibles/` (`?con_ficha=1` encadena `con_ficha()`) |
| `/api/categorias/` | `CategoriaViewSet` (`ModelViewSet`) | GET, POST, PUT, PATCH, DELETE | — |
| `/api/espacios/` | `EspacioViewSet` (`ModelViewSet`) | GET, POST, PUT, PATCH, DELETE | `?search=` (nombre, edificio), `?ordering=` (nombre, aforo, cupos_disponibles) |
| `/api/solicitantes/` | `SolicitanteViewSet` (`ReadOnlyModelViewSet`) | GET | `?rol=` |
| `/api/prestamos/` | `PrestamoViewSet` (`ReadOnlyModelViewSet`) | GET | `?estado=`, acciones `/api/prestamos/activos/` y `/api/prestamos/del-mes/` |
| `/api/genericas/accesorios/` y `/api/genericas/accesorios/<id>/` | `ListCreateAPIView` y `RetrieveUpdateDestroyAPIView` | Los mismos que el ViewSet | Primera versión del ejercicio 4, conservada para comparar |

El `DefaultRouter` genera para cada `ModelViewSet` dos rutas: la lista (`/api/accesorios/`, con GET y POST) y el detalle (`/api/accesorios/<id>/`, con GET, PUT, PATCH y DELETE), además de la raíz `/api/` y los sufijos de formato (`?format=json`). En los `ReadOnlyModelViewSet` solo quedan GET de lista y de detalle; un POST o DELETE responde 405. Cada `@action(detail=False)` agrega una ruta más bajo la lista.

---

## Ejercicios 2, 3 y 10 — serializar y validar en el shell

Desde `Semana_08/django_proyect/src`:

```bash
python manage.py shell
```

Serializar (ejercicio 2):

```python
from equipment.models import Accesorio
from equipment.serializers import AccesorioSerializer

AccesorioSerializer(Accesorio.objects.first()).data
AccesorioSerializer(Accesorio.objects.all(), many=True).data
```

Salida obtenida con los datos actuales:

```text
{'id': 2, 'nombre': 'Cable HDMI 2 m', 'tipo': 'Video', 'existencias': 5}
[{'id': 2, 'nombre': 'Cable HDMI 2 m', ...}, {'id': 1, 'nombre': 'Cargador Lenovo 65W', ...}, {'id': 3, 'nombre': 'Control Remoto', ...}]
```

`many=True` hace falta porque un QuerySet es una colección: el serializer recorre cada objeto y devuelve una lista de diccionarios. Sin `many=True` intentaría leer `nombre` del QuerySet como si fuera un único accesorio.

Deserializar y validar (ejercicio 3). El caso válido sí se guarda:

```python
valido = AccesorioSerializer(data={"nombre": "Puntero láser", "tipo": "Presentación", "existencias": 2})
valido.is_valid()        # True
valido.validated_data    # {'nombre': 'Puntero láser', 'tipo': 'Presentación', 'existencias': 2}
valido.save()            # <Accesorio: Puntero láser>

invalido = AccesorioSerializer(data={"nombre": "ab", "tipo": "Video", "existencias": -1})
invalido.is_valid()      # False
invalido.errors
# {'nombre': ['El nombre del accesorio debe tener al menos 3 caracteres.'],
#  'existencias': ['Asegúrese de que este valor es mayor o igual a 0.']}
```

El error de `nombre` viene de `validate_nombre`; el de `existencias` lo agrega DRF solo, porque el campo del modelo es `PositiveIntegerField`. Un nombre repetido (por ejemplo `"cable hdmi 2 m"`) también falla, sin importar mayúsculas.

Validación de la investigación (ejercicio 10):

```python
from prestamos.serializers import EspacioSerializer

ok = EspacioSerializer(data={"nombre": "Sala 105", "edificio": "Central", "aforo": 30})
ok.is_valid()            # True

mal = EspacioSerializer(data={"nombre": "Depósito", "edificio": "Central", "aforo": 0})
mal.is_valid()           # False
mal.errors               # {'aforo': ['El aforo debe ser de al menos una persona.']}
```

---

## Ejercicios 6 y 11 — CRUD y códigos de estado

Peticiones para Thunder Client, Postman o curl (servidor en `http://127.0.0.1:8000`). En POST, PUT y PATCH usar cuerpo JSON.

| # | Petición | Cuerpo | Código esperado |
|---|---|---|---|
| 1 | `GET /api/accesorios/` | — | 200 OK |
| 2 | `GET /api/accesorios/2/` | — | 200 OK |
| 3 | `POST /api/accesorios/` | `{"nombre": "Puntero láser", "tipo": "Presentación", "existencias": 2}` | 201 Created |
| 4 | `POST /api/accesorios/` | `{"nombre": "ab", "tipo": "Video", "existencias": -1}` | 400 Bad Request |
| 5 | `PATCH /api/accesorios/<id creado>/` | `{"existencias": 5}` | 200 OK |
| 6 | `DELETE /api/accesorios/<id creado>/` | — | 204 No Content |
| 7 | `GET /api/accesorios/99999/` | — | 404 Not Found |

Para la Parte 2 se repite sobre espacios:

| # | Petición | Cuerpo | Código esperado |
|---|---|---|---|
| 1 | `GET /api/espacios/` | — | 200 OK |
| 2 | `POST /api/espacios/` | `{"nombre": "Sala 105", "edificio": "Central", "piso": "1", "aforo": 30}` | 201 Created |
| 3 | `POST /api/espacios/` | `{"nombre": "Depósito", "edificio": "Central", "aforo": 0}` | 400 Bad Request |
| 4 | `PUT /api/espacios/<id creado>/` | `{"nombre": "Sala 105", "edificio": "Central", "piso": "1", "aforo": 35, "cupos_disponibles": 2}` | 200 OK |
| 5 | `DELETE /api/espacios/<id creado>/` | — | 204 No Content |
| 6 | `GET /api/espacios/<id borrado>/` | — | 404 Not Found |

Ojo: estas peticiones sí modifican `db.sqlite3`. El POST deja un registro hasta que se hace el DELETE.

Un Template devuelve una página HTML ya armada para una persona en el navegador. La API devuelve solo los datos en JSON y el código de estado HTTP, para que otro programa (una app móvil o el React de la Semana 9) decida cómo mostrarlos. La API queda abierta porque no tiene autenticación ni permisos: DRF usa por defecto `AllowAny`, así que cualquiera que llegue a la URL puede crear, editar o borrar. Eso se resuelve cuando se trabaje la seguridad.

---

## Ejercicios 7 y 12 — Solo lectura con relaciones anidadas y número de consultas

`EquipoViewSet.get_queryset()` usa `select_related("ficha")` (1:1) y `prefetch_related("mantenimientos", "asignaciones_accesorio__accesorio")` (colecciones). `SolicitanteViewSet.get_queryset()` usa `select_related("perfil")` y `prefetch_related("autorizaciones__espacio")`. `PrestamoViewSet` usa `prefetch_related("detalles")`.

Medición en el shell, serializando todos los registros:

```python
from django.db import connection, reset_queries
from equipment.models import Equipo
from equipment.serializers import EquipoSerializer

reset_queries()
EquipoSerializer(Equipo.objects.all(), many=True).data
print("ANTES", len(connection.queries))

reset_queries()
qs = Equipo.objects.select_related("ficha").prefetch_related(
    "mantenimientos", "asignaciones_accesorio__accesorio"
)
EquipoSerializer(qs, many=True).data
print("DESPUES", len(connection.queries))
```

```python
from django.db import connection, reset_queries
from prestamos.models import Solicitante
from prestamos.serializers import SolicitanteSerializer

reset_queries()
SolicitanteSerializer(Solicitante.objects.all(), many=True).data
print("ANTES", len(connection.queries))

reset_queries()
qs = Solicitante.objects.select_related("perfil").prefetch_related("autorizaciones__espacio")
SolicitanteSerializer(qs, many=True).data
print("DESPUES", len(connection.queries))
```

Resultados con los datos actuales de `db.sqlite3`:

| Recurso | Registros | Antes | Después |
|---|---|---|---|
| `Equipo` (ficha, mantenimientos, asignaciones con accesorio) | 6 equipos, 9 asignaciones | 28 | 4 |
| `Solicitante` (perfil, autorizaciones con espacio) | 2 solicitantes, 4 autorizaciones | 9 | 3 |
| `Prestamo` (detalles) | 2 préstamos | 3 | 2 |

En `Prestamo` la diferencia es pequeña porque hay pocos préstamos: sin optimizar son 1 + N consultas y con `prefetch_related` siempre son 2.

Después de optimizar, el número de consultas ya no depende de cuántos registros haya. Las pruebas automáticas lo verifican con `assertNumQueries`: 4 en `/api/equipos/`, 3 en `/api/solicitantes/` y 2 en `/api/prestamos/`.

---

## Ejercicios 8 y 13 — Búsqueda, ordenamiento, filtros y acciones

| URL | Qué hace | Resultado con los datos actuales |
|---|---|---|
| `/api/accesorios/?search=cable` | `SearchFilter` en nombre y tipo | Cable HDMI 2 m |
| `/api/accesorios/?ordering=-existencias` | `OrderingFilter` | Cable HDMI (5), Cargador (4), Puntero láser (2), Control Remoto (1) |
| `/api/accesorios/?search=ca&ordering=-existencias` | Búsqueda y orden combinados con `&` | Cable HDMI (5), Cargador (4) |
| `/api/equipos/?estado=prestado` | Filtro en `get_queryset()` | Proyector 01, Mouse 01, Tablet 01 |
| `/api/equipos/disponibles/` | `@action` → `Equipo.objects.disponibles()` | Laptop 01, Laptop 02, Prueba XSS |
| `/api/equipos/disponibles/?con_ficha=1` | Encadena `disponibles().con_ficha()` | Laptop 01 |
| `/api/espacios/?search=a&ordering=-aforo` | Búsqueda y orden combinados con `&` | Biblioteca, Aula 201, Laboratorio 3 |
| `/api/solicitantes/?rol=docente` | Filtro en `get_queryset()` | Carlos Medina |
| `/api/prestamos/?estado=activo` | Filtro en `get_queryset()` | PR-002, PR-001 |
| `/api/prestamos/activos/` | `@action` → `Prestamo.objects.activos()` | PR-002, PR-001 |
| `/api/prestamos/del-mes/?estado=activo` | `@action` → `del_mes()` combinado con `?estado=` | PR-002 (octubre 2026; PR-001 es de agosto) |

Las acciones llaman a `self.get_queryset()` y luego al método del QuerySet de la Semana 7, por eso respetan el filtro `?estado=` y la optimización de consultas. `del-mes` usa el mes actual: si la base no tiene un préstamo de este mes, crea uno en el Admin.

---

## Qué resuelve la API frente a los Templates y al Admin, y qué le falta

Los Templates sirven a una persona que navega el sitio y el Admin sirve al personal interno que administra datos; los dos devuelven HTML y solo se usan desde el navegador. La API expone los mismos modelos, con las mismas reglas y los mismos QuerySets, como JSON con códigos HTTP estándar, de modo que cualquier cliente (una app móvil, React en la Semana 9, otro sistema) puede leer y escribir sin depender de nuestras pantallas. Las validaciones viven en el serializer y se aplican igual a cualquier cliente. Todavía le falta: autenticación y permisos (hoy cualquiera puede escribir), paginación para listas grandes, CORS para que un frontend en otro puerto pueda consumirla, y que las operaciones con `transaction.atomic()` de la Semana 7 (asignar accesorio, autorizar espacio) también estén disponibles como endpoints.

---

## Implementado y probado

**Implementado en el código**

- DRF instalado, `'rest_framework'` en `INSTALLED_APPS` y `requirements.txt` actualizado.
- Seis recursos con `ModelSerializer`: `Accesorio`, `Equipo`, `Categoria`, `Espacio`, `Solicitante` y `Prestamo` (más los serializers anidados de ficha, mantenimiento, asignación, perfil, autorización y detalle).
- Validaciones propias: `AccesorioSerializer.validate_nombre` y `EspacioSerializer.validate_aforo`.
- Vistas genéricas (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) y su reemplazo por `ModelViewSet` con `DefaultRouter`.
- Recursos de solo lectura anidados y optimizados: `Equipo`, `Solicitante` y `Prestamo`.
- `SearchFilter` y `OrderingFilter` en accesorios y espacios; `?estado=` en equipos y préstamos; `?rol=` en solicitantes; acciones `disponibles`, `activos` y `del-mes`.

**Probado**

- `python manage.py test`: 34 pruebas en verde (21 de semanas anteriores y 13 nuevas de la API). Cubren 200, 201, 400, 404, 204 y 405, la búsqueda, el ordenamiento, los filtros, las acciones y el número de consultas con `assertNumQueries`. Las pruebas corren en una base temporal y no tocan `db.sqlite3`.
- Shell: serialización con y sin `many=True`, `is_valid()`, `validated_data`, `errors` y `save()`.
- Mediciones de consultas de la tabla de arriba, sobre `db.sqlite3`.
- Navegador: la API navegable de DRF carga en `/api/`, `/api/accesorios/` y `/api/genericas/accesorios/`.

---

## Cómo correrlo

```bash
cd Semana_08/django_proyect
python -m venv venv
venv\Scripts\activate
pip install -r src/requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

`migrate` no aplica nada nuevo si la base viene de la Semana 07: esta semana no cambia modelos.

| Pantalla | URL |
|---|---|
| Raíz de la API | http://127.0.0.1:8000/api/ |
| Accesorios (CRUD) | http://127.0.0.1:8000/api/accesorios/ |
| Equipos (solo lectura) | http://127.0.0.1:8000/api/equipos/ |
| Espacios (CRUD) | http://127.0.0.1:8000/api/espacios/ |
| Solicitantes (solo lectura) | http://127.0.0.1:8000/api/solicitantes/ |
| Préstamos (solo lectura) | http://127.0.0.1:8000/api/prestamos/ |
| Vistas genéricas del ejercicio 4 | http://127.0.0.1:8000/api/genericas/accesorios/ |
| Sitio con Templates | http://127.0.0.1:8000/equipos/ |
| Admin | http://127.0.0.1:8000/admin/ |
