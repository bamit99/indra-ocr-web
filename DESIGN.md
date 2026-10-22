---
name: Indra OCR — Finding Aid
description: Archival accession-desk design system for Indra OCR's single intake page.
colors:
  paper: "#F4EFE4"
  panel: "#FBF8F1"
  sheet: "#FFFFFF"
  ink: "#1A1712"
  ink-soft: "#554C3F"
  ink-faint: "#6B6152"
  rule: "#C9BFA9"
  rule-soft: "#E2D9C6"
  vermilion: "#C8371E"
  vermilion-deep: "#A82C16"
  vermilion-wash: "#F6E4DC"
typography:
  display:
    fontFamily: "Libre Caslon Display, Georgia, serif"
    fontSize: "clamp(30px, 6vw, 44px)"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "0.01em"
  body:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: "normal"
  label:
    fontFamily: "Archivo, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.18em"
  mono:
    fontFamily: "Courier Prime, ui-monospace, Courier New, monospace"
    fontSize: "13px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  stamp:
    fontFamily: "Courier Prime, ui-monospace, Courier New, monospace"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.22em"
rounded:
  none: "0px"
  sm: "2px"
  md: "3px"
spacing:
  sm: "14px"
  md: "20px"
  lg: "26px"
  xl: "30px"
components:
  button-primary:
    backgroundColor: "{colors.vermilion}"
    textColor: "{colors.sheet}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: "14px 30px"
  button-primary-hover:
    backgroundColor: "{colors.vermilion-deep}"
    textColor: "{colors.sheet}"
    rounded: "{rounded.sm}"
    padding: "14px 30px"
  button-disabled:
    backgroundColor: "{colors.ink-faint}"
    textColor: "{colors.sheet}"
    rounded: "{rounded.sm}"
    padding: "14px 30px"
  panel:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "26px 26px 22px"
  drop-field:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "20px"
  drop-field-over:
    backgroundColor: "{colors.vermilion-wash}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "20px"
  stamp:
    typography: "{typography.stamp}"
    textColor: "{colors.vermilion}"
    rounded: "{rounded.md}"
    padding: "6px 10px 5px"
  stamp-accessioned:
    typography: "{typography.stamp}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "6px 10px 5px"
  claim-stub:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "14px 16px"
  preview:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "14px"
---

# Design System: Indra OCR — Finding Aid

## Overview

**Creative North Star: "Finding Aid — the Archival Accession Desk"**

OCR intake is staged as archival accession: every document that arrives is accessioned, stamped, and served from a claim desk. The page reads like a repository reading room — bone paper ground, engraving ink, hairline rules, tracked small-caps labels — not like a developer tool. It explicitly refuses the category default: the dark dev-tool card, the system-font stack, the spinner status line.

Density is form-like and centered: a single 760px column carries an accession panel whose fields are ruled like paper form lines, a live monospace ledger line underneath, then claim stubs and ruled reading columns for results. The memorable moment is the stamp — states press themselves onto the page (ACCESSIONED → PROCESSING → DIGITIZED) over a live monospace ledger counting pages and seconds.

One accent does all the committing. Everything else is warm neutral paper, ink, and rule tones, held apart by hairlines rather than depth. All fonts are self-hosted OFL Google Fonts (Libre Caslon Display, Archivo, Courier Prime).

**Key Characteristics:**
- Archival, printed, ruled — flat surfaces separated by hairlines, never by glass or glow.
- Three-voice type: Caslon for the masthead only, Archivo for interface prose and labels, Courier Prime for anything countable or status-bearing.
- Vermilion as the single committed accent: stamps, primary action, links, errors.
- Motion is a physical press, not a digital fade; reduced-motion collapses it to instant.

## Colors

A warm bone-paper palette: two paper tones, three ink tones, two rule tones, and one committed vermilion accent with a deep hover and a pale wash.

