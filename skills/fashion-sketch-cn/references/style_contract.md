# Apparel Tech Pack -- Style Contract

Extracted from the FW26 Jacket Collection Tech Pack PDF reference artifact.

## Reference Source

- **Reference Type**: Uploaded PDF artifact
- **Artifact**: `FW_Jacket_Collection_Tech_Pack.pdf`
- **Page count**: 33 pages
- **Language**: English (Latin script)

## Typography System

### Font Families (extracted via fitz)

| Role | Reference Font | Weight | Attributes |
|------|---------------|--------|------------|
| H1 (Section titles) | Montserrat | Bold (700) | Large, commanding, dark color |
| H2 (Subsection titles) | Montserrat | SemiBold (600) | Medium size, dark color |
| H3 (Sub-subsection) | Montserrat | Medium (500) | Smaller, used for card labels |
| Body text | Open Sans | Regular (400) | 10-11 pt, dark gray, justified |
| Body medium | Open Sans | Medium (500) | Metadata labels |
| Body semi-bold | Open Sans | SemiBold (600) | Callout titles, bold labels |
| Serif accent | Noto Serif | Regular (400) | Occasional accent use |

### Critical Font Requirement

Use **TrueType fonts only** -- Montserrat for headings, Open Sans for body, Noto Serif for accents. These fonts are confirmed embedded in the reference PDF. Do **not** use generic Type3, bitmap, or system fallback fonts. All fonts must be properly embedded in the output document.

### CJK Font Strategy

When content includes Chinese/CJK text, substitute Montserrat with a geometric sans-serif CJK font (e.g., Noto Sans CJK SC for headings, using heavier weights for hierarchy). Substitute Open Sans with Noto Sans CJK SC for body text. Maintain the same weight hierarchy and sizing system regardless of script.

