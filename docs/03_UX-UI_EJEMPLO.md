# UX-UI — Guía visual de estilos — [Nombre del producto]

> **EJEMPLO COMPLETADO** — referencia de formato y profundidad para la plantilla
> [`03_UX-UI.md`](./03_UX-UI.md).
> **No lo copies tal cual:** los valores de este ejemplo responden a la inspiración Google
> fijada por la SPEC. Tu guía debe tomar decisiones para **tu** producto, con tus propios
> tokens, tus componentes y tus justificaciones — pero con **esta** profundidad.

## 1. Principios

1. **Limpieza sobre adorno:** si un elemento no comunica información ni acción, sobra.
2. **Espacio en blanco como herramienta:** el aire agrupa mejor que las cajas.
3. **Un solo color de acción por pantalla:** el azul primario marca lo que se puede hacer.
4. **Mobile primero:** el layout base se diseña para 360px y se mejora hacia arriba, nunca se repara.

## 2. Design tokens

### 2.1 Paleta de colores

| Token | Valor | Uso | Contraste |
|-------|-------|-----|-----------|
| `--color-primary` | `#1a73e8` | botones primarios, links, foco, labels activos | vs white ≈ 4.6:1 ✓ AA |
| `--color-primary-dark` | `#185abc` | hover/press del primario | — |
| `--color-primary-container` | `#e8f0fe` | chips seleccionados, fondos de ítem activo del menú | — |
| `--color-on-primary` | `#ffffff` | texto/iconos sobre primario | vs `#1a73e8` ≈ 4.6:1 ✓ AA |
| `--color-surface` | `#ffffff` | cards, drawer, header | — |
| `--color-background` | `#f8f9fa` | fondo de página (gris Google muy claro) | — |
| `--color-text` | `#202124` | texto principal | vs `#ffffff` ≈ 16:1 ✓ AA |
| `--color-text-muted` | `#5f6368` | metadatos, texto secundario | vs `#ffffff` ≈ 7:1 ✓ AA |
| `--color-border` | `#dadce0` | bordes de inputs, divisores | ver nota de accesibilidad §6 |
| `--color-hover-grey` | `#f1f3f4` | hover de botones secundarios y filas | — |
| `--color-success` | `#188038` | toast de éxito, badge "publicado" | — |
| `--color-warning` | `#f9ab00` | badge "en revisión", avisos | — |
| `--color-error` | `#d93025` | errores de validación, botón peligroso | — |

> Los valores son los de la paleta de productos Google (azul `#1a73e8`, gris de texto
> `#202124`/`#5f6368`, semáforo Material). Verificá cada ratio en
> https://webaim.org/resources/contrastchecker/ y anotá el tuyo real.

### 2.2 Tipografía

| Token | Familia | Tamaño / line-height | Uso |
|-------|---------|----------------------|-----|
| `--font-family-base` | Roboto, `system-ui`, sans-serif | — | cuerpo |
| `--text-sm` | | 14px / 20px | metadatos, badges, tabla |
| `--text-base` | | 16px / 24px | texto de formulario y párrafo |
| `--text-lg` | | 18px / 24px | títulos de card |
| `--text-xl` | | 22px / 28px | títulos de pantalla |

> Roboto (Google Fonts) es la fuente de la inspiración. Cargala self-host o por CDN
> y declará `font-display: swap`.