### Primary
- **Committed Vermilion** (`#C8371E`): the only accent. Owns the stamp states, the BEGIN CONVERSION button, links, the focus-visible outline, the caret, and the checked checkbox. Reserved for moments of commitment.
- **Vermilion Deep** (`#A82C16`): hover/pressed state of anything vermilion — button hover, link hover.
- **Vermilion Wash** (`#F6E4DC`): the accent at rest — text selection background and the drop field while a file is dragged over it.

### Secondary
- **Engraving Ink** (`#1A1712`): primary text; masthead; the ACCESSIONED stamp.
- **Ink Soft** (`#554C3F`): secondary text — small-caps labels, section heads, ledger copy, footer row.
- **Ink Faint** (`#6B6152`): tertiary text — hints, placeholders, empty-state copy, the engine stamp and API line; also the disabled button background.

### Neutral
- **Bone Paper** (`#F4EFE4`): page ground (body, header, footer), scrollbar track.
- **Panel** (`#FBF8F1`): raised-by-tone surfaces — accession panel, claim stubs.
- **Sheet** (`#FFFFFF`): working surfaces — drop field, preview figures.
- **Rule** (`#C9BFA9`): primary hairlines — header/footer double rules, panel and stub borders, scrollbar thumb.
- **Rule Soft** (`#E2D9C6`): secondary hairlines — section-head leader lines, ledger top border, preview caption divider.

### Named Rules
**The Vermilion Rule.** Vermilion appears only where the system commits or signals: stamps, the primary button, links, focus, errors. Its rarity against bone paper is the point; if a screen has more than one vermilion element beyond action/error/active-state, one of them is wrong.

**The Tone-Depth Rule.** Depth is expressed only by the paper → panel → sheet ladder plus hairlines (`#F4EFE4` → `#FBF8F1` → `#FFFFFF`). Never by shadow.

## Typography

**Display Font:** Libre Caslon Display (with Georgia, serif fallback)
**Body Font:** Archivo (with system-ui, sans-serif fallback)
**Label/Mono Font:** Courier Prime (with ui-monospace, Courier New, monospace fallback)

**Character:** A classic pairing — Caslon brings the repository-title formality to one line only, Archivo carries the whole interface with a neutral grotesque voice, and Courier Prime lends typewriter authority to accession data. All three are self-hosted (`static/fonts/`, OFL).

### Hierarchy
- **Display** (400, `clamp(30px, 6vw, 44px)`, 1.05, `0.01em` tracking): the "Indra OCR" masthead — the only place display type appears.
- **Title / section head** (600, `12px`, 1, `0.2em`, uppercase): panel headings ("ACCESSION INTAKE"), followed by a flexible hairline leader (`.panel h2::after`).
- **Label** (600, `11px`, 1, `0.18em`, uppercase): field labels, claim-stub kinds, preview captions, footer row (`0.16em`), meta rule (`0.22em`). Ink-soft.
- **Body** (400, `16px`, 1.55): Archivo prose. Checkbox label `14.5px`; hints and descriptions `12px` (1.5).
- **Data / mono** (400, `13px`, 1.5): ledger line with `font-variant-numeric: tabular-nums`; document filename `15px`; preview code `13px/1.6` (`12px` for JSON). Ink-soft or ink.
- **Engine stamp / API line** (mono, `11px`, `0.14em`/`0.1em`, uppercase): masthead carries the live OCR engine version ("ENGINE v1.1.2"), footer carries the page's API ("POST /convert · GET /download/{id}"). Both are functional facts, not decorative marks. Ink-faint.
- **Button** (600, `12.5px`, `0.16em`, uppercase): Archivo on the primary action.
- **Stamp** (700, `11px`, `0.22em`, uppercase): Courier Prime, always inside a bordered, slightly rotated box.

### Named Rules
**The Data Rule.** Anything countable, status-bearing, or identifying — elapsed time, the engine version stamp, result ids, filenames, file contents — is Courier Prime. Prose is Archivo. Display type never leaves the masthead.

## Layout

Single centered column: `.wrap` is `max-width: 760px`, `margin: 0 auto`, `padding: 0 20px` — the 20px gutter is the only horizontal page padding.

