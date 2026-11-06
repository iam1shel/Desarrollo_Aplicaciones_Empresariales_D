import { useState } from 'react'
import AccesorioCard from './AccesorioCard.jsx'
import Tarjeta from './Tarjeta.jsx'

export default function ListaAccesorios({ accesorios }) {
  const [lista, setLista] = useState(accesorios)
  const [busqueda, setBusqueda] = useState('')
  const [nombre, setNombre] = useState('')
  const [tipo, setTipo] = useState('')
  const [existencias, setExistencias] = useState('')
  const [error, setError] = useState('')

  const totalExistencias = lista.reduce((suma, item) => suma + item.existencias, 0)
  const consulta = busqueda.trim().toLowerCase()
  const visibles = lista.filter((item) => item.nombre.toLowerCase().includes(consulta))

  function agregar(event) {
    event.preventDefault()
    const limpio = nombre.trim()
    if (limpio.length < 3) {
      setError('El nombre del accesorio debe tener al menos 3 caracteres.')
      return
    }
    const repetido = lista.some((item) => item.nombre.toLowerCase() === limpio.toLowerCase())
    if (repetido) {
      setError('Ya existe un accesorio con ese nombre; sus existencias se llevan en un solo registro.')
      return
    }
    const unidades = Number(existencias)
    if (!Number.isInteger(unidades) || unidades < 0) {
      setError('Las existencias deben ser un entero mayor o igual que cero.')
      return
    }
    const siguienteId = lista.length === 0 ? 1 : Math.max(...lista.map((item) => item.id)) + 1
    const nuevo = { id: siguienteId, nombre: limpio, existencias: unidades }
    if (tipo.trim()) {
      nuevo.tipo = tipo.trim()
    }
    setLista([...lista, nuevo])
    setNombre('')
    setTipo('')
    setExistencias('')
    setError('')
  }

  return (
    <section className="bloque" id="accesorios">
      <h3>Accesorios en almacén ({totalExistencias} unidades)</h3>
      <div id="panel-accesorios">
        <label className="etiqueta-campo" htmlFor="buscar-accesorio">
          Buscar accesorio
          <input
            id="buscar-accesorio"
            className="buscador"
            value={busqueda}
            onChange={(event) => setBusqueda(event.target.value)}
            placeholder="Nombre del accesorio"
            autoComplete="off"
          />
        </label>
        <div id="resultado-accesorios">
          {lista.length === 0 ? (
            <p className="vacio">No hay registros</p>
          ) : visibles.length === 0 ? (
            <p className="vacio">Ningún accesorio coincide con «{busqueda.trim()}».</p>
          ) : (
            <ul className="lista">
              {visibles.map((accesorio) => (
                <AccesorioCard
                  key={accesorio.id}
                  nombre={accesorio.nombre}
                  tipo={accesorio.tipo}
                  existencias={accesorio.existencias}
                  totalExistencias={totalExistencias}
                />
              ))}
            </ul>
          )}
        </div>
      </div>
      <div id="form-accesorio">
        <Tarjeta titulo="Nuevo accesorio">
          <form className="formulario" onSubmit={agregar} noValidate>
            <label className="etiqueta-campo" htmlFor="accesorio-nombre">
              Nombre
              <input
                id="accesorio-nombre"
                className="buscador"
                value={nombre}
                onChange={(event) => setNombre(event.target.value)}
                autoComplete="off"
              />
            </label>
            <label className="etiqueta-campo" htmlFor="accesorio-tipo">
              Tipo (vacío usa el valor por defecto «General»)
              <input
                id="accesorio-tipo"
                className="buscador"
                value={tipo}
                onChange={(event) => setTipo(event.target.value)}
                autoComplete="off"
              />
            </label>
            <label className="etiqueta-campo" htmlFor="accesorio-existencias">
              Existencias
              <input
                id="accesorio-existencias"
                className="buscador"
                type="number"
                value={existencias}
                onChange={(event) => setExistencias(event.target.value)}
              />
            </label>
            {error ? <p className="error">{error}</p> : null}
            <button className="boton" type="submit">
              Agregar accesorio
            </button>
          </form>
        </Tarjeta>
      </div>
    </section>
  )
}
