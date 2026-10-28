import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { renderHook, act, waitFor } from '@testing-library/react'
import { useCursos } from './useCursos'

describe('useCursos Hook', () => {
  const mockCursos = [
    { id: 1, title: 'Curso de React', technology: 'Frontend' },
    { id: 2, title: 'Curso de FastAPI', technology: 'Backend' },
  ]

  beforeEach(() => {
    vi.restoreAllMocks()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  it('carga inicial: loading=true -> loading=false con datos', async () => {
    // Arrange
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockCursos,
    })

    // Act
    const { result } = renderHook(() => useCursos())

    // Assert inicial: loading true
    expect(result.current.loading).toBe(true)

    // Assert final: loading false con datos
    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })
    expect(result.current.cursos).toEqual(mockCursos)
    expect(result.current.error).toBeNull()
  })

  it('error de red: estado de error seteado, lista vacía', async () => {
    // Arrange
    globalThis.fetch = vi.fn().mockRejectedValue(new Error('Fallo de conexión'))

    // Act
    const { result } = renderHook(() => useCursos())

    // Assert
    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })
    expect(result.current.error).toBe('Fallo de conexión')
    expect(result.current.cursos).toEqual([])
  })

  it('setPage(n) -> recarga con page=n (y resetea a 1 si cambia el filtro)', async () => {
    // Arrange
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockCursos,
    })
    const { result } = renderHook(() => useCursos())
    await waitFor(() => expect(result.current.loading).toBe(false))

    // Act 1: Cambiar a página 3
    await act(async () => {
      result.current.setPage(3)
    })

    // Assert 1: page=3 y llamado a la API con page=3
    expect(result.current.page).toBe(3)
    expect(globalThis.fetch).toHaveBeenLastCalledWith(expect.stringContaining('page=3'))

    // Act 2: Cambiar filtro de búsqueda
    await act(async () => {
      result.current.setFilter('docker')
    })

    // Assert 2: Al cambiar filtro, debe resetear a página 1
    expect(result.current.page).toBe(1)
    expect(result.current.filter).toBe('docker')
    expect(globalThis.fetch).toHaveBeenLastCalledWith(expect.stringContaining('page=1'))
    expect(globalThis.fetch).toHaveBeenLastCalledWith(expect.stringContaining('q=docker'))
  })

  it('refetch() -> recarga con parámetros actuales', async () => {
    // Arrange
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockCursos,
    })
    const { result } = renderHook(() => useCursos({ initialPage: 2, initialFilter: 'python' }))
    await waitFor(() => expect(result.current.loading).toBe(false))
    expect(globalThis.fetch).toHaveBeenCalledTimes(1)

    // Act: Disparar refetch manual
    await act(async () => {
      await result.current.refetch()
    })

    // Assert: Debe haber invocado fetch nuevamente con page=2 y q=python
    expect(globalThis.fetch).toHaveBeenCalledTimes(2)
    expect(globalThis.fetch).toHaveBeenLastCalledWith(expect.stringContaining('page=2'))
    expect(globalThis.fetch).toHaveBeenLastCalledWith(expect.stringContaining('q=python'))
  })
})