Vertical rhythm: masthead `34px 0 10px`, meta rule `0 0 12px`, main `30px 0 8px`, results `margin-top: 30px`, footer `margin-top: 44px` with `18px 0 34px` padding. Inside the panel: `26px 26px 22px` padding, section head to form `18px`, field gaps `16px` (`7px` label-to-control), ledger `18px` above / `14px` below its hairline.

Header and footer carry a **double rule**: a 1px border plus a second 1px rule inset 3px (`header::after`, `footer::before`) — the ruled edge of an archival folder.

Claim stubs (`flex: 1 1 200px`) and previews (`flex: 1 1 300px`) wrap into rows; both the masthead and the footer row wrap on narrow screens.

**Responsive:** one breakpoint, `560px` — masthead wraps (engine version stamp drops to its own line, `padding-top: 24px`), panel padding tightens to `20px 16px`.

## Elevation & Depth

**No shadows anywhere.** The system is flat by doctrine. Depth is conveyed by the tonal ladder (paper → panel → sheet) and by 1px hairlines; there is no glass, blur, or glow. The only z-layering is functional (a hidden file input, the caret).

### Shadow Vocabulary
None. This is the answer, not an omission.

### Named Rules
**The Flat-By-Default Rule.** A surface is a flat tone with a hairline edge. If something needs to feel raised, move it one step up the tone ladder (`#F4EFE4` → `#FBF8F1` → `#FFFFFF`); never add a shadow.

## Shapes

Square corners are the default (`0px`): panels, stubs, previews, drop field. Two deliberate exceptions — the button is barely softened (`2px`) and the stamp box (`3px`) — so pressed objects read as objects, not as boxes.

Borders are 1px hairlines in `#C9BFA9` (or `#E2D9C6` for interior dividers), except the stamp, which uses a 2px border in its own currentColor. The drop field is the only dashed border (`1px dashed`) — a form line awaiting input. Checkboxes use native elements tinted with `accent-color: #C8371E`. The masthead mark is a 22px hairline circle-and-cross engraving glyph in vermilion. Scrollbars are themed (`10px` thumb, `#C9BFA9` on `#F4EFE4` track, `5px` radius, `2px` paper inset border).

## Components

### Masthead
- Caslon `h1` (display token) in ink, vermilion 22px SVG mark at left (baseline row, `14px` gap), engine version stamp `ENGINE v<version>` in mono `11px / 0.14em / uppercase` pushed right (`margin-left: auto`). The version is read at request time from the installed `indra-ocr` distribution, so it can never drift from the running engine.
- Below: meta rule — Archivo 600 `11px / 0.22em / uppercase`, ink-soft ("Self-hosted · CPU-only").
- Bottom edge: double hairline rule (`1px solid #C9BFA9` + inset `#C9BFA9` line at `bottom: 3px`).

### Accession Panel
- **Shape:** square (`0px`), `1px solid #C9BFA9`.
- **Background:** panel tone `#FBF8F1` on paper ground; padding `26px 26px 22px`.
- **Section head:** label token, ink-soft, with a flexible `1px` rule-soft leader line filling the remainder of the row.
- **States:** static container; no hover.

### Drop Field (file input)
- **Style:** `1px dashed #C9BFA9`, sheet background (`#FFFFFF`), `20px` padding, centered text, `20px` field margin.
- **Filename:** mono `15px`; empty placeholder is ink-faint, chosen file is ink. Hint below: Archivo `12px`, ink-faint.
- **Hover:** border deepens to ink-soft (`0.18s`).
- **Drag-over (`.over`):** border becomes `1px solid #C8371E`, background becomes vermilion wash `#F6E4DC`.
- **Focus:** `2px solid #C8371E` outline, `2px` offset (matches global `:focus-visible`).

### Buttons (primary action)
- **Shape:** `2px` radius, padding `14px 30px`.
- **Primary:** vermilion `#C8371E` background, white text, Archivo 600 `12.5px / 0.16em / uppercase`.
- **Hover:** background vermilion-deep `#A82C16` (`0.15s`).
- **Active:** `translateY(1px)` (`0.05s`) — the press.
- **Disabled / processing:** background ink-faint `#6B6152`, `cursor: not-allowed`, no transform; label swaps to "Processing…".

