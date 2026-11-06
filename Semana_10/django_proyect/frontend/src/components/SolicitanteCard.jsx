import AutorizacionItem from './AutorizacionItem.jsx'
import Tarjeta from './Tarjeta.jsx'

export default function SolicitanteCard({ nombre, codigo, rolDisplay, perfil = null, autorizaciones = [] }) {
  const vigentes = autorizaciones.filter((autorizacion) => autorizacion.estado === 'vigente').length
  const area = perfil ? perfil.area_o_ciclo : 'Sin perfil registrado'

  return (
    <Tarjeta titulo={nombre}>
      <span className="etiqueta">
        {rolDisplay} · {codigo}
      </span>
      <p className="detalle">{area}</p>
      {autorizaciones.length === 0 ? (
        <p className="vacio">Sin autorizaciones</p>
      ) : (
        <ul className="anidada">
          {autorizaciones.map((autorizacion) => (
            <AutorizacionItem
              key={autorizacion.id}
              espacio={autorizacion.espacio}
              edificio={autorizacion.edificio}
              fechaInicio={autorizacion.fecha_inicio}
              fechaFin={autorizacion.fecha_fin}
              estado={autorizacion.estado}
            />
          ))}
        </ul>
      )}
      <p className="total">
        {vigentes} de {autorizaciones.length} autorizaciones vigentes
      </p>
    </Tarjeta>
  )
}
