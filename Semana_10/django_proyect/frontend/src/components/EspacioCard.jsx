import { useState } from 'react'

export default function EspacioCard({
  nombre,
  edificio = 'Sin edificio',
  piso = 's/n',
  aforo,
  cuposDisponibles,
}) {
  const [apartados, setApartados] = useState(0)
  const sinCupos = apartados >= cuposDisponibles
  const ocupacion = aforo === 0 ? 0 : ((aforo - cuposDisponibles) / aforo) * 100
  const ancho = Math.min(100, Math.max(0, ocupacion))

  return (
    <li className="tarjeta">
      <div className="titulo">
        <strong>{nombre}</strong>
        <span className="etiqueta">
          {edificio} · piso {piso}
        </span>
      </div>
      <span className={cuposDisponibles === 0 ? 'estado agotado' : 'estado'}>
        {cuposDisponibles === 0 ? 'Sin cupos' : `Cupos: ${cuposDisponibles} de ${aforo}`}
      </span>
      {cuposDisponibles > 0 && cuposDisponibles <= 3 && <span className="aviso">¡Últimos cupos!</span>}
      <div className="barra">
        <div className="barra-relleno" style={{ width: `${ancho}%` }} />
      </div>
      <small>Ocupación: {ocupacion.toFixed(1)} %</small>
      <div className="acciones">
        <button type="button" className="boton" disabled={sinCupos} onClick={() => setApartados(apartados + 1)}>
          {sinCupos ? 'Sin cupos' : 'Apartar cupo'}
        </button>
        {apartados > 0 && <span className="contador">Apartados: {apartados}</span>}
      </div>
    </li>
  )
}
