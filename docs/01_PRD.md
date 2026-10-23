# PRD — Product Requirements Document — [Nombre del producto]

> **Qué es:** el QUÉ y el POR QUÉ. Para quién construimos, qué problema resuelve, qué hace
> y — con el mismo peso — qué **no** hace. No habla de tecnología ni de carpetas (eso es el TRD).
> **Cuándo está bien:** alguien del equipo puede construir la feature correcta sin preguntarte
> nada de producto; el "no" (out of scope) está tan claro como el "sí"; cada historia tiene
> criterios de aceptación verificables.

## 1. Resumen ejecutivo

[El producto en 3 a 5 líneas. Si alguien lee solo esto, debe entender de qué va.]

## 2. Objetivos y métricas de éxito

| Objetivo | Cómo sabemos que lo logramos |
|----------|------------------------------|
| [ej. que el catálogo comunitario tenga cursos validados de múltiples plataformas] | [ej. X% de los aportes terminan validados; variedad de categorías] |
| [ej. que el roadmap sea usado para planificar] | [métrica o señal observable] |

## 3. Personas

### Persona 1 — [nombre/rol] (mínimo 2 personas en total)

- **Contexto:** [quién es, cuándo usa el producto]
- **Motivaciones:** [qué quiere lograr]
- **Frustraciones hoy:** [qué lo frena en lo existente]
- **Historias tipo:** [2 o 3 frases en su voz]

### Persona 2 — [...]

## 4. User stories

> Mínimo 6 historias, al menos 4 con prioridad **P0** (P0 = el producto no funciona sin esto
> el día del MVP). Formato: **Como** [rol], **quiero** [acción], **para** [beneficio].
> Criterios de aceptación en formato Dado/Cuando/Entonces o checklist verificable.

| ID | Prioridad | Historia | Criterios de aceptación |
|----|-----------|----------|-------------------------|
| US-001 | P0 | Como visitante, quiero ver el catálogo comunitario paginado, para descubrir cursos sin registrarme | - [ ] Dado que visito `/catalogo`, veo la primera página (20 items)<br>- [ ] Dado que hay más de 20 cursos, aparece el paginador<br>- [ ] Dado que no hay cursos, veo un empty state con CTA |
| US-002 | P0 | Como usuario, quiero aportar un curso con sus metadatos, para enriquecer el catálogo | [...] |
| US-003 | P0 | [...] | [...] |
| US-004 | P0 | [...] | [...] |
| US-005 | P1 | [...] | [...] |
| US-006 | P1 | [...] | [...] |

## 5. Requisitos funcionales

| ID | Requisito | Historia relacionada |
|----|-----------|----------------------|
| RF-001 | [ej. el sistema permite registrar usuarios con email y contraseña] | US-xxx |
| RF-002 | | |

## 6. Requisitos no funcionales

| ID | Requisito | Notas |
|----|-----------|-------|
| RNF-001 | Todos los listados paginados | heredado de SPEC clase |
| RNF-002 | Mobile-first con mejora progresiva | heredado de SPEC clase |
| RNF-003 | [ej. el catálogo debe cargar en < 2 s con 1.000 cursos] | decisión propia |

## 7. Reglas de negocio

| ID | Regla | Fuente |
|----|-------|--------|
| BR-001 | Un curso aportado no aparece en el catálogo comunitario hasta ser validado | SPEC clase |
| BR-002 | Quien aporta un curso declara si tomó el curso o no | SPEC clase |
| BR-003 | [ej. el roadmap es personal y privado por defecto] | decisión propia |
| BR-004 | [ej. un usuario no puede aportar dos veces el mismo URL de curso] | decisión propia |
| BR-… | | |

## 8. Fuera de alcance (out of scope)

- [explícito y duro: lo que NO se construye en esta versión]
- [ej. pagos, cursos de pago, certificados emitidos por la plataforma, app móvil nativa…]

## 9. Supuestos y decisiones sobre la SPEC de clase

[Qué asumiste y por qué — con link al detalle en `docs/SPEC.md` §8]

## 10. Preguntas abiertas

| Pregunta | Impacto | Estado |
|----------|---------|--------|
| [ej. ¿los aportes expiran si nadie los valida?] | medio | [abierta / decidida → link] |

---

**Referencias:**
- Atlassian — Plantilla PRD: https://www.atlassian.com/software/confluence/templates/product-requirements
- Lenny Rachitsky — Plantilla de requirements: https://www.atlassian.com/software/confluence/templates/requirements
