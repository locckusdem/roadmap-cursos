# SPEC — [Nombre del producto]

> **Qué es este documento:** tu versión refinada de la SPEC de clase.
> El repo empieza con la SPEC de clase **tal cual** (primer commit). Este archivo es su evolución:
> mismos requisitos, ambigüedades resueltas, decisiones incorporadas.
> **Regla:** si la SPEC de clase no lo decía y vos lo definiste, queda acá (con el porqué)
> o se referencia al documento donde quedó decidido (PRD para producto, TRD para técnica).
> **Cuándo está bien:** un lector que no estuvo en el aula del 20/10 entiende el producto
> completo leyendo solo este archivo, y puede rastrear cada decisión hasta su origen.

## 1. Identidad del producto

- **Nombre propio:** [el nombre que le pusiste — es tu producto ahora]
- **Una línea:** [para quién · qué hace · por qué importa]

## 2. Problema

[2 a 4 párrafos: quién sufre el problema hoy, cómo lo resuelve (o no) lo que ya existe,
por qué una comunidad cambia la ecuación del catálogo de cursos]

## 3. Visión

[1 párrafo: cómo se ve el producto en su mejor versión dentro de 12 meses]

## 4. Alcance

### Dentro

- [feature o capacidad 1]
- [...]

### Fuera (out of scope explícito)

- [lo que NO vamos a construir en esta versión — cuanto más duro y explícito, mejor]
- [...]

## 5. Reglas de producto clave

| # | Regla | Origen |
|---|-------|--------|
| BR-001 | [ej. un curso aportado entra al sistema "en revisión" y solo llega al catálogo comunitario tras validación] | SPEC clase ("cursos cargados y **validados** pasan al catálogo") |
| BR-002 | [ej. cada usuario ve y edita solo su propio roadmap] | decisión propia |
| BR-003 | [ej. quien aporta un curso declara si él/ella lo tomó] | SPEC clase |
| BR-… | | |

> El detalle completo de reglas vive en el PRD §7. Acá van las 3 a 5 que definen el carácter del producto.

## 6. Stack registrado (versiones exactas con las que se va a desarrollar)

| Capa | Tecnología | Versión exacta instalada |
|------|------------|--------------------------|
| Frontend | React + Vite + pnpm | [ej. react 19.x, vite x.y, pnpm x.y] |
| Backend | FastAPI + uv | [ej. fastapi 0.158.x, uv x.y] |
| Base de datos | PostgreSQL | [18.6] |
| Infra (dev) | Docker + Docker Compose | [versión] |

> Verificá con `pnpm -v`, `uv --version`, `docker --version` etc. y registrá lo que **realmente** instalaste.

## 7. Restricciones técnicas heredadas de la SPEC de clase

| # | Restricción | Cómo la vamos a cumplir (1-2 líneas) |
|---|-------------|--------------------------------------|
| 1 | Mobile-first con mejora progresiva: base sin media queries; `@media (min-width: …)` solo para agregar/mejorar | [decisión] |
| 2 | Paginación de todas las consultas de listado y de sus tablas | [decisión: offset+total / cursor — ver TRD] |
| 3 | Menú sándwich en mobile | [decisión] |
| 4 | Screaming Architecture | [decisión: carpetas por dominio — ver TRD §3.2] |

## 8. Vacíos de la SPEC de clase y decisiones tomadas

> La SPEC de clase fue escrita a propósito incompleta. Esta tabla es la prueba de que
> los huecos los **resolviste vos**, no que los esquivaste.

| # | Vacío detectado en la SPEC | Opciones consideradas | Decisión | Dónde se desarrolla |
|---|----------------------------|-----------------------|----------|---------------------|
| 1 | [ej. ¿quién valida los cursos aportados?] | [auto-moderación / validación por docente / puntuación comunitaria] | [tu decisión] | [PRD BR-xxx / TRD TD-xxx] |
| 2 | [ej. ¿hay roles?] | | | |
| 3 | [ej. ¿qué es exactamente "incluir en mi catálogo"?] | | | |
| 4 | [ej. ¿la búsqueda es por texto, filtro, o ambos?] | | | |
| … | | | | |

## 9. Historia de la SPEC (autoregistro de cambios)

| Fecha | Cambio | Por qué |
|-------|--------|---------|
| 20/10/2026 | SPEC de clase recibida en el aula | — |
| 21/10/2026 | Primer commit: SPEC de clase tal cual | regla de la consigna |
| [fecha] | [ej. se agregó §8 con las decisiones sobre validación] | [motivo] |
