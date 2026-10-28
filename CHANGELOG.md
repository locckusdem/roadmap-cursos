# Changelog

## [Clase 27/10/2026] - Instancia C: Testing, Docker Multi-Stage y Gestión del Cambio

### Added
- **T1 — Reglas de negocio de curso (`ticket/T1-reglas-cursos`):** Funciones puras `validar_aporte_curso` y `transicionar_estado_curso` con tests unitarios bajo patrón AAA y cobertura de edge cases (año futuro, URL duplicada, flags).
- **T2 — Reglas del roadmap del usuario (`ticket/T2-reglas-roadmaps`):** Funciones puras `validar_agregar_curso_a_roadmap`, `quitar_curso_de_roadmap` y `reordenar_items_roadmap` con control de duplicados, límites y estados requeridos.
- **T3 — Servicio de validación de aportes (`ticket/T3-validacion-aportes`):** Funciones puras `validar_permisos_moderacion` y `validar_decision_moderacion` con errores semánticos estables (`AportePermissionError`, `AporteStateError`, `AporteValidationError`).
- **T4 — Integration tests de `CursoRepository` (`ticket/T4-integracion-curso-repository`):** Suite completa de integración contra SQLite en memoria con SQLAlchemy 2.0 (roundtrip, paginación, filtro case-insensitive `q`, filtros por categoría, updates parciales y delete).
- **T5 — Integration tests de flujo aporte → validación (`ticket/T5-integracion-flujo-aporte`):** Verificación HTTP integral de endpoints `/api/aportes` y moderación (401 para autor sin sesión, creación en PENDING, 403 para validador no moderador, publicación y visibilidad en catálogo).
- **T6 — Tests de frontend para hook `useCursos` (`ticket/T6-tests-frontend-hook`):** Hook reactivo con estados de carga, manejo de errores de red, paginación, reseteo ante filtros y refetch testeado con Vitest y Happy-DOM.
- **T7 — Dockerfile multi-stage para backend (`ticket/T7-dockerfile-backend-multistage`):** Builder stage con `uv` y runtime en `python:3.12-alpine` con usuario no-root `appuser`, healthcheck y optimización de tamaño (< 100 MB).
- **T8 — Archivos `.dockerignore` optimizados (`ticket/T8-dockerignore-optimizado`):** Exclusión estricta de `.git`, caches de python/pytest/vitest, entornos virtuales y dependencias para builds reproducibles y limpios.
- **T9 — Dockerfile multi-stage para frontend (`ticket/T9-dockerfile-frontend-nginx`):** Builder con `node:20-alpine` + `pnpm` y runtime ultra liviano sobre `nginx:alpine-slim` (< 30 MB) con SPA fallback, proxy `/api/` y headers de seguridad.
- **T10 — Docker Compose con healthchecks (`ticket/T10-compose-con-healthchecks`):** Configuración de healthchecks en los 3 servicios (`postgres`, `backend`, `frontend`), dependencias `service_healthy`, volúmenes persistentes y verificación 3/3 healthy.
- **T11 — Cierre auditable y retrospectiva (`ticket/T11-cierre-auditable-ciclo`):** Documentación completa del ciclo, actualización del plan de implementación y retrospectiva del flujo de trabajo.

## [v0.1.0] - 2026-10-27

### Added
- Scaffold del proyecto: estructura backend/frontend, docker-compose de dev
- Backend mínimo: FastAPI con /health y GET /cursos
- Frontend mínimo: React + Vite consumiendo GET /cursos
- Integración de servicios con Docker Compose (PostgreSQL 18.6, backend, frontend)
