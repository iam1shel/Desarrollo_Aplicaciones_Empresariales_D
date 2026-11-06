export default function AsignacionItem({ cantidad, nombreAccesorio, estado }) {
  return (
    <li>
      {cantidad} × {nombreAccesorio} <em>({estado})</em>
    </li>
  )
}
