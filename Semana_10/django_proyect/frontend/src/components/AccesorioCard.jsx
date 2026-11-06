import { useState } from 'react'

export default function AccesorioCard({
  nombre,
  tipo = 'General',
  existencias,
  totalExistencias = 0,
}) {
  const [reservas, setReservas] = useState(0)
  const sinStock = reservas >= existencias
  const porcentaje = totalExistencias === 0 ? 0 : (existencias / totalExistencias) * 100

  return (
    <li className="tarjeta">
      <div className="titulo">
        <strong>{nombre}</strong>
        <span className="etiqueta">{tipo}</span>
      </div>
      <span className={existencias === 0 ? 'estado agotado' : 'estado'}>
        {existencias === 0 ? 'Agotado' : `Existencias: ${existencias}`}
      </span>
      {existencias > 0 && existencias <= 2 && <span className="aviso">¡Últimas unidades!</span>}
      <small>{porcentaje.toFixed(2)} % del stock</small>
      <div className="acciones">
        <button type="button" className="boton" disabled={sinStock} onClick={() => setReservas(reservas + 1)}>
          {sinStock ? 'Sin stock' : 'Reservar'}
        </button>
        {reservas > 0 && <span className="contador">Reservas: {reservas}</span>}
      </div>
    </li>
  )
}
