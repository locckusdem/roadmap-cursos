# UX-UI — Sistema de diseño de Roadmap de Cursos

**Versión:** 1.0 · **Instancia A** · **23/10/2026**

## 1. Principios

1. Mobile-first: diseñar primero para 360 px y mejorar progresivamente.
2. Claridad antes que decoración: una acción primaria visible y estados explícitos.
3. Confianza: mostrar estado de moderación, fuente externa y mensajes de error accionables.
4. Accesibilidad desde el componente: teclado, foco, contraste y semántica no son una etapa posterior.

## 2. Tokens

### 2.1 Color

| Token | HEX | Uso | Contraste |
|---|---|---|---|
| `--color-primary` | `#1A73E8` | acciones y links | 4.56:1 con blanco, AA para texto normal |
| `--color-on-primary` | `#FFFFFF` | texto sobre primario | 4.56:1 |
| `--color-background` | `#F8F9FA` | fondo de página | — |
| `--color-surface` | `#FFFFFF` | cards, formularios, navbar | — |
| `--color-text` | `#202124` | texto principal | 16.10:1 con blanco |
| `--color-text-muted` | `#5F6368` | metadatos | 6.43:1 con blanco |
| `--color-border` | `#DADCE0` | divisores y controles | 1.88:1; no se usa como único indicador |
| `--color-success` | `#137333` | aprobado/éxito | 5.10:1 con blanco |
| `--color-warning` | `#8A4B00` | pendiente/advertencia | ≥4.5:1 con blanco |
| `--color-error` | `#B3261E` | validación/error | 5.38:1 con blanco |

### 2.2 Tipografía

| Token | Valor | Uso |
|---|---|---|
| `--font-family-base` | `Arial, Helvetica, sans-serif` | fallback estable, estética Google |
| `--text-sm` | 14px / 21px | metadatos y ayudas |
| `--text-base` | 16px / 24px | cuerpo, inputs, botones |
| `--text-lg` | 20px / 28px | títulos de sección |
| `--text-xl` | 24px / 31px | títulos de página |
| `--text-xxl` | 32px / 40px | hero, solo desktop si aplica |

### 2.3 Espaciado y elevación

| Token | Valor |
|---|---|
| `--space-1` a `--space-8` | 4, 8, 12, 16, 24, 32, 40, 48px |
| `--radius-sm / md / lg` | 4 / 8 / 16px |
| `--shadow-sm / md` | `0 1px 2px #0000001A` / `0 2px 8px #0000001F` |
| `--z-header / modal / toast` | 100 / 200 / 300 |
| `--content-max` | 1200px |

```css
:root {
  --color-primary: #1A73E8;
  --color-on-primary: #FFFFFF;
  --color-background: #F8F9FA;
  --color-surface: #FFFFFF;
  --color-text: #202124;
  --color-text-muted: #5F6368;
  --color-border: #DADCE0;
  --color-success: #137333;
  --color-warning: #8A4B00;
  --color-error: #B3261E;
  --font-family-base: Arial, Helvetica, sans-serif;
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 40px; --space-8: 48px;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 16px;
  --shadow-sm: 0 1px 2px #0000001A; --shadow-md: 0 2px 8px #0000001F;
}
```

## 3. Mobile-first

La base no contiene media queries: contenedor con padding 16 px, una columna, cards apiladas, controles con target mínimo 44×44 px y navbar hamburguesa. En `@media (min-width: 768px)` se habilitan grid de dos/tres columnas, navegación horizontal y timeline con más aire. En `@media (min-width: 1024px)` se limita el contenedor a 1200 px y se aumenta densidad, sin cambiar prioridades ni esconder información.

## 4. Componentes y estados

### CourseCard

Anatomía: título enlazado, categoría/tema, resumen de metadatos, badges de certificado/examen/aval y acción “Agregar a mi roadmap”. `default` usa superficie y sombra sutil; `hover` eleva en desktop; `focus-visible` muestra outline de 2 px; `seleccionada` muestra borde primario y texto “En mi roadmap”; `loading` usa skeleton; `error` no se representa como card incompleta, sino con retry/estado global.

### RoadmapTimeline

Cada item muestra posición, título, categoría y acciones reordenar/quitar. Estados `loading` (skeleton vertical), `empty` (mensaje + “Explorar cursos”), `ready`, `saving` (acción deshabilitada y feedback), `error` (mantener orden local y ofrecer reintento). En móvil es una columna; desde 768 px incorpora conectores y más información.

### Pagination

Muestra anterior, siguiente, páginas cercanas, página actual con `aria-current="page"` y total. `disabled` en extremos, `loading` deshabilita controles, `single-page` se oculta si `pages ≤ 1`, `error` ofrece reintentar. Nunca cambia `limit` silenciosamente.

### Navbar con menú hamburguesa

En móvil: logo, botón de 44 px y panel; cerrado no expone links al foco, abierto usa `aria-expanded=true`, `aria-controls`, foco al primer link, cierre por X, Escape, click fuera o selección. En 768 px los links son horizontales y el botón desaparece visualmente. Debe mantener “Catálogo”, “Mi roadmap”, “Aportar curso” y sesión.

### Botones, campos y feedback

Botón: `default`, `hover`, `active`, `focus-visible`, `disabled`, `loading`; label estable y spinner con texto accesible. Campo: label visible, `default`, `focus`, `filled`, `error`, `disabled`; error vinculado por `aria-describedby`. Toast: éxito/error/info, `role=status` (error `role=alert`), 5 s como máximo y cierre manual. Skeleton solo durante carga esperada. Empty state siempre explica causa y ofrece CTA.

## 5. Layout y pantallas

Header sticky sobre fondo blanco, contenido centrado en `--content-max`. Catálogo usa búsqueda, filtro, grid y paginador. Detalle prioriza título, metadatos y acción de roadmap. Aporte usa formulario agrupado y estado. Roadmaps usa timeline y estados vacíos. Las rutas y APIs están en [APPFlow.md](./APPFlow.md).

## 6. WCAG 2.1 AA

- Contraste de texto mínimo 4.5:1 y 3:1 para texto grande; no usar color como único indicador.
- Todos los controles accesibles por teclado, orden de foco lógico y `:focus-visible` de 2 px.
- Landmarks `header`, `nav`, `main`, `footer`; un único `h1` por pantalla y jerarquía sin saltos.
- Navbar con `aria-expanded`, `aria-controls`, foco y Escape; modal con focus trap y retorno de foco.
- Labels persistentes, `aria-describedby` para errores, `aria-live` para cambios y foco al primer error del formulario.
- Alt descriptivo o `aria-hidden` para imágenes decorativas; iconos con nombre cuando son botones.
- Respeto de `prefers-reduced-motion`; no depender de animaciones.
- Targets mínimos 44×44 px y zoom del navegador sin pérdida de contenido.

## 7. Iconografía

Se utilizará una biblioteca SVG consistente compatible con React (por ejemplo Lucide) cuando se agreguen dependencias en Instancia B. Iconos de 20–24 px, color heredado, nunca como sustituto único de texto; se documentará la versión junto con el `package.json`.
