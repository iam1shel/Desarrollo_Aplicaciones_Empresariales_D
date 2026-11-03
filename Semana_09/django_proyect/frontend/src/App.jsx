import './App.css'

const nombreApp = 'Préstamo de equipos'
const semana = 9

// Parte 1 — misma forma que GET /api/accesorios/ (Semana 8)
const accesorios = [
  { id: 5, nombre: 'Adaptador USB-C a HDMI', tipo: 'Video', existencias: 0 },
  { id: 2, nombre: 'Cable HDMI 2 m', tipo: 'Video', existencias: 5 },
  { id: 1, nombre: 'Cargador Lenovo 65W', tipo: 'Energía', existencias: 4 },
  { id: 3, nombre: 'Control Remoto', tipo: 'Control', existencias: 1 },
  { id: 4, nombre: 'Puntero láser', tipo: 'Presentación', existencias: 2 },
]

// Parte 1 — misma forma que GET /api/equipos/ (Semana 8)
const equipos = [
  {
    id: 1,
    nombre: 'Laptop 01',
    tipo: 'Laptop',
    marca: 'Lenovo',
    ubicacion: 'Biblioteca',
    estado: 'disponible',
    estado_display: 'Disponible',
    prestado_a: '',
    ficha: {
      numero_serie: 'LN-2026-001',
      fecha_adquisicion: '2025-03-10',
      garantia_hasta: '2027-03-10',
      especificaciones: '16 GB RAM, SSD 512 GB',
    },
    mantenimientos: [
      { id: 2, fecha: '2026-08-20', tipo: 'correctivo', tecnico: 'María Quispe', descripcion: 'Cambio de teclado' },
    ],
    asignaciones_accesorio: [
      { id: 4, accesorio: 'Cable HDMI 2 m', cantidad: 2, fecha_asignacion: '2026-09-30', estado: 'vigente' },
      { id: 1, accesorio: 'Cargador Lenovo 65W', cantidad: 1, fecha_asignacion: '2026-03-12', estado: 'vigente' },
    ],
  },
  {
    id: 2,
    nombre: 'Proyector 01',
    tipo: 'Proyector',
    marca: 'Epson',
    ubicacion: 'Aula 201',
    estado: 'prestado',
    estado_display: 'Prestado',
    prestado_a: '',
    ficha: {
      numero_serie: 'EP-201-088',
      fecha_adquisicion: '2024-08-01',
      garantia_hasta: '2026-08-01',
      especificaciones: '3800 lúmenes, HDMI',
    },
    mantenimientos: [],
    asignaciones_accesorio: [
      { id: 8, accesorio: 'Control Remoto', cantidad: 1, fecha_asignacion: '2026-09-30', estado: 'vigente' },
      { id: 2, accesorio: 'Cable HDMI 2 m', cantidad: 1, fecha_asignacion: '2026-08-01', estado: 'vigente' },
    ],
  },
  {
    id: 3,
    nombre: 'Mouse 01',
    tipo: 'Mouse',
    marca: 'Acer',
    ubicacion: 'Aula 1501',
    estado: 'prestado',
    estado_display: 'Prestado',
    prestado_a: '',
    ficha: null,
    mantenimientos: [],
    asignaciones_accesorio: [
      { id: 7, accesorio: 'Cable HDMI 2 m', cantidad: 1, fecha_asignacion: '2026-09-30', estado: 'perdido' },
    ],
  },
  {
    id: 4,
    nombre: 'Laptop 02',
    tipo: 'Laptop',
    marca: 'HP',
    ubicacion: 'Biblioteca',
    estado: 'disponible',
    estado_display: 'Disponible',
    prestado_a: '',
    ficha: null,
    mantenimientos: [],
    asignaciones_accesorio: [
      { id: 3, accesorio: 'Cargador Lenovo 65W', cantidad: 2, fecha_asignacion: '2026-09-30', estado: 'vigente' },
      { id: 5, accesorio: 'Cable HDMI 2 m', cantidad: 1, fecha_asignacion: '2026-09-30', estado: 'devuelto' },
    ],
  },
  {
    id: 5,
    nombre: 'Tablet 01',
    tipo: 'Tablet',
    marca: 'Honor',
    ubicacion: 'Aula 505',
    estado: 'prestado',
    estado_display: 'Prestado',
    prestado_a: '',
    ficha: null,
    mantenimientos: [],
    asignaciones_accesorio: [
      { id: 6, accesorio: 'Cable HDMI 2 m', cantidad: 1, fecha_asignacion: '2026-09-30', estado: 'vigente' },
    ],
  },
]

