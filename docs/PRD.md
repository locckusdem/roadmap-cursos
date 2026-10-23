# PRD — Roadmap de Cursos (Comunidad)

**Versión:** 1.0 · **Instancia A** · **23/10/2026**

## 1. Resumen ejecutivo

Roadmap de Cursos (Comunidad) reúne cursos gratuitos aportados por usuarios y publicados solo después de una auditoría de moderación. Permite descubrirlos mediante catálogo, búsqueda, categorías y paginación, y ordenarlos en un roadmap personal. El MVP prioriza confianza, trazabilidad y una experiencia mobile-first.

## 2. Problema, objetivos y métricas

| Problema | Objetivo | Señal de éxito del MVP |
|---|---|---|
| Cursos gratuitos dispersos y difíciles de comparar | Catálogo público con metadatos homogéneos | Un visitante consulta cursos publicados, filtra y pagina sin autenticarse |
| Aportes sin control de calidad | Flujo auditable de moderación | 100% de los aportes nuevos se almacenan como `PENDIENTE` y ninguno pendiente aparece públicamente |
| Descubrimiento sin planificación | Roadmap personal ordenable | Un usuario autenticado agrega, reordena y quita un curso publicado |
| Navegación poco usable en móvil | Interfaz responsive accesible | Recorrido P0 usable a 360 px con menú hamburguesa y foco visible |

## 3. Público objetivo

### Autodidacta

Busca una ruta confiable para aprender una competencia sin pagar. Usa el catálogo desde móvil, compara metadatos y guarda cursos publicados en su roadmap privado. Le frustran enlaces rotos, información incompleta y no saber qué estudiar primero.

### Colaborador

Conoce cursos valiosos que no están catalogados. Aporta URL y metadatos, declara si lo realizó y necesita saber si está pendiente, aprobado o rechazado. Le frustran formularios ambiguos y no recibir feedback.

### Moderador

Revisa que el enlace sea accesible, gratuito, pertinente y que los metadatos sean razonables. Aprueba o rechaza con motivo. Necesita una cola clara y acciones trazables para evitar que contenido no auditado llegue al catálogo.

## 4. Alcance

### En alcance

Catálogo público paginado, detalle, búsqueda/filtro, autenticación básica, aportes, estado del aporte, moderación, roadmap privado y diseño responsive accesible.

### Fuera de alcance

No se incluye reproductor embebido de video, pasarela de pagos, cursos pagos, certificados propios, app nativa, chat/foro, recomendaciones automáticas, scraping, OAuth, MFA ni recuperación de contraseña.

## 5. Historias de usuario P0

### US-01 — Descubrir el catálogo

**Como** Autodidacta, **quiero** consultar un catálogo público paginado y filtrable, **para** encontrar cursos gratuitos sin registrarme.

**Criterios de aceptación (Gherkin):**

```gherkin
Característica: Catálogo público
  Escenario: consultar la primera página
    Dado que existen cursos PUBLICADO
    Cuando visito "/"
    Entonces veo cursos en tarjetas y la respuesta usa page=1 y limit=20
    Y no veo cursos PENDIENTE ni RECHAZADO
  Escenario: paginar resultados
    Dado que existen más de 20 cursos publicados
    Cuando selecciono la página siguiente
    Entonces se solicita la página correspondiente con el mismo limit
    Y el paginador informa total y páginas
  Escenario: filtrar sin resultados
    Dado que la búsqueda no coincide con cursos publicados
    Cuando aplico el filtro
    Entonces veo un estado vacío y una acción para limpiar filtros
```

### US-02 — Consultar el detalle

**Como** Autodidacta, **quiero** abrir el detalle de un curso publicado, **para** evaluar si encaja en mi aprendizaje.

```gherkin
Característica: Detalle de curso
  Escenario: curso existente
    Dado que el curso 42 está PUBLICADO
    Cuando visito "/cursos/42"
    Entonces veo título, categoría, tema, versión, año, docentes, flags y enlace externo
  Escenario: curso inexistente o no publicado
    Cuando visito un id que no existe o no está PUBLICADO
    Entonces recibo una pantalla 404 sin exponer datos privados
```

### US-03 — Aportar para moderación

**Como** Colaborador autenticado, **quiero** postular un curso con sus metadatos, **para** enriquecer el catálogo.

