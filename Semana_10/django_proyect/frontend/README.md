# Frontend — Préstamo de equipos (React + Vite, Laboratorio 10)

La interfaz de la Semana 9, ahora repartida en componentes funcionales. Los datos siguen escritos a mano en `src/datos.js`, con la misma forma que el JSON de la API de la Semana 8. Cada componente recibe esos datos por props. Las reservas, las búsquedas y los formularios se guardan con `useState` dentro del componente que los dibuja.

Todavía no se consume la API (Semana 12) y no se pasan funciones entre componentes (Semana 11).

## Requisitos

- Node.js LTS (incluye npm).

## Instalar y ejecutar

```bash
cd Semana_10/django_proyect/frontend
npm install
npm run dev
```

Abrir http://localhost:5173/.

| Comando | Qué hace |
|---|---|
| `npm run lint` | Revisa el código con oxlint |
| `npm run build` | Genera la versión de producción en `dist/` |
| `npm run preview` | Sirve la carpeta `dist/` para revisarla |

`node_modules/` y `dist/` están en `.gitignore` y no se suben al repositorio.

## Componentes

| Archivo | Qué hace |
|---|---|
| `Tarjeta.jsx` | Contenedor. Recibe `titulo` y `children`, y envuelve un equipo, un solicitante o un formulario. |
| `AccesorioCard.jsx` | Un accesorio: nombre, tipo (por defecto «General»), existencias y el botón Reservar. El contador de reservas es estado local y el botón se desactiva al llegar a las existencias. |
| `ListaAccesorios.jsx` | Lista de accesorios con `map()` y `key`. Incluye el buscador controlado y el formulario que agrega un accesorio al estado. |
| `AsignacionItem.jsx` | Una fila de la relación 1:N: cantidad, nombre del accesorio y estado de la asignación. |
| `EquipoCard.jsx` | Un equipo dentro de `Tarjeta`. Recorre sus asignaciones con `AsignacionItem` y calcula el total en uso. |
| `ListaEquipos.jsx` | Arma la rejilla de equipos. Traduce `estado_display` y `asignaciones_accesorio` a props. |
| `EspacioCard.jsx` | Un espacio: cupos, barra de ocupación y el botón Apartar cupo, con contador propio. `edificio` vale «Sin edificio» y `piso` vale «s/n» si no llegan. |
| `ListaEspacios.jsx` | Lista de espacios, buscador y formulario. Valida el aforo con la regla de `EspacioSerializer` (al menos 1). |
| `AutorizacionItem.jsx` | Una autorización del modelo intermedio: espacio, edificio, fechas y estado. |
| `SolicitanteCard.jsx` | Un solicitante dentro de `Tarjeta`, con sus autorizaciones anidadas y el conteo de vigentes. |
| `ListaSolicitantes.jsx` | Arma la rejilla de solicitantes. Traduce `rol_display` a la prop `rolDisplay`. |

`App.jsx` solo compone esas listas y calcula el resumen de equipos disponibles.

## Estructura

```text
frontend/
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── public/
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    ├── datos.js
    ├── index.css
    └── components/
        ├── AccesorioCard.jsx
        ├── AsignacionItem.jsx
        ├── AutorizacionItem.jsx
        ├── EquipoCard.jsx
        ├── EspacioCard.jsx
        ├── ListaAccesorios.jsx
        ├── ListaEquipos.jsx
        ├── ListaEspacios.jsx
        ├── ListaSolicitantes.jsx
        ├── SolicitanteCard.jsx
        └── Tarjeta.jsx
```
