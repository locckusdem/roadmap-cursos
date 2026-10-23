# SPEC — Roadmap de Cursos (Comunidad)

**Versión:** 1.0 · **Instancia:** A — documentación · **Fecha:** 23/10/2026  
**Propósito:** refinamiento formal de la especificación de clase y registro de las decisiones que cierran sus vacíos.

## 1. Identidad del producto

**Roadmap de Cursos (Comunidad)** es una webapp para descubrir cursos gratuitos validados por la comunidad y organizar un roadmap personal de aprendizaje. Un visitante puede consultar el catálogo; un usuario registrado puede aportar cursos y gestionar su roadmap; un moderador audita los aportes antes de publicarlos.

## 2. Problema y visión

La oferta de cursos gratuitos está dispersa entre plataformas, con metadatos incompletos y calidad variable. Las búsquedas generales no permiten distinguir rápidamente si un curso sigue disponible, qué conocimientos requiere o si incluye evaluación, certificado o aval.

La comunidad aporta conocimiento contextual y mantiene el catálogo actualizado. La moderación agrega una barrera de calidad: ningún aporte se publica automáticamente. El roadmap convierte el descubrimiento en un plan personal ordenado.

En doce meses, el producto será un catálogo confiable y consultable desde móvil, con aportes trazables, moderación auditable y roadmaps personales que permitan pasar de una búsqueda a una secuencia de aprendizaje concreta.

## 3. Alcance de la Instancia A / MVP

### Dentro

- Catálogo público de cursos gratuitos en estado `PUBLICADO`, con búsqueda, filtro por categoría y paginación uniforme mediante `page` y `limit`.
- Detalle de curso con enlace externo, metadatos y disponibilidad.
- Registro, login y logout con JWT en cookie `HttpOnly`, `Secure` en producción y protección CSRF mediante `SameSite=Lax` más validación de origen para mutaciones.
- Formulario autenticado para aportar cursos y consultar el estado del propio aporte.
- Ciclo de moderación `PENDIENTE → APROBADO/RECHAZADO`, con rol `MODERADOR` y motivo de rechazo.
- Roadmap personal: agregar, ordenar y quitar cursos publicados.
- Interfaz responsive mobile-first, menú hamburguesa y estética Google/Material.

### Fuera de alcance

- No se reproduce video ni audio dentro de la plataforma: el enlace lleva al proveedor externo.
- No hay pasarela de pagos, cursos pagos, suscripciones ni procesamiento de tarjetas.
- No se emiten certificados ni se verifica la certificación de terceros.
- No hay aplicación móvil nativa, modo offline, chat, foro, mensajería ni recomendaciones algorítmicas.
- No se implementa OAuth social, recuperación de contraseña ni MFA en el MVP.
- No se permite edición colaborativa de un mismo roadmap ni roadmaps públicos en esta instancia.
- No se realiza scraping automático: quien aporta declara los metadatos y el moderador verifica el enlace.

## 4. Reglas de producto

| ID | Regla | Origen |
|---|---|---|
| BR-001 | Todo curso aportado nace en estado `PENDIENTE`; solo un moderador puede aprobarlo y hacerlo visible en el catálogo general. | Requisito obligatorio de la instancia |
| BR-002 | El aportante debe declarar si realizó el curso; la declaración queda registrada con el aporte. | Especificación de clase |
| BR-003 | Solo cursos `PUBLICADO` pueden aparecer en el catálogo o agregarse a un roadmap. | Decisión de producto |
| BR-004 | Un usuario solo puede leer y modificar sus propios aportes y roadmaps. | Decisión de producto |
| BR-005 | La URL canónica de un curso no puede duplicarse entre aportes activos. | Integridad y calidad |
| BR-006 | Todos los listados de cursos usan `page` y `limit`, con límites `1 ≤ limit ≤ 100` y valor predeterminado 20. | Restricción de diseño |

## 5. Stack registrado

