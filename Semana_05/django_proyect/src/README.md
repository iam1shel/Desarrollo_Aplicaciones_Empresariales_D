# Préstamo de equipos — Django Admin (Laboratorio 05)

Laboratorio Semana 05. Desarrollo de Aplicaciones Empresariales (sección D).

- **Project:** `config`
- **Apps:** `core`, `equipment` y `prestamos`
- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D

Esta semana **no se crean modelos nuevos**. Se recupera la aplicación de
Semana 04 y se administra desde `/admin/` con `ModelAdmin` e inlines.

Flujo del Admin:

Navegador → `/admin/` → autenticación (superusuario) → ModelAdmin → Model → ORM → SQLite

---

## Laboratorio 05 - Django Admin

**Objetivo.** Recuperar la aplicación de Semana 04 y administrar sus modelos
desde `/admin/`, sin crear modelos nuevos ni vistas CRUD propias para el panel.

### Modelos registrados

En `prestamos/admin.py` (investigación propia, 7 entidades):

- `Categoria`
- `Espacio`
- `Solicitante`
- `Prestamo`
- `DetallePrestamo`
- `PerfilSolicitante`
- `AutorizacionEspacio`

También están registrados `Equipo`, `FichaTecnica`, `Mantenimiento`,
`Accesorio` y `AsignacionAccesorio` (`equipment/admin.py`) e `Item`
(`core/admin.py`, con `admin.site.register(Item)`).

### ModelAdmin utilizados

| Clase | Modelo |
|---|---|
| `CategoriaAdmin` | `Categoria` |
| `EspacioAdmin` | `Espacio` |
| `SolicitanteAdmin` | `Solicitante` |
| `PrestamoAdmin` | `Prestamo` |
| `DetallePrestamoAdmin` | `DetallePrestamo` |
| `PerfilSolicitanteAdmin` | `PerfilSolicitante` |
| `AutorizacionEspacioAdmin` | `AutorizacionEspacio` |
| `EquipoAdmin` | `Equipo` |
| `FichaTecnicaAdmin` | `FichaTecnica` |
| `MantenimientoAdmin` | `Mantenimiento` |
| `AccesorioAdmin` | `Accesorio` |
| `AsignacionAccesorioAdmin` | `AsignacionAccesorio` |

### `list_display`

- `CategoriaAdmin`: `id`, `nombre`
- `EspacioAdmin`: `id`, `nombre`, `edificio`, `piso`, `aforo`
- `SolicitanteAdmin`: `id`, `nombre`, `codigo`, `rol`, `correo`
- `PrestamoAdmin`: `codigo`, `nombre_solicitante`, `fecha_prestamo`, `fecha_estimada_devolucion`, `estado`
- `DetallePrestamoAdmin`: `id`, `prestamo`, `nombre_equipo`, `cantidad`
- `PerfilSolicitanteAdmin`: `solicitante`, `documento_identidad`, `telefono`, `area_o_ciclo`
- `AutorizacionEspacioAdmin`: `solicitante`, `espacio`, `fecha_inicio`, `fecha_fin`, `estado`
- `EquipoAdmin`: `id`, `nombre`, `tipo`, `marca`, `ubicacion`, `estado`, `prestado_a`
- `FichaTecnicaAdmin`: `equipo`, `numero_serie`, `fecha_adquisicion`, `garantia_hasta`
- `MantenimientoAdmin`: `equipo`, `fecha`, `tipo`, `tecnico`
- `AccesorioAdmin`: `nombre`, `tipo`
- `AsignacionAccesorioAdmin`: `equipo`, `accesorio`, `cantidad`, `fecha_asignacion`, `estado`

### `search_fields`

- `CategoriaAdmin`: `nombre`
- `EspacioAdmin`: `nombre`, `edificio`
- `SolicitanteAdmin`: `nombre`, `codigo`
- `PrestamoAdmin`: `codigo`, `nombre_solicitante`
- `DetallePrestamoAdmin`: `nombre_equipo`, `prestamo__codigo`
- `PerfilSolicitanteAdmin`: `solicitante__nombre`, `documento_identidad`
- `EquipoAdmin`: `nombre`, `marca`, `prestado_a`
- `AccesorioAdmin`: `nombre`, `tipo`

### `list_filter`

- `SolicitanteAdmin`: `rol`
- `PrestamoAdmin`: `estado`
- `AutorizacionEspacioAdmin`: `estado`
- `EquipoAdmin`: `estado`, `tipo`
- `MantenimientoAdmin`: `tipo`
- `AsignacionAccesorioAdmin`: `estado`

### Inlines

- `PerfilSolicitanteInline` (`StackedInline`) en `SolicitanteAdmin`: edita el
  OneToOne `PerfilSolicitante` en bloques, dentro del solicitante.
- `AutorizacionEspacioInline` (`TabularInline`, `fk_name = "solicitante"`) en
  `SolicitanteAdmin`: edita el modelo intermedio `AutorizacionEspacio` en tabla
  (ManyToMany con `through`).
