import EquipoCard from './EquipoCard.jsx'

export default function ListaEquipos({ equipos }) {
  return (
    <section className="bloque" id="equipos">
      <h3>Equipos y sus accesorios asignados</h3>
      {equipos.length === 0 ? (
        <p className="vacio">No hay equipos registrados</p>
      ) : (
        <div className="rejilla">
          {equipos.map((equipo) => (
            <EquipoCard
              key={equipo.id}
              nombre={equipo.nombre}
              marca={equipo.marca}
              ubicacion={equipo.ubicacion}
              estado={equipo.estado}
              estadoDisplay={equipo.estado_display}
              asignaciones={equipo.asignaciones_accesorio}
            />
          ))}
        </div>
      )}
    </section>
  )
}