// Parte 2 — misma forma que GET /api/espacios/ (Semana 8)
const espacios = [
  { id: 5, nombre: 'Auditorio', edificio: 'Central', piso: '1', aforo: 150, cupos_disponibles: 3 },
  { id: 2, nombre: 'Aula 201', edificio: 'Ingeniería', piso: '2', aforo: 40, cupos_disponibles: 0 },
  { id: 1, nombre: 'Biblioteca', edificio: 'Central', piso: '1', aforo: 80, cupos_disponibles: 12 },
  { id: 3, nombre: 'Laboratorio 3', edificio: 'Cómputo', piso: '3', aforo: 25, cupos_disponibles: 2 },
  { id: 4, nombre: 'Sala 105', edificio: 'Central', piso: '1', aforo: 30, cupos_disponibles: 8 },
]

// Parte 2 — misma forma que GET /api/solicitantes/ (Semana 8)
const solicitantes = [
  {
    id: 1,
    nombre: 'Ana Torres',
    codigo: 'U20261234',
    rol: 'estudiante',
    rol_display: 'Estudiante',
    correo: 'ana.torres@universidad.edu',
    perfil: { documento_identidad: '71234567', telefono: '987654321', area_o_ciclo: 'Ciclo V — Computación' },
    autorizaciones: [
      { id: 4, espacio: 'Biblioteca', edificio: 'Central', fecha_inicio: '2026-10-01', fecha_fin: '2026-10-31', estado: 'vigente' },
      { id: 2, espacio: 'Laboratorio 3', edificio: 'Cómputo', fecha_inicio: '2026-08-01', fecha_fin: '2026-12-15', estado: 'vigente' },
      { id: 1, espacio: 'Biblioteca', edificio: 'Central', fecha_inicio: '2026-03-01', fecha_fin: '2026-12-15', estado: 'vigente' },
    ],
  },
  {
    id: 2,
    nombre: 'Carlos Medina',
    codigo: 'D1022',
    rol: 'docente',
    rol_display: 'Docente',
    correo: 'cmedina@universidad.edu',
    perfil: { documento_identidad: '40111222', telefono: '999111222', area_o_ciclo: 'Docente de Ingeniería' },
    autorizaciones: [
      { id: 3, espacio: 'Aula 201', edificio: 'Ingeniería', fecha_inicio: '2026-03-01', fecha_fin: '2026-07-31', estado: 'vencida' },
    ],
  },
  {
    id: 3,
    nombre: 'Lucía Ramos',
    codigo: 'U20265678',
    rol: 'estudiante',
    rol_display: 'Estudiante',
    correo: 'lucia.ramos@universidad.edu',
    perfil: null,
    autorizaciones: [],
  },
]