```gherkin
Característica: Aporte de curso
  Escenario: envío válido
    Dado que inicié sesión
    Cuando envío URL, título, categoría, tema, versión, año, docentes, flags y declaración de realización
    Entonces el sistema crea el aporte con estado PENDIENTE
    Y muestra confirmación y el id del aporte
    Y el curso no aparece aún en el catálogo público
  Escenario: URL duplicada
    Dado que la URL ya tiene un aporte activo
    Cuando envío el formulario
    Entonces veo un error de duplicado y no se crea otro aporte
  Escenario: datos inválidos
    Cuando falta un campo obligatorio o el año no es válido
    Entonces veo errores junto a cada campo y conservo los valores ingresados
```

### US-04 — Moderar un aporte

**Como** Moderador, **quiero** aprobar o rechazar aportes pendientes con un motivo, **para** controlar la calidad del catálogo.

```gherkin
Característica: Moderación
  Escenario: aprobación
    Dado que soy MODERADOR y el aporte está PENDIENTE
    Cuando lo apruebo
    Entonces pasa a PUBLICADO
    Y puede aparecer en el catálogo y ser agregado a roadmaps
  Escenario: rechazo
    Dado que soy MODERADOR y el aporte está PENDIENTE
    Cuando lo rechazo informando un motivo
    Entonces pasa a RECHAZADO
    Y el autor puede consultar el motivo
  Escenario: usuario sin rol
    Dado que no soy MODERADOR
    Cuando intento moderar
    Entonces recibo 403 y el estado no cambia
```

### US-05 — Gestionar roadmap personal

**Como** Autodidacta autenticado, **quiero** agregar, ordenar y quitar cursos publicados, **para** construir mi plan personal.

```gherkin
Característica: Roadmap personal
  Escenario: agregar curso
    Dado que inicié sesión y el curso está PUBLICADO
    Cuando lo agrego desde el detalle
    Entonces aparece en "/roadmaps" con una posición
  Escenario: reordenar
    Dado que mi roadmap tiene dos o más cursos
    Cuando cambio el orden y guardo
    Entonces la secuencia se conserva al recargar
  Escenario: quitar
    Cuando quito un curso de mi roadmap
    Entonces deja de aparecer en mi lista y no se elimina del catálogo
  Escenario: no autenticado
    Cuando intento agregar un curso sin sesión
    Entonces se me redirige a login y puedo volver al detalle
```

## 6. Requisitos funcionales

| ID | Requisito | Historia |
|---|---|---|
| RF-01 | Exponer catálogo solo con cursos `PUBLICADO`, búsqueda por `q`, filtro por categoría y paginación `page`/`limit`. | US-01 |
| RF-02 | Exponer detalle público de un curso publicado. | US-02 |
| RF-03 | Registrar, autenticar y cerrar sesión con cookie JWT HttpOnly. | US-03, US-05 |
| RF-04 | Validar y persistir aportes como `PENDIENTE`, evitando URL duplicada. | US-03 |
| RF-05 | Permitir a un moderador aprobar/rechazar con motivo y registrar auditoría básica. | US-04 |
| RF-06 | Mantener un roadmap privado por usuario con cursos publicados, orden y operaciones CRUD necesarias. | US-05 |

## 7. Reglas de negocio

| ID | Regla |
|---|---|
| BR-01 | `PENDIENTE` es el estado inicial obligatorio de todo aporte. |
| BR-02 | Solo `MODERADOR` puede cambiar `PENDIENTE` a `PUBLICADO` o `RECHAZADO`. |
| BR-03 | Un curso no publicado no es visible públicamente ni puede agregarse a un roadmap. |
| BR-04 | El aportante declara `realizado_por_aportante` y el valor no puede omitirse. |
| BR-05 | URL normalizada única entre aportes que no estén rechazados. |
| BR-06 | Los roadmaps son privados y cada item pertenece a un único usuario. |

## 8. No funcionales

| ID | Requisito verificable |
|---|---|
| RNF-01 | Listados de cursos usan `page` y `limit`; `limit` está acotado a 1–100 y default 20. |
| RNF-02 | Base mobile-first de 360 px sin media queries; mejora en `min-width: 768px`. |
| RNF-03 | Contraste, teclado, foco, nombres accesibles y errores asociados cumplen WCAG 2.1 AA. |
| RNF-04 | Contraseñas nunca se almacenan en claro; JWT no se expone a `localStorage`. |
| RNF-05 | Errores se expresan como `application/problem+json` y timestamps en UTC ISO 8601. |

## 9. Supuestos y preguntas cerradas

Los vacíos se resolvieron en [SPEC.md](./SPEC.md) §7. No quedan preguntas bloqueantes para Instancia B. Los textos de los campos de aporte son contractuales y están detallados en [BackendSchema.md](./BackendSchema.md) §3.3.
