import './App.css'
import { accesorios, equipos, espacios, solicitantes } from './datos.js'
import ListaAccesorios from './components/ListaAccesorios.jsx'
import ListaEquipos from './components/ListaEquipos.jsx'
import ListaEspacios from './components/ListaEspacios.jsx'
import ListaSolicitantes from './components/ListaSolicitantes.jsx'

const nombreApp = 'Préstamo de equipos'
const semana = 10

function App() {
  const disponibles = equipos.filter((equipo) => equipo.estado === 'disponible').length
  const porcentajeDisponibles = (disponibles / equipos.length) * 100

  return (
    <main className="pagina">
      <header className="cabecera">
        <h1>{nombreApp}</h1>
        <p>
          Laboratorio {String(semana).padStart(2, '0')} · React + Vite · Componentes, props, estado y eventos
        </p>
        <p className="resumen">
          {disponibles} de {equipos.length} equipos disponibles ({porcentajeDisponibles.toFixed(2)} %)
        </p>
      </header>

      <h2 className="parte">Parte 1 — Equipos y accesorios (Semanas 4 a 8)</h2>
      <ListaAccesorios accesorios={accesorios} />
      <ListaEquipos equipos={equipos} />

      <h2 className="parte">Parte 2 — Investigación propia: espacios y autorizaciones</h2>
      <ListaEspacios espacios={espacios} />
      <ListaSolicitantes solicitantes={solicitantes} />

      <footer className="pie">
        Los datos siguen escritos a mano, con la forma de la API de la Semana 8. Las reservas, las búsquedas y los
        registros nuevos viven en el estado del navegador y se pierden al recargar. Guardarlos en la base de Django
        corresponde a la Semana 12.
      </footer>
    </main>
  )
}

export default App