| Capa | Tecnología/versionado objetivo | Registro |
|---|---|---|
| Frontend | React 19 + Vite + pnpm | versiones fijadas por el `package.json` de Instancia B; no se generan dependencias en Instancia A |
| Backend | FastAPI + uv | versiones fijadas por `pyproject.toml` de Instancia B; no se generan dependencias en Instancia A |
| Persistencia | PostgreSQL 18.6 | versión obligatoria |
| Infraestructura local | Docker + Docker Compose | Compose plugin compatible con Docker Desktop/Engine del equipo |

## 6. Restricciones técnicas heredadas

| # | Restricción | Cumplimiento |
|---|---|---|
| 1 | Mobile-first con mejora progresiva | Base para 360 px sin media queries; mejoras únicamente con `@media (min-width: 768px)` y, cuando corresponda, 1024 px. |
| 2 | Paginación de listados | Contrato uniforme `page` + `limit`, respuesta con `items`, `total`, `page`, `limit`, `pages`. |
| 3 | Menú sándwich | Navbar colapsada por defecto en móvil, con `aria-expanded`, foco administrado y navegación horizontal desde 768 px. |
| 4 | Screaming Architecture | Backend organizado en `app/cursos/`, `app/roadmaps/`, `app/aportes/`, `app/auth/`, `app/core/`; frontend en `src/features/catalogo/`, `src/features/roadmaps/`, `src/features/aportar/`, `src/shared/`. |

## 7. Decisiones sobre vacíos

| # | Vacío | Opciones consideradas | Decisión | Desarrollo |
|---|---|---|---|---|
| 1 | ¿Quién valida un aporte? | Automático, docente único, moderación comunitaria | Rol `MODERADOR`; el aporte queda `PENDIENTE` hasta aprobación explícita. | PRD §7, BackendSchema §2 |
| 2 | ¿Qué estados tiene un curso? | Borrador/revisión/publicado, solo publicado, workflow externo | `PENDIENTE`, `PUBLICADO`, `RECHAZADO`; el estado de postulación es visible al autor. | BackendSchema §2 |
| 3 | ¿Cómo se autentica? | Sesión server-side, JWT en localStorage, JWT HttpOnly | JWT en cookie `HttpOnly`; no se expone el token a JavaScript. | TRD ADR-001 |
| 4 | ¿Cómo se pagina? | Cursor, offset con `page_size`, offset con `page` + `limit` | `page` + `limit` en todos los listados de cursos y roadmap. | TRD ADR-002 |
| 5 | ¿Qué significa “mi roadmap”? | Público, uno compartido, privado por usuario | Colección privada por usuario autenticado, ordenable y editable. | PRD BR-004, BackendSchema §3.4 |
| 6 | ¿Cómo se filtra? | Texto, categorías, ambos | Texto `q` y categoría opcional `categoria_id`; solo sobre `PUBLICADO`. | APPFlow §3, BackendSchema §3.2 |
| 7 | ¿Qué respuesta de error se usa? | Texto libre, RFC 7807, envelope propio | `application/problem+json` para errores, con `code`, `message` y `details`. | TRD ADR-003 |

## 8. Criterio de trazabilidad

Las historias P0 son US-01 a US-05 en [PRD.md](./PRD.md). Cada una tiene pantalla/ruta en [APPFlow.md](./APPFlow.md), endpoints en [BackendSchema.md](./BackendSchema.md) y tareas P0 en [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md). Las definiciones visuales compartidas viven en [UX-UI.md](./UX-UI.md); las decisiones técnicas, en [TRD.md](./TRD.md).

## 9. Historia

| Fecha | Cambio | Motivo |
|---|---|---|
| 20/10/2026 | Recepción de especificación de clase | Punto de partida académico |
| 21/10/2026 | Registro inicial de documentación | Requisito de la consigna |
| 23/10/2026 | Refinamiento formal y consolidación de siete documentos canónicos | Cerrar vacíos y garantizar trazabilidad para Instancia B |