### Type Scale (approximate)

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Collection season label | 14-16 pt | Regular | Light gray (#B0B0B0) |
| Cover title | 48-56 pt | Bold | White (on dark cover) |
| H1 Section title | 28-32 pt | Bold | Dark charcoal (#2D2D3A) |
| H2 Subsection | 18-22 pt | SemiBold | Dark charcoal (#2D2D3A) |
| H3 / Card header | 14-16 pt | Medium | Dark charcoal (#2D2D3A) |
| Body text | 10-11 pt | Regular | Dark charcoal (#2D2D3A) |
| Table header | 10-11 pt | SemiBold | Dark charcoal (#2D2D3A) |
| Table body | 10-11 pt | Regular | Dark charcoal (#2D2D3A) |
| Figure caption | 10 pt | Regular | Medium gray (#6B6B6B) |
| Page number | 10 pt | Regular | Medium gray (#6B6B6B) |
| Footer / confidential | 9-10 pt | Regular | Medium gray (#6B6B6B) |

### Cover Page Special Typography

- Season label: all caps, wide letter-spacing (~0.3em), **centered**
- Title: all caps, extra bold, **centered**, with thick coral underline rule (~4-6 pt)
- Document type: **centered**, regular weight
- Metadata: label in bold, value in regular, **centered** vertical stack
- Confidential line: all caps, small, **centered** at page bottom

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--text-primary` | #2D2D3A | All body text, headings |
| `--text-secondary` | #6B6B6B | Captions, page numbers, footer |
| `--text-muted` | #B0B0B0 | Season label, subtle text |
| `--accent-coral` | #C94F56 | H1 underlines, style codes, "Table X" labels, callout borders |
| `--accent-teal` | #3A8080 | Alternate table label color |
| `--bg-page` | #FFFFFF | Page background |
| `--bg-card` | #F7F7F7 | Info card backgrounds |
| `--bg-callout` | #F5F5F5 | Callout/info box backgrounds |
| `--bg-table-header` | #F8F8F6 | Standard table header row |
| `--bg-table-header-dark` | #2D3142 | BOM table header (white text on dark navy) |
| `--bg-table-alt` | #FAFAFA | Alternating table row |
| `--border-light` | #E0E0E0 | Card borders, table row borders |
| `--border-callout` | #C94F56 | Callout box left border accent |
| `--cover-bg` | #2A2D3E | Cover page dark navy background |
| `--cover-ring` | #3D4055 | Decorative ring outlines on cover |

## Page Layout

### Page Composition
- **Page size**: A4 (or US Letter)
- **Margins**: ~25 mm (1 inch) all sides; generous whitespace
- **Content width**: Single column, full text width within margins
- **Alignment**: Body text justified; headings left-aligned; tables left-aligned
- **Page numbers**: Centered at bottom, medium gray

### Cover Page
- Full-page dark navy background (#2A2D3E)
- Decorative: two partial circular ring outlines (upper-right and lower-left)
- Accent: short coral horizontal line at upper-left
- **All text centered** vertically in the middle third of the page:
  - Season label (top, letter-spaced)
  - Collection title (large, bold, with coral underline)
  - Document type (regular)
  - Metadata fields (centered stack: Code, SKUs, Size Range, Date, Version)
- Confidential footer centered at bottom

### Table of Contents Page
- "Table of Contents" as H1 with coral underline spanning ~85% width
- Two-level hierarchy: main sections (bold) + subsections (regular, indented)
- **Right-aligned page numbers** connected by **dotted leader lines**
- Style names listed individually under "Style Specifications"
- Clean, minimal, single page (fit all entries on one page with appropriate spacing)

### Section Divider Pages
- H1 title with coral underline spanning ~85% page width
- One-line description below the title
- No other content on the page
- Used before: Style Specifications, Fabric & Trim Library, BOM, Packaging & Labeling, Quality Standards

### Content Pages
- H1 section title at top with coral underline rule spanning ~85% page width
- H2 subsection titles without underline
- Body text in single justified column
- Page number centered at bottom

## Table Styling

### Standard Tables (measurement charts, construction details, colorways)
- Header row: light warm gray background (#F8F8F6), semi-bold text
- Body rows: alternating white / very light gray
- Horizontal borders only: thin light gray (#E0E0E0) lines between rows
- No vertical borders
- Cell padding: moderate (~8-10 pt vertical)

### BOM Tables
- Header row: **dark navy background (#2D3142)**, **white** text, bold
- Category divider rows: light gray background with bold uppercase text (e.g., "FABRICS", "HARDWARE", "LABELS & TRIMS")
- Body rows: alternating white / light gray
- Horizontal borders only

### Table Labels
- "Table X" prefix in coral accent color
- Description in regular dark text following

## Callout / Info Boxes

- Light gray background (#F5F5F5)
- Thick left border in coral (#C94F56), ~4-6 pt
- Used for: measurement tolerance notes, BOM notes, special handling notes, carton labeling requirements, leather/fur special notes
- Internal padding: moderate (~12-16 pt)

## Info Cards (Style Summary)

- Light gray border (#E0E0E0)
- Very light gray background (#F7F7F7)
- Style code in coral color, bold
- 2-column grid layout on the page
- 3-4 info lines per card (Fabric, Category, Price Tier)

## Metadata Bars (Style Spec Pages)

- Light gray background strip spanning page width
- 3 columns of label-value pairs
- Labels in small uppercase/medium gray; values in bold dark text
- Categories shown: CATEGORY, PRIMARY/SHELL FABRIC, LINING/FILL/ORIGIN

## Figure Treatment

- Flat sketches centered on page, side-by-side front/back
- Caption centered below: "Figure X: [description]"
- Caption text in medium gray, regular weight
- **Must be actual generated illustrations**, not placeholder boxes

## Fabric Swatch Grid

- 2x4 image grid displaying actual fabric texture photographs
- Each swatch labeled: Code, Material Name, Available Colors
- **Must be actual generated fabric texture images**, not solid color rectangles

## Section Heading Pattern

- H1: "N. Section Name" -- large bold text + thick coral underline rule below
- H2: "N.N Subsection Name" -- medium semi-bold, no underline
- H3: inline bold labels for sub-subsections

## Signature Block Grid (Approval Page)

- 3-column x 2-row grid layout
- Each block: role title (regular) + signature line + date line
- Horizontal rule for signature, "Date: ___" for date

## Revision History Table

- Standard table styling
- Columns: Version, Date, Description, Author

## Footer / Confidentiality

- Centered at page bottom
- "CONFIDENTIAL" label + confidentiality statement
- Document title + version + date on final line
