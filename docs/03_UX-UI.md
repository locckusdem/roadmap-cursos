# UX-UI — Guía visual de estilos — [Nombre del producto]

> **Qué es:** la gramática visual de la interfaz: tokens, componentes, estados, accesibilidad.
> No es un prototipo navegable (eso lo cubre el APPFlow); es el conjunto de reglas con las que
> se construye cada pantalla **antes** de escribir CSS.
> **Inspiración fijada por la SPEC:** la apariencia y experiencia deben ser similares a **Google**
> (estética Material: limpieza, espacio en blanco, azul primario, sombras sutiles, radios amplios).
> **Ejemplo completado:** [`03_UX-UI_EJEMPLO.md`](./03_UX-UI_EJEMPLO.md) — mirá el nivel de detalle
> esperado; no lo copies, adaptá.
> **Cuándo está bien:** dos personas que sigan esta guía construyen la misma pantalla y queda
> igual; todos los estados de cada componente (focus, error, empty, loading) están definidos
> de antemano; la estrategia mobile-first con mejora progresiva es explícita.

## 1. Principios (3 a 5)

- [ej. "Mobile primero: el layout base se diseña para 360px y se mejora, nunca se repara"]
- [ej. "El estado vacío y el de error son parte del diseño, no un afterthought"]
- [...]

## 2. Design tokens

### 2.1 Paleta de colores

| Token | Valor | Uso | Contraste AA |
|-------|-------|-----|--------------|
| `--color-primary` | `#……` | botones primarios, links | vs `--surface`: X.X:1 ✓ |
| `--color-on-primary` | `#……` | texto/iconos sobre primario | vs primary: X.X:1 ✓ |
| `--color-surface` | `#……` | fondos de tarjetas | |
| `--color-background` | `#……` | fondo de página | |
| `--color-text` | `#……` | texto principal | vs background: X.X:1 ✓ |
| `--color-text-muted` | `#……` | texto secundario | vs background: ≥ 4.5:1 ✓ |
| `--color-success` | `#……` | confirmaciones | |
| `--color-warning` | `#……` | avisos | |
| `--color-error` | `#……` | errores de validación | |

> Verificá el contraste en https://webaim.org/resources/contrastchecker/ y anotá el ratio real.

### 2.2 Tipografía

| Token | Familia | Tamaño / line-height | Uso |
|-------|---------|----------------------|-----|
| `--font-family-base` | [ej. Inter, system-ui] | — | |
| `--text-sm` | | 14px / 1.5 | metadatos |
| `--text-base` | | 16px / 1.5 | cuerpo |
| `--text-lg` | | 20px / 1.4 | títulos de sección |
| `--text-xl` | | 24px / 1.3 | títulos de página |

### 2.3 Espaciado, radios, sombras, z-index

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` … `--space-8` | [escala 4px o 8px: 4, 8, 12, 16, 24, 32…] | ritmo vertical y gutters |
| `--radius-sm / md / lg` | | botones / cards / modales |
| `--shadow-sm / md` | | elevación de cards / modales |
| `--z-header / --z-modal / --z-toast` | | orden de capas |

### 2.4 Bloque de variables listo para copiar

```css
:root {
  /* completar con los valores de las tablas anteriores */
}
```

## 3. Estrategia mobile-first con mejora progresiva

> Obligatorio según la SPEC. **Prohibido** usar media queries para "arreglar" el layout base:
> solo para agregar o mejorar a medida que la pantalla crece.

| Capa | Dónde aplica | Qué define |
|------|--------------|------------|
| **Base (sin media queries)** | todos los viewports | layout de 1 columna, menú sándwich, tablas densas → cards apiladas, tipografía mobile, targets ≥ 44px |
| `@media (min-width: 768px)` | tablets | [ej. grid de 2 columnas, nav horizontal en el header, tablas como tabla real] |
| `@media (min-width: 1024px)` | desktop | [ej. sidebar o nav completa, grid de 3 columnas, contenedor con max-width] |

## 4. Componentes (anatomía + estados)

> Por cada componente: anatomía breve, tokens usados y **todos** sus estados.

### 4.1 Botón (primario / secundario / peligro)

- Estados: `default`, `hover`, `focus-visible`, `active`, `disabled`, `loading`
- [anatomía en 3 a 5 líneas: padding, radio, tipografía, icono]

### 4.2 Campo de formulario (input / select)

- Estados: `default`, `focus`, `filled`, `error` (con mensaje asociado), `disabled`
- [label siempre visible, mensajes de error con `aria-describedby`]

### 4.3 Card de curso

- [campos: título, categoría, docentes, badges: certificado / examen / aval]
- Estados: `default`, `hover`, `seleccionada (en mi roadmap)`

### 4.4 Lista/tabla paginada

- [qué elemento usa cada viewport; comportamiento del paginador; qué muestra al estar vacía]

### 4.5 Menú sándwich

- Anatomía: botón hamburguesa → panel de navegación
- Estados: cerrado, abierto
- Cierre: toque en link, botón X, tecla `ESC`, click fuera
- ARIA: `aria-expanded`, `aria-controls`, manejo de foco

### 4.6 Modal

- Estados: cerrado, abierto; con `focus trap`; cierre con `ESC`

### 4.7 Toast (notificación)

- Tipos: éxito / error / info; duración; posición; `role="status"`

### 4.8 Skeleton y Empty state

- Skeleton: para `loading` de listados y detalle
- Empty state: ilustración/icono + mensaje + CTA (ej. "todavía no hay cursos en esta categoría — aportá el primero")

## 5. Layout y navegación

- **Header:** sticky; contenido en mobile (logo + hamburguesa) vs desktop (logo + nav horizontal + acciones de sesión)
- **Contenedores:** [max-width, gutters, márgenes]
- **Pantallas:** [descripción breve por pantalla → el detalle de navegación vive en el APPFlow]

## 6. Accesibilidad mínima (no negociable)

- [ ] Contraste AA (≥ 4.5:1) en todo texto; ≥ 3:1 en bordes de controles
- [ ] `:focus-visible` visible en todo elemento interactivo
- [ ] Menú sándwich con `aria-expanded` / `aria-controls` y foco gestionado
- [ ] `prefers-reduced-motion` respetado en transiciones
- [ ] Imágenes y iconos con `alt` o `aria-label`
- [ ] Errores de formulario asociados al campo (`aria-describedby`)

## 7. Iconografía y assets

- Set elegido: [ej. lucide-react / heroicons / SVGs inline]
- Por qué: [...]
- Tamaño y color por defecto de los iconos: [...]

---

**Referencias:**
- NN/g — Front-End Style-Guides (definición y checklist): https://www.nngroup.com/articles/front-end-style-guides/
- NN/g — Design Systems 101: https://www.nngroup.com/articles/design-systems-101/
