import { useEffect, useState } from 'react'

export default function App() {
  const [cursos, setCursos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/cursos')
      .then(res => {
        if (!res.ok) throw new Error('Error al conectar con la API')
        return res.json()
      })
      .then(data => {
        setCursos(data)
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Catálogo Comunitario de Cursos</h1>
      
      {loading && <p>Cargando cursos disponibles...</p>}
      {error && <p style={{ color: '#d93025' }}>Error: {error}</p>}
      
      {!loading && !error && cursos.length === 0 && (
        <p>No hay cursos disponibles en el catálogo.</p>
      )}

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {cursos.map(c => (
          <li key={c.id} style={{ border: '1px solid #dadce0', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>
            <h3 style={{ margin: '0 0 0.5rem 0' }}>{c.title}</h3>
            <p style={{ margin: '0 0 0.5rem 0', color: '#5f6368' }}>Plataforma: {c.platform} | Nivel: {c.level}</p>
            <span style={{ background: '#e8f0fe', color: '#1a73e8', padding: '4px 8px', borderRadius: '4px', fontSize: '0.85rem' }}>
              {c.technology}
            </span>
          </li>
        ))}
      </ul>
    </main>
  )
}
