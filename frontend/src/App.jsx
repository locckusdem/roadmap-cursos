import { useCursos } from './features/catalogo/hooks/useCursos'

export default function App() {
  const { cursos, loading, error, page, setPage, filter, setFilter, refetch } = useCursos()

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Catálogo Comunitario de Cursos</h1>
      
      <div style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
        <input
          type="text"
          placeholder="Buscar cursos..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: '0.5rem', flex: 1, borderRadius: '4px', border: '1px solid #dadce0' }}
        />
        <button onClick={refetch} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
          Recargar
        </button>
      </div>

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

      <div style={{ marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Anterior</button>
        <span>Página {page}</span>
        <button onClick={() => setPage(page + 1)}>Siguiente</button>
      </div>
    </main>
  )
}
