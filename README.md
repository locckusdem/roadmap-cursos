# Roadmap de Cursos (Comunidad)

> WebApp de gestión de comunidad de cursos: catálogo comunitario de cursos gratuitos
> + roadmaps personales de aprendizaje.
>
> **Estado:** 📚 Documentación (Instancia A) — desarrollo pendiente de aprobación docente.

**Stack:** React 19 + Vite + pnpm · FastAPI + uv · PostgreSQL 18.6 · Docker Compose (dev)

---

## Cómo levantar en desarrollo

Para levantar el entorno completo con PostgreSQL, backend y frontend en una máquina limpia:

```bash
git clone https://github.com/locckusdem/roadmap-cursos
cd roadmap-cursos
cp .env.example .env
docker compose up --build
```

### URLs de acceso

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend Healthcheck:** [http://localhost:8000/health](http://localhost:8000/health)
- **Backend API Cursos:** [http://localhost:8000/cursos](http://localhost:8000/cursos)
- **Base de datos:** `localhost:5432`

---

## Qué hace

Plataforma comunitaria donde cualquier usuario puede descubrir y postular cursos gratuitos de diversas plataformas web. Tras un proceso de validación para garantizar la calidad del contenido, los cursos pasan a formar parte del catálogo público general, permitiendo que cada estudiante diseñe, organice y gestione sus propios roadmaps de aprendizaje personalizados.

## Documentación

| Documento | Responde la pregunta | Link |
|---|---|---|
| SPEC | ¿Qué nos pidieron construir y qué decidimos nosotros? | [docs/SPEC.md](docs/SPEC.md) |
| PRD | ¿Para quién, qué problema resuelve, qué hace y qué NO hace? | [docs/PRD.md](docs/PRD.md) |
| TRD | ¿Cómo lo construimos técnicamente y por qué? | [docs/TRD.md](docs/TRD.md) |
| UX-UI | ¿Cómo se ve, se siente y se comporta? | [docs/UX-UI.md](docs/UX-UI.md) |
| APPFlow | ¿Qué pantallas hay y cómo se navega? | [docs/APPFlow.md](docs/APPFlow.md) |
| BackendSchema | ¿Qué datos persistimos y qué API expone? | [docs/BackendSchema.md](docs/BackendSchema.md) |
| Implementation Plan | ¿En qué orden construimos y qué significa "hecho"? | [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) |

## Cómo revisar este repo

- Los archivos `.md` se renderizan automáticamente en la interfaz web de GitHub.
- Los diagramas Mermaid (`erDiagram`, `flowchart`, `stateDiagram`) renderizan nativamente en GitHub.
- Para previsualización local: en VS Code con `Ctrl + Shift + V` (o extensión Markdown All in One).

## Estado del trabajo

| Instancia | Contenido | Estado |
|---|---|---|
| A — Documentación | Repo + 7 documentos técnicos | ✅ Enviada a aprobación el 23/10/2026 |
| B — Desarrollo del MVP | Ejecución del Implementation Plan | ⏳ Pendiente de aprobación docente |
| C — Clase 27/10 | Testing, Docker multi-stage, gestión del cambio | ✅ Completada (T1–T11 verificados) |

### Checklist final de la clase (27/10/2026)

| Ticket | Estado | Rama | Merge | Commit |
|---|:---:|---|:---:|---|
| T1 | ✅ | `ticket/T1-reglas-cursos` | ✅ | `test: agregar tests unitarios para reglas de cursos` |
| T2 | ✅ | `ticket/T2-reglas-roadmaps` | ✅ | `test: agregar tests unitarios para reglas de roadmaps` |
| T3 | ✅ | `ticket/T3-validacion-aportes` | ✅ | `test: agregar tests unitarios para servicio de validacion de aportes` |
| T4 | ✅ | `ticket/T4-integracion-curso-repository` | ✅ | `test: agregar tests de integracion para CursoRepository` |
| T5 | ✅ | `ticket/T5-integracion-flujo-aporte` | ✅ | `test: agregar tests de integracion para flujo de aporte y validacion` |
| T6 | ✅ | `ticket/T6-tests-frontend-hook` | ✅ | `test: agregar tests de frontend para hook useCursos` |
| T7 | ✅ | `ticket/T7-dockerfile-backend-multistage` | ✅ | `docker: agregar Dockerfile multi-stage para backend` |
| T8 | ✅ | `ticket/T8-dockerignore-optimizado` | ✅ | `docker: agregar archivos .dockerignore optimizados` |
| T9 | ✅ | `ticket/T9-dockerfile-frontend-nginx` | ✅ | `docker: agregar Dockerfile multi-stage para frontend con nginx` |
| T10 | ✅ | `ticket/T10-compose-con-healthchecks` | ✅ | `docker: agregar healthchecks y dependencias de servicios a compose` |
| T11 | ✅ | `ticket/T11-cierre-auditable-ciclo` | ✅ | `docs: agregar changelog y retrospectiva de la clase 27/10` |

### Criterios de verificación alcanzados

| Criterio | Mínimo requerido | Resultado obtenido |
|---|---|---|
| Tests passing (0 failed, 0 skipped) | 100% | 100% (42 backend + 4 frontend) |
| Cobertura backend (unit + integration) | $\ge 85\%$ | **96%** |
| Imagen backend (multi-stage) | < 100 MB | **96.8 MB** |
| Imagen frontend (multi-stage + nginx) | < 30 MB | **13.9 MB** |
| Docker Compose | 3/3 servicios healthy | **3/3 healthy** (`postgres`, `backend`, `frontend`) |
| Commits | 100% Conventional Commits | 100% Conventional Commits en español |
| Gestión del cambio | Rama por ticket, merges trazables, CHANGELOG | T1–T11 en ramas individuales mergeadas sin ramas huérfanas |

## Versionado

- **Flujo de Git:** GitHub Flow con ramas temáticas cortas (`docs/*`, `feat/*`, `fix/*`) que se integran a `main` mediante commits de fusión trazables.
- **Convención de commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `docker:`, `chore:`).

---

## Licencia / Uso

Trabajo Práctico — Desarrollo de Software, UTN FR La Plata, 2026.