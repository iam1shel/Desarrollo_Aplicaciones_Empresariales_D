# Préstamo de equipos — Componentes y eventos (Laboratorio 10)

Laboratorio Semana 10. Desarrollo de Aplicaciones Empresariales (sección D).

- **Repositorio:** https://github.com/iam1shel/Desarrollo_Aplicaciones_Empresariales_D
- **Frontend:** [`frontend/`](frontend), la interfaz React de la Semana 9 reorganizada en componentes
- **Backend:** no cambia en esta semana. Sigue en [`../../Semana_09/django_proyect/src`](../../Semana_09/django_proyect/src), con la API REST bajo `/api/`
- **Capturas:** [`capturas/`](capturas)

Un componente recibe datos por props, guarda en `useState` lo que cambia con el usuario y responde a `onClick`, `onChange` y `onSubmit`. El estado y los eventos viven en el componente que los usa: esta semana no se pasan funciones de un componente a otro (eso es la Semana 11) y todavía no se llama a la API (Semana 12).

## Cómo correrlo

```bash
cd Semana_10/django_proyect/frontend
npm install
npm run dev
```

Abrir http://localhost:5173/. La descripción de cada componente está en [`frontend/README.md`](frontend/README.md).