### 2.3 Espaciado, radios, sombras

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` … `--space-8` | 4, 8, 12, 16, 24, 32, 40, 48 px | ritmo de 4px en todo |
| `--radius-input` | 8px | inputs, selects |
| `--radius-card` | 12px | cards de curso |
| `--radius-button` | 18px (pill) | botones — estilo Material 3 |
| `--radius-snackbar` | 8px | toasts |
| `--shadow-1` | `0 1px 2px rgba(60, 64, 67, .1), 0 1px 3px 1px rgba(60, 64, 67, .15)` | reposo (cards) |
| `--shadow-2` | `0 1px 2px rgba(60, 64, 67, .1), 0 2px 6px 2px rgba(60, 64, 67, .15)` | hover de card, drawer |
| `--z-header` | 100 | header sticky |
| `--z-drawer` | 200 | menú sándwich + overlay |
| `--z-snackbar` | 300 | toasts |

> Las sombras son las de elevación de los productos Google (capas de rgba(60,64,67,…)).

### 2.4 Bloque de variables listo para copiar

```css
:root {
  --color-primary: #1a73e8;
  --color-primary-dark: #185abc;
  --color-primary-container: #e8f0fe;
  --color-on-primary: #ffffff;
  --color-surface: #ffffff;
  --color-background: #f8f9fa;
  --color-text: #202124;
  --color-text-muted: #5f6368;
  --color-border: #dadce0;
  --color-hover-grey: #f1f3f4;
  --color-success: #188038;
  --color-warning: #f9ab00;
  --color-error: #d93025;

  --font-family-base: "Roboto", system-ui, sans-serif;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.375rem;

  --space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 40px; --space-8: 48px;

  --radius-input: 8px;
  --radius-card: 12px;
  --radius-button: 18px;
  --radius-snackbar: 8px;

  --shadow-1: 0 1px 2px rgba(60, 64, 67, .1), 0 1px 3px 1px rgba(60, 64, 67, .15);
  --shadow-2: 0 1px 2px rgba(60, 64, 67, .1), 0 2px 6px 2px rgba(60, 64, 67, .15);
}
```

## 3. Estrategia mobile-first con mejora progresiva

> Regla de la SPEC: la base **no** usa media queries; `@media (min-width: …)` solo agrega o mejora.

| Capa | Dónde aplica | Qué define |
|------|--------------|------------|
| **Base (sin MQ)** | todos los viewports | 1 columna; header con hamburguesa; grid de cards apiladas; tablas densas → cards; targets ≥ 44px |
| `@media (min-width: 768px)` | tablet | grid de 2 columnas; nav horizontal en header; tablas como tabla real; padding de página ↑ |
| `@media (min-width: 1024px)` | desktop | grid de 3 columnas; contenedor `max-width: 1140px`; hamburguesa oculta (nav visible); drawer deprecado |

## 4. Componentes (anatomía + estados)

### 4.1 Botón

- **Primario (filled):** fondo `--color-primary`, texto `--color-on-primary`, pill
  (`--radius-button`), padding `11px 23px`, Roboto 500 14px. Hover: `--color-primary-dark` + `--shadow-1`.
- **Secundario (text button):** sin fondo; texto `--color-primary`; hover: fondo `--color-hover-grey`.
- **Peligro:** texto `--color-error`; confirmación obligatoria antes de ejecutar.
- Estados de todos: `default`, `hover`, `focus-visible` (anillo `2px solid --color-primary` con offset 2px),
  `active`, `disabled` (opacidad .38, sin pointer), `loading` (spinner + disabled).

### 4.2 Campo de formulario

- Outlined: 1px `--color-border`, radio `--radius-input`, label flotante en `--color-text-muted`.
- Estados: `default` · `focus` (borde 2px `--color-primary`, label azul) · `filled` ·
  `error` (borde y label `--color-error` + mensaje con `aria-describedby`) · `disabled` (fondo `--color-hover-grey`).

### 4.3 Card de curso

- Superficie `--color-surface`, radio `--radius-card`, `--shadow-1`; padding `--space-4`.
- Contenido: título (`--text-lg`, `--color-text`) · categoría como chip (`--color-primary-container` /
  texto `--color-primary-dark`) · docentes en `--text-sm` `--color-text-muted` · badges
  certificado/examen/aval con icono Material Symbols.
- Estados: `default` · `hover` (`--shadow-2`, cursor pointer) · `seleccionada` (borde
  `--color-primary` + check).

### 4.4 Lista/tabla paginada

- ≥ 768px: tabla real, filas con divisor `--color-border`, hover `--color-hover-grey`.
- < 768px: las mismas filas como cards apiladas (misma data, otro layout — no scroll horizontal).
- Paginador estilo Google: «‹ 1 2 3 … ›» centrado, botones circulares, actual en `--color-primary-container`.

### 4.5 Menú sándwich (drawer)

- Botón hamburguesa (icono Material Symbols `menu`) en el header izquierdo, < 1024px.
- Panel: `--color-surface`, sombra al abierto (`--shadow-2`), borde derecho redondeado `0 16px 16px 0`,
  ancho 280px, overlay `rgba(32, 33, 34, .6)`.
- Ítems: 48px de alto; el activo con fondo `--color-primary-container` y texto `--color-primary-dark`.
- Cierre: link, X, `ESC`, click en overlay. ARIA: `aria-expanded`, `aria-controls`, foco atrapado y restaurado.

### 4.6 Modal

- Superficie blanca, radio 28px (Material 3), `--shadow-2`, overlay igual al drawer.
- `focus trap`; cierre con `ESC` y botón X; acciones a la derecha (Cancelar texto / acción primaria filled).

### 4.7 Snackbar (toast)

- Fondo `#323232`, texto blanco, radio `--radius-snackbar`, ancho mínimo 344px,
  posición inferior centrada (mobile) / inferior izquierda (desktop), `role="status"`.
- Tipos: éxito (icono verde ✓) · error (icono rojo) · info. Duración 4–6 s; acción "Deshacer" cuando aplica.

### 4.8 Skeleton y Empty state

- Skeleton: bloques `--color-hover-grey` con shimmer; se usa en listados y detalle mientras carga.
- Empty state: icono grande `--color-text-muted` + título `--text-lg` + bajada + CTA primario
  (ej. "Todavía no aportaste cursos — Aportar el primero").

## 5. Layout y navegación

- **Header:** sticky (`--z-header`), fondo blanco, alto 64px; izquierda: hamburguesa + logo;
  derecha: acciones de sesión (avatar o "Ingresar"). Sombra aparece al hacer scroll (`--shadow-1`).
- **Contenedor:** `max-width: 1140px`, padding lateral `--space-5` (desktop) / `--space-4` (mobile).
- **Pantallas:** el detalle de cada una vive en el APPFlow; acá está la gramática con la que se dibujan.

## 6. Accesibilidad mínima (no negociable)

- [x] Texto sobre superficies claras: `#202124` ≈ 16:1 y `#5f6368` ≈ 7:1 → ✓ AA
- [x] Botón primario: blanco sobre `#1a73e8` ≈ 4.6:1 → ✓ AA
- [ ] `#dadce0` es borde **decorativo** de inputs: el contraste de 3:1 del control lo entrega el
      **estado focus** (`#1a73e8`, 4.6:1). Si un control no tiene estado focus visible, no cumple.
- [ ] `:focus-visible` en todo interactivo (anillo azul con offset)
- [ ] Drawer con `aria-expanded` / `aria-controls`, foco atrapado y restaurado al cerrar
- [ ] `prefers-reduced-motion: reduce` desactiva shimmer y transiciones de elevación
- [ ] Iconos decorativos con `aria-hidden="true"`; iconos de acción con `aria-label`

## 7. Iconografía y assets

- Set: **Material Symbols** (el set de Google) — https://fonts.google.com/icons
  (self-host o ligado por variable font, peso 400/500)
- Tamaño por defecto de icono en botón: 20px; en lista: 24px; color: hereda del texto
- Imágenes: sin stock decorativo; ilustraciones de empty state en estilo Material (colores planos,
  formas redondeadas)
