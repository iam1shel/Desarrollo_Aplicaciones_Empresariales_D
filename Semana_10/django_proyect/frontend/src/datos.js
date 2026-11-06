// Misma forma que las respuestas JSON de la API de la Semana 8.
// Los componentes reciben estos objetos y, cuando hace falta, traducen
// los nombres de la API a props en el map().

export const accesorios = [
  { id: 5, nombre: 'Adaptador USB-C a HDMI', tipo: 'Video', existencias: 0 },
  { id: 2, nombre: 'Cable HDMI 2 m', tipo: 'Video', existencias: 5 },
  { id: 1, nombre: 'Cargador Lenovo 65W', tipo: 'Energía', existencias: 4 },
  { id: 3, nombre: 'Control Remoto', tipo: 'Control', existencias: 1 },
  { id: 4, nombre: 'Puntero láser', tipo: 'Presentación', existencias: 2 },
]

export const equipos = [
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

export const espacios = [
  { id: 5, nombre: 'Auditorio', edificio: 'Central', piso: '1', aforo: 150, cupos_disponibles: 3 },
  { id: 2, nombre: 'Aula 201', edificio: 'Ingeniería', piso: '2', aforo: 40, cupos_disponibles: 0 },
  { id: 1, nombre: 'Biblioteca', edificio: 'Central', piso: '1', aforo: 80, cupos_disponibles: 12 },
  { id: 3, nombre: 'Laboratorio 3', edificio: 'Cómputo', piso: '3', aforo: 25, cupos_disponibles: 2 },
  { id: 4, nombre: 'Sala 105', edificio: 'Central', piso: '1', aforo: 30, cupos_disponibles: 8 },
]

export const solicitantes = [
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
