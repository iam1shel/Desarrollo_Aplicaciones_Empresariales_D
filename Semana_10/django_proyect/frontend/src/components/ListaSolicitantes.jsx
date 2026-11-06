import SolicitanteCard from './SolicitanteCard.jsx'

export default function ListaSolicitantes({ solicitantes }) {
  return (
    <section className="bloque" id="solicitantes">
      <h3>Solicitantes y espacios autorizados</h3>
      {solicitantes.length === 0 ? (
        <p className="vacio">No hay solicitantes registrados</p>
      ) : (
        <div className="rejilla">
          {solicitantes.map((solicitante) => (
            <SolicitanteCard
              key={solicitante.id}
              nombre={solicitante.nombre}
              codigo={solicitante.codigo}
              rolDisplay={solicitante.rol_display}
              perfil={solicitante.perfil}
              autorizaciones={solicitante.autorizaciones}
            />
          ))}
        </div>
      )}
    </section>
  )
}
