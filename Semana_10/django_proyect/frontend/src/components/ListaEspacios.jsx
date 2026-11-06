import { useState } from 'react'
import EspacioCard from './EspacioCard.jsx'
import Tarjeta from './Tarjeta.jsx'

export default function ListaEspacios({ espacios }) {
  const [lista, setLista] = useState(espacios)
  const [busqueda, setBusqueda] = useState('')
  const [nombre, setNombre] = useState('')
  const [edificio, setEdificio] = useState('')
  const [piso, setPiso] = useState('')
  const [aforo, setAforo] = useState('')
  const [cupos, setCupos] = useState('')
  const [error, setError] = useState('')

  const totalCupos = lista.reduce((suma, item) => suma + item.cupos_disponibles, 0)
  const consulta = busqueda.trim().toLowerCase()
  const visibles = lista.filter((item) => item.nombre.toLowerCase().includes(consulta))

  function agregar(event) {
    event.preventDefault()
    const limpio = nombre.trim()
    if (limpio.length < 3) {
      setError('El nombre del espacio debe tener al menos 3 caracteres.')
      return
    }
    const personas = Number(aforo)
    if (!Number.isInteger(personas) || personas < 1) {
      setError('El aforo debe ser de al menos una persona.')
      return
    }
    const libres = cupos.trim() === '' ? 0 : Number(cupos)
    if (!Number.isInteger(libres) || libres < 0) {
      setError('Los cupos disponibles deben ser un entero mayor o igual que cero.')
      return
    }
    const siguienteId = lista.length === 0 ? 1 : Math.max(...lista.map((item) => item.id)) + 1
    const nuevo = {
      id: siguienteId,
      nombre: limpio,
      aforo: personas,
      cupos_disponibles: libres,
    }
    if (edificio.trim()) {
      nuevo.edificio = edificio.trim()
    }
    if (piso.trim()) {
      nuevo.piso = piso.trim()
    }
    setLista([...lista, nuevo])
    setNombre('')
    setEdificio('')
    setPiso('')
    setAforo('')
    setCupos('')
    setError('')
  }

  return (
    <section className="bloque" id="espacios">
      <h3>Espacios ({totalCupos} cupos libres en total)</h3>
      <div id="panel-espacios">
        <label className="etiqueta-campo" htmlFor="buscar-espacio">
          Buscar espacio
          <input
            id="buscar-espacio"
            className="buscador"
            value={busqueda}
            onChange={(event) => setBusqueda(event.target.value)}
            placeholder="Nombre del espacio"
            autoComplete="off"
          />
        </label>
        <div id="resultado-espacios">
          {lista.length === 0 ? (
            <p className="vacio">No hay espacios registrados</p>
          ) : visibles.length === 0 ? (
            <p className="vacio">Ningún espacio coincide con «{busqueda.trim()}».</p>
          ) : (
            <ul className="lista">
              {visibles.map((espacio) => (
                <EspacioCard
                  key={espacio.id}
                  nombre={espacio.nombre}
                  edificio={espacio.edificio}
                  piso={espacio.piso}
                  aforo={espacio.aforo}
                  cuposDisponibles={espacio.cupos_disponibles}
                />
              ))}
            </ul>
          )}
        </div>
      </div>
      <div id="form-espacio">
        <Tarjeta titulo="Nuevo espacio">
          <form className="formulario" onSubmit={agregar} noValidate>
            <label className="etiqueta-campo" htmlFor="espacio-nombre">
              Nombre
              <input
                id="espacio-nombre"
                className="buscador"
                value={nombre}
                onChange={(event) => setNombre(event.target.value)}
                autoComplete="off"
              />
            </label>
            <label className="etiqueta-campo" htmlFor="espacio-edificio">
              Edificio (vacío usa el valor por defecto «Sin edificio»)
              <input
                id="espacio-edificio"
                className="buscador"
                value={edificio}
                onChange={(event) => setEdificio(event.target.value)}
                autoComplete="off"
              />
            </label>
            <label className="etiqueta-campo" htmlFor="espacio-piso">
              Piso (vacío usa el valor por defecto «s/n»)
              <input
                id="espacio-piso"
                className="buscador"
                value={piso}
                onChange={(event) => setPiso(event.target.value)}
                autoComplete="off"
              />
            </label>
            <label className="etiqueta-campo" htmlFor="espacio-aforo">
              Aforo
              <input
                id="espacio-aforo"
                className="buscador"
                type="number"
                value={aforo}
                onChange={(event) => setAforo(event.target.value)}
              />
            </label>
            <label className="etiqueta-campo" htmlFor="espacio-cupos">
              Cupos disponibles
              <input
                id="espacio-cupos"
                className="buscador"
                type="number"
                value={cupos}
                onChange={(event) => setCupos(event.target.value)}
              />
            </label>
            {error ? <p className="error">{error}</p> : null}
            <button className="boton" type="submit">
              Agregar espacio
            </button>
          </form>
        </Tarjeta>
      </div>
    </section>
  )
}