### Ledger Line
- Row under a rule-soft top hairline (`margin-top: 18px; padding-top: 14px`), `min-height: 38px`, wraps.
- Text: mono `13px/1.5`, ink-soft, `tabular-nums` so elapsed time doesn't jitter. `role="status" aria-live="polite"`.

### Stamps (signature component)
- **Style:** mono 700 `11px`, `0.22em`, uppercase, `2px solid currentColor` border, `3px` radius, padding `6px 10px 5px`, rotated `-2.5deg` — a rubber stamp pressed slightly crooked.
- **States:** `accessioned` = ink `#1A1712`; `processing` = ink-soft `#554C3F`; `digitized` and `err` = vermilion `#C8371E`.
- **Motion (press):** `animation: press .5s cubic-bezier(.2,.9,.3,1.2) both` — `from { transform: rotate(-8deg) scale(1.7); opacity: 0 }` → `to { transform: rotate(-2.5deg) scale(1); opacity: 1 }`. Overshoot ease gives the stamp a physical thunk. Re-triggered per state by re-assigning the class and forcing a reflow.
- **Reduced motion:** global `prefers-reduced-motion: reduce` rule collapses all animation/transition durations to `0.001s` — the stamp lands instantly, rotation and final state preserved.

### Claim Stubs
- `flex: 1 1 200px`, panel background, `1px solid #C9BFA9`, padding `14px 16px`, square, stacked: kind label (label token, ink-soft), download link (mono 700 `14px`, vermilion, `word-break: break-all`), description (Archivo `12px`, ink-faint).

### Previews (reading columns)
- `flex: 1 1 300px`, sheet background, `1px solid #C9BFA9`, square.
- Caption row: label token, ink-soft, padding `10px 14px`, bottom hairline rule-soft.
- Body: mono `13px/1.6` ink, `14px` padding, `max-height: 44vh` scroll, `pre-wrap`. JSON variant drops to `12px`.

### Footer
- Double hairline rule on top (border + inset line at `top: 3px`), `18px 0 34px` padding.
- Row: Archivo 600 `11px / 0.16em / uppercase` ink-soft; API line (`POST /convert · GET /download/{id}`) in mono `11px / 0.1em` ink-faint; copyright name in ink; links vermilion (hover vermilion-deep). Right group pushed with `margin-left: auto`.

## Do's and Don'ts

### Do:
- **Do** keep the page on the tone ladder `#F4EFE4` → `#FBF8F1` → `#FFFFFF` and separate surfaces with `1px solid #C9BFA9` hairlines.
- **Do** reserve `#C8371E` for stamps, the primary button, links, focus rings, checked checkboxes, and errors — hover states step to `#A82C16`, drag-over/idle washes use `#F6E4DC`.
- **Do** set every label, section head, caption, and footer row as Archivo 600 `11–12px`, uppercase, tracked `0.16em–0.22em`, in ink-soft.
- **Do** set every number, status, filename, result id, and code block in Courier Prime with `tabular-nums` where values update live.
- **Do** use square corners (`0px`) everywhere except the button (`2px`) and the stamp (`3px`).
- **Do** press new stamps with the `press` keyframe (`-8deg/1.7 → -2.5deg/1`, `0.5s cubic-bezier(.2,.9,.3,1.2)`) and honor `prefers-reduced-motion`.

### Don't:
- **Don't** add shadows, glass, blur, or glow — depth is tone + hairline only.
- **Don't** use a spinner or generic progress bar for status; states are stamps plus a monospace ledger line.
- **Don't** introduce a second accent hue, a dark-mode dev-tool surface, or system-font defaults.
- **Don't** put display Caslon anywhere except the masthead `h1`.
- **Don't** use vermilion for decorative emphasis, long text, or large fills — its rarity is the system.