- También: `DetallePrestamoInline` en `PrestamoAdmin`; `FichaTecnicaInline`,
  `MantenimientoInline` y `AsignacionAccesorioInline` en `EquipoAdmin`.

Django Admin permite crear, buscar, filtrar y editar datos relacionados
(perfil 1:1 y autorizaciones N:M) **sin programar vistas propias** para el
panel: se configura en `admin.py` sobre los mismos modelos de Semana 04.

---

## PARTE 1 — Recuperar Semana 04 y entrar al Admin

### Ejercicio 1 — Recuperar la aplicación

Misma problemática: préstamo de equipos en una institución educativa.

| Pieza | Qué se reutiliza de Semana 04 |
|---|---|
| Entidad principal `prestamos` | `Solicitante` |
| Entidad principal `equipment` | `Equipo` |
| Relación 1:1 | `PerfilSolicitante` / `FichaTecnica` |
| Relación 1:N | `DetallePrestamo` / `Mantenimiento` |
| Relación N:M + through | `AutorizacionEspacio` / `AsignacionAccesorio` |

### Ejercicio 2 — Superusuario

```bash
python manage.py createsuperuser
```

Con un superusuario se entra a `http://127.0.0.1:8000/admin/`.
Sin él, Django Admin no deja gestionar los modelos.

### Ejercicio 3 — Registrar modelos

Los modelos de `prestamos` y `equipment` se registran en cada `admin.py`
con `@admin.register(...)`. Las 7 entidades de la investigación propia son:

1. `Categoria`
2. `Espacio`
3. `Solicitante`
4. `Prestamo`
5. `DetallePrestamo`
6. `PerfilSolicitante`
7. `AutorizacionEspacio`

---

## PARTE 2 — ModelAdmin, columnas, búsqueda y filtros

### Ejercicio 4 — ModelAdmin

`ModelAdmin` es la clase que le dice a Django **cómo** mostrar un modelo
en el panel: columnas, buscador, filtros e inlines.

Hay ModelAdmin (entre otros) en:

- `SolicitanteAdmin`
- `PrestamoAdmin`
- `EquipoAdmin`

### Ejercicio 5 — `list_display`

Define las columnas de la lista. Ejemplo: en `SolicitanteAdmin`
se ven `nombre`, `codigo`, `rol` y `correo` sin entrar al detalle.

### Ejercicio 6 — `search_fields`

Activa la caja de búsqueda. Ejemplo: buscar un solicitante por nombre o código.

### Ejercicio 7 — `list_filter`

Activa el filtro de la derecha. Ejemplo: filtrar solicitantes por `rol`
o préstamos por `estado`.

---

## PARTE 3 — Inlines (administrar relaciones desde la entidad principal)

### Ejercicio 8 — StackedInline (OneToOne)

`PerfilSolicitanteInline` se muestra al editar un `Solicitante`.
Como la relación es 1:1, el formulario va **en bloques** (StackedInline).

Equivalente en `equipment`: `FichaTecnicaInline` dentro de `Equipo`.

### Ejercicio 9 — TabularInline (modelo intermedio N:M)

`AutorizacionEspacioInline` muestra el through `AutorizacionEspacio`
en **tabla**. `fk_name = "solicitante"` es necesario porque ese modelo
tiene dos ForeignKey.

Equivalente en `equipment`: `AsignacionAccesorioInline` dentro de `Equipo`.

Así se administran perfil y autorizaciones **desde el solicitante**,
sin saltar a otra pantalla.

---

## Cómo correrlo

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

| Pantalla | URL |
|---|---|
| Login Admin | `http://127.0.0.1:8000/admin/login/` |
| Índice Admin | `http://127.0.0.1:8000/admin/` |
| Solicitantes (inlines 1:1 y N:M) | `http://127.0.0.1:8000/admin/prestamos/solicitante/` |
| Equipos (inlines 1:1, 1:N y N:M) | `http://127.0.0.1:8000/admin/equipment/equipo/` |
| App pública de préstamos | `http://127.0.0.1:8000/prestamos/` |

---

## Evidencia por integrante

### Mishel Rojas

- **Nombre:** Mishel Rojas
- **Título:** Django Admin sobre los modelos de Semana 04
- **Qué hizo:** Superusuario; registro de las 7 entidades de `prestamos`;
  ModelAdmin con `list_display`, `search_fields` y `list_filter`;
  StackedInline del OneToOne y TabularInline del through.
- **Código:** `src/prestamos/admin.py` y `src/equipment/admin.py`
- **Explicación:** El Admin no reemplaza al Model. Solo ofrece una interfaz
  para crear, buscar, filtrar y editar relaciones (inlines) sobre los
  mismos modelos de Semana 04.

---

## Conclusiones

1. Django Admin es un panel automático para el Model; hay que registrar cada modelo.
2. `ModelAdmin` personaliza listas, búsqueda, filtros e inlines.
3. `StackedInline` encaja en relaciones 1:1 (un bloque por objeto relacionado).
4. `TabularInline` encaja en 1:N y en el modelo `through` de un N:M.
5. Un Inline permite editar la relación **dentro** de la entidad principal.
