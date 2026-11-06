import AsignacionItem from './AsignacionItem.jsx'
import Tarjeta from './Tarjeta.jsx'

export default function EquipoCard({
  nombre,
  marca,
  ubicacion,
  estado,
  estadoDisplay,
  asignaciones = [],
}) {
  const enUso = asignaciones
    .filter((asignacion) => asignacion.estado === 'vigente')
    .reduce((suma, asignacion) => suma + asignacion.cantidad, 0)

  return (
    <Tarjeta titulo={nombre}>
      <span className="estado" style={{ color: estado === 'disponible' ? '#15803d' : '#b45309' }}>
        {estadoDisplay}
      </span>
      <p className="detalle">
        {marca} · {ubicacion}
      </p>
      {asignaciones.length === 0 ? (
        <p className="vacio">Sin accesorios asignados</p>
      ) : (
        <ul className="anidada">
          {asignaciones.map((asignacion) => (
            <AsignacionItem
              key={asignacion.id}
              cantidad={asignacion.cantidad}
              nombreAccesorio={asignacion.accesorio}
              estado={asignacion.estado}
            />
          ))}
        </ul>
      )}
      <p className="total">
        Total en uso: {enUso} {enUso === 1 ? 'unidad' : 'unidades'}
      </p>
    </Tarjeta>
  )
}
