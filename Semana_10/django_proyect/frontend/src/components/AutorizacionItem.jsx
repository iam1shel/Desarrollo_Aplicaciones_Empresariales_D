export default function AutorizacionItem({ espacio, edificio, fechaInicio, fechaFin, estado }) {
  return (
    <li>
      {espacio} ({edificio}) · {fechaInicio} al {fechaFin} <em>({estado})</em>
    </li>
  )
}
