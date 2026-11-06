export default function Tarjeta({ titulo, children }) {
  return (
    <article className="tarjeta">
      {titulo ? (
        <div className="titulo">
          <strong>{titulo}</strong>
        </div>
      ) : null}
      {children}
    </article>
  )
}
