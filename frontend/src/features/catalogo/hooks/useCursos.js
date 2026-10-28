import { useState, useEffect, useCallback } from 'react'

export function useCursos({ initialPage = 1, initialFilter = '' } = {}) {
  const [cursos, setCursos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [page, setPageState] = useState(initialPage)
  const [filter, setFilterState] = useState(initialFilter)

  const fetchCursos = useCallback(async (p, f) => {
    setLoading(true)
    setError(null)
    try {
      const query = new URLSearchParams()
      if (p) query.set('page', p)
      if (f) query.set('q', f)
      const queryString = query.toString()
      const url = queryString ? `/api/cursos?${queryString}` : '/api/cursos'

      const res = await fetch(url)
      if (!res.ok) {
        throw new Error('Error al conectar con la API de cursos')
      }
      const data = await res.json()
      setCursos(Array.isArray(data) ? data : (data.items || []))
    } catch (err) {
      setError(err.message || 'Error de red')
      setCursos([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchCursos(page, filter)
  }, [page, filter, fetchCursos])

  const setPage = useCallback((newPage) => {
    setPageState(newPage)
  }, [])

  const setFilter = useCallback((newFilter) => {
    setFilterState(newFilter)
    setPageState(1) // Resetea a 1 si cambia el filtro
  }, [])

  const refetch = useCallback(() => {
    return fetchCursos(page, filter)
  }, [fetchCursos, page, filter])

  return {
    cursos,
    loading,
    error,
    page,
    setPage,
    filter,
    setFilter,
    refetch,
  }
}
