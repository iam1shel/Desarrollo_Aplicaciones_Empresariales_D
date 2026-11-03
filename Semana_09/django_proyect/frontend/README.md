# Frontend — Préstamo de equipos (React + Vite, Laboratorio 09)

Interfaz de una sola página hecha con React 19 y Vite 8. Muestra los datos de la aplicación de préstamo de equipos
(Semanas 4 a 8) y de la investigación propia (espacios y autorizaciones). Los datos están escritos a mano en
`src/App.jsx`, con la misma forma que las respuestas JSON de la API de la Semana 8. Todavía no se consume la API:
eso se hace en la Semana 12.

## Requisitos

- Node.js LTS (incluye npm). Probado con Node.js v26.13.0 y npm 11.20.0.

## Instalar y ejecutar

```bash
cd Semana_09/django_proyect/frontend
npm install        # crea node_modules a partir de package.json y package-lock.json
npm run dev        # servidor de desarrollo en http://localhost:5173/
```

Otros comandos:

| Comando | Qué hace |
|---|---|
| `npm run lint` | Revisa el código con oxlint |
| `npm run build` | Genera la versión de producción en `dist/` |
| `npm run preview` | Sirve la carpeta `dist/` para revisarla |

`node_modules/` y `dist/` no se suben al repositorio (están en `.gitignore`): se regeneran con `npm install` y `npm run build`.

## Qué muestra la interfaz

| Sección | Arreglo en `App.jsx` | Forma tomada de | Qué se practica |
|---|---|---|---|
| Cabecera | `nombreApp`, `semana`, cálculos sobre `equipos` | — | Expresiones entre llaves: variable, `padStart()` y `toFixed(2)` |
| Accesorios en almacén | `accesorios` (5 registros) | `GET /api/accesorios/` | `map()` con `key={accesorio.id}`, ternario «Agotado / Existencias: n», `&&` «¡Últimas unidades!» y mensaje «No hay registros» |
| Equipos y sus accesorios asignados | `equipos` con `asignaciones_accesorio` | `GET /api/equipos/` | `map()` dentro de otro `map()` y total de unidades en uso por equipo |
| Espacios | `espacios` (5 registros) | `GET /api/espacios/` | Ternario «Sin cupos / Cupos: n de aforo», `&&` «¡Últimos cupos!», barra de ocupación con `style={{ width }}` y mensaje de lista vacía |
| Solicitantes y espacios autorizados | `solicitantes` con `autorizaciones` | `GET /api/solicitantes/` | Lista anidada del modelo intermedio `AutorizacionEspacio` y conteo de autorizaciones vigentes |

Los estilos están en `src/App.css` (clases con `className`); `src/index.css` quedó vacío a propósito.

## Estructura

```text
frontend/
├── index.html        # la única página; tiene el <div id="root">
├── package.json      # dependencias y scripts (dev, build, lint, preview)
├── package-lock.json # versiones exactas instaladas
├── vite.config.js    # configuración de Vite con el plugin de React
├── public/           # archivos servidos tal cual (favicon.svg)
└── src/
    ├── main.jsx      # monta <App /> dentro de #root
    ├── App.jsx       # componente principal: datos y JSX
    ├── App.css       # estilos propios
    └── index.css     # vacío
```