function App() {
  const disponibles = equipos.filter((equipo) => equipo.estado === 'disponible').length
  const porcentajeDisponibles = (disponibles / equipos.length) * 100
  const totalExistencias = accesorios.reduce((suma, accesorio) => suma + accesorio.existencias, 0)
  const totalCupos = espacios.reduce((suma, espacio) => suma + espacio.cupos_disponibles, 0)

  return (
    <main className="pagina">
      <header className="cabecera">
        <h1>{nombreApp}</h1>
        <p>
          Laboratorio {String(semana).padStart(2, '0')} · React + Vite · Semanas 4 a 8 e investigación propia
        </p>
        <p className="resumen">
          {disponibles} de {equipos.length} equipos disponibles ({porcentajeDisponibles.toFixed(2)} %)
        </p>
      </header>

      <h2 className="parte">Parte 1 — Equipos y accesorios (Semanas 4 a 8)</h2>

      <section className="bloque" id="accesorios">
        <h3>Accesorios en almacén ({totalExistencias} unidades)</h3>
        {accesorios.length === 0 ? (
          <p className="vacio">No hay registros</p>
        ) : (
          <ul className="lista">
            {accesorios.map((accesorio) => (
              <li key={accesorio.id} className="tarjeta">
                <div className="titulo">
                  <strong>{accesorio.nombre}</strong>
                  <span className="etiqueta">{accesorio.tipo}</span>
                </div>
                <span className={accesorio.existencias === 0 ? 'estado agotado' : 'estado'}>
                  {accesorio.existencias === 0 ? 'Agotado' : `Existencias: ${accesorio.existencias}`}
                </span>
                {accesorio.existencias > 0 && accesorio.existencias <= 2 && (
                  <span className="aviso">¡Últimas unidades!</span>
                )}
                <small>
                  {((accesorio.existencias / totalExistencias) * 100).toFixed(2)} % del stock
                </small>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="bloque" id="equipos">
        <h3>Equipos y sus accesorios asignados</h3>
        <div className="rejilla">
          {equipos.map((equipo) => {
            const enUso = equipo.asignaciones_accesorio
              .filter((asignacion) => asignacion.estado === 'vigente')
              .reduce((suma, asignacion) => suma + asignacion.cantidad, 0)
            return (
              <article key={equipo.id} className="tarjeta">
                <div className="titulo">
                  <strong>{equipo.nombre}</strong>
                  <span
                    className="estado"
                    style={{ color: equipo.estado === 'disponible' ? '#15803d' : '#b45309' }}
                  >
                    {equipo.estado_display}
                  </span>
                </div>
                <p className="detalle">
                  {equipo.marca} · {equipo.ubicacion}
                </p>
                <ul className="anidada">
                  {equipo.asignaciones_accesorio.map((asignacion) => (
                    <li key={asignacion.id}>
                      {asignacion.cantidad} × {asignacion.accesorio} <em>({asignacion.estado})</em>
                    </li>
                  ))}
                </ul>
                <p className="total">
                  Total en uso: {enUso} {enUso === 1 ? 'unidad' : 'unidades'}
                </p>
              </article>
            )
          })}
        </div>
      </section>

      <h2 className="parte">Parte 2 — Investigación propia: espacios y autorizaciones</h2>

      <section className="bloque" id="espacios">
        <h3>Espacios ({totalCupos} cupos libres en total)</h3>
        {espacios.length === 0 ? (
          <p className="vacio">No hay espacios registrados</p>
        ) : (
          <ul className="lista">
            {espacios.map((espacio) => {
              const ocupacion = ((espacio.aforo - espacio.cupos_disponibles) / espacio.aforo) * 100
              return (
                <li key={espacio.id} className="tarjeta">
                  <div className="titulo">
                    <strong>{espacio.nombre}</strong>
                    <span className="etiqueta">
                      {espacio.edificio} · piso {espacio.piso}
                    </span>
                  </div>
                  <span className={espacio.cupos_disponibles === 0 ? 'estado agotado' : 'estado'}>
                    {espacio.cupos_disponibles === 0
                      ? 'Sin cupos'
                      : `Cupos: ${espacio.cupos_disponibles} de ${espacio.aforo}`}
                  </span>
                  {espacio.cupos_disponibles > 0 && espacio.cupos_disponibles <= 3 && (
                    <span className="aviso">¡Últimos cupos!</span>
                  )}
                  <div className="barra">
                    <div className="barra-relleno" style={{ width: `${ocupacion}%` }} />
                  </div>
                  <small>Ocupación: {ocupacion.toFixed(1)} %</small>
                </li>
              )
            })}
          </ul>
        )}
      </section>

      <section className="bloque" id="solicitantes">
        <h3>Solicitantes y espacios autorizados</h3>
        {solicitantes.length === 0 ? (
          <p className="vacio">No hay solicitantes registrados</p>
        ) : (
          <div className="rejilla">
            {solicitantes.map((solicitante) => {
              const vigentes = solicitante.autorizaciones.filter(
                (autorizacion) => autorizacion.estado === 'vigente',
              ).length
              return (
                <article key={solicitante.id} className="tarjeta">
                  <div className="titulo">
                    <strong>{solicitante.nombre}</strong>
                    <span className="etiqueta">
                      {solicitante.rol_display} · {solicitante.codigo}
                    </span>
                  </div>
                  <p className="detalle">
                    {solicitante.perfil ? solicitante.perfil.area_o_ciclo : 'Sin perfil registrado'}
                  </p>
                  {solicitante.autorizaciones.length === 0 ? (
                    <p className="vacio">Sin autorizaciones</p>
                  ) : (
                    <ul className="anidada">
                      {solicitante.autorizaciones.map((autorizacion) => (
                        <li key={autorizacion.id}>
                          {autorizacion.espacio} ({autorizacion.edificio}) · {autorizacion.fecha_inicio} al{' '}
                          {autorizacion.fecha_fin} <em>({autorizacion.estado})</em>
                        </li>
                      ))}
                    </ul>
                  )}
                  <p className="total">
                    {vigentes} de {solicitante.autorizaciones.length} autorizaciones vigentes
                  </p>
                </article>
              )
            })}
          </div>
        )}
      </section>

      <footer className="pie">
        Datos escritos a mano con la forma de la API de la Semana 8. La conexión con la API llega en la Semana 12.
      </footer>
    </main>
  )
}

export default App
