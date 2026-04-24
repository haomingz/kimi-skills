---
name: fashion-sketch-cn
description: 创建专业服装技术规格包（Tech Pack），包含系列概览、款式规格、工艺细节、尺寸表、面料库、物料清单（BOM）、质量标准与签核页。适用于服装、鞋履、配饰等需要结构化、专业技术文档格式的品类。
---

# Apparel Tech Pack

Create professional apparel technical specification packages following a structured, visually refined document format with a dark navy cover page, coral accent system, and clean table-driven content layout.

## Reference & Output Policy

| Attribute | Value |
|-----------|-------|
| **Reference Source** | Uploaded PDF artifact |
| **Reference Artifact Type** | PDF |
| **Reference File Type** | PDF |
| **Supported Outputs** | PDF, DOCX, PPTX |
| **Default Output** | DOCX (document is structured as an editable multi-section text document) |

When the user does not specify an output format, produce **DOCX**. Produce **PDF** when the user requests a finalized non-editable document. Produce **PPTX** only when the user explicitly requests a slide-presentation format.

## Quick Workflow

1. Gather collection data from the user (styles, measurements, materials, BOM)
2. Read `references/style_contract.md` for visual styling rules
3. Read `references/structure_contract.md` for document section hierarchy and field definitions
4. Generate the document in the requested output format
5. Apply the style contract consistently across all pages

## Style Summary

The tech pack follows a **modern minimal** aesthetic:

- **Cover**: Dark navy (#2A2D3E) full-bleed background with decorative ring outlines, **centered** collection metadata, coral accent underline on title
- **Typography**: Montserrat family for headings (Bold -> SemiBold -> Medium hierarchy), Open Sans for body text, Noto Serif for occasional accents; geometric sans-serif character throughout
- **Accent color**: Coral red (#C94F56) used for H1 underlines, style codes, "Table X" labels, and callout box left borders
- **Tables**: Light-gray header rows, alternating body rows, horizontal borders only; BOM tables use a dark navy header (#2D3142) with white text for stronger hierarchy
- **Callout boxes**: Light gray background with thick coral left border for notes and special instructions
- **Layout**: Generous margins, single-column content, page numbers centered at bottom
- **Section dividers**: Clean divider pages with H1 title + coral underline + brief description only, before major sections

For full details read `references/style_contract.md`.

## Document Structure

The tech pack contains these sections in order:

1. **Cover Page** -- season, collection title, metadata (code, SKU count, size range, date, version)
2. **Table of Contents** -- two-level hierarchy with dotted leaders and right-aligned page numbers
3. **Collection Overview** -- style summary cards + standard size chart
4. **Style Specifications** -- one 2-page spread per style (metadata bar, flat sketch, construction table, measurement chart, colorways)
5. **Fabric & Trim Library** -- fabric swatch photo grid + specifications, hardware tables, trims, labels
6. **Bill of Materials (BOM)** -- per-style material breakdown with category groupings
7. **Packaging & Labeling** -- individual packaging, carton specs, labeling requirements
8. **Quality Standards** -- AQL table, defect categories, testing requirements, inspection checklist
9. **Approval & Sign-Off** -- signature blocks, revision history, confidentiality notice (part of Section 6, not a separate top-level section)

For full section definitions, field lists, and numbering rules read `references/structure_contract.md`.

## Typography & Font Handling

### Reference Fonts (TrueType)
- **Headings**: Montserrat (Bold 700 for H1, SemiBold 600 for H2, Medium 500 for H3)
- **Body**: Open Sans (Regular 400, Medium 500, SemiBold 600)
- **Serif accent**: Noto Serif (Regular 400) for occasional accent use

### Critical Font Requirements
Use **TrueType fonts only** -- Montserrat, Open Sans, and Noto Serif. Do **not** use generic Type3 or bitmap fonts. These fonts must be embedded in the output document for professional text rendering.

### CJK / Mixed-Script Strategy
When content includes Chinese or other CJK text, substitute:
- **Headings**: Noto Sans CJK SC (Heavy/Bold for H1, Bold for H2, Medium for H3)
- **Body**: Noto Sans CJK SC (Regular 400, Medium 500)

Maintain the same type scale, weight hierarchy, and visual density regardless of script. Use one CJK-capable font family consistently across the entire document.

## Illustration & Image Requirements

### Flat Sketches (CRITICAL)
Each style specification page **must** include front and back flat sketch illustrations. Do **not** use placeholder boxes or generic icons.

- Use the image generation tool to create technical flat sketches for each style
- Prompt pattern: "Technical fashion flat sketch, front and back view of a [garment type], clean line drawing, white background, professional garment technical illustration style"
- Place side-by-side (front left, back right) centered on the page
- Caption below: "Figure N: [Style Code] Front & Back Flat Sketch"

### Fabric Swatches (CRITICAL)
The Fabric Swatches section **must** include actual fabric texture photographs, not solid color rectangles.

- Use the image generation tool to create fabric swatch textures
- Prompt pattern: "Close-up fabric swatch texture photo, [material type] fabric, showing weave/pattern detail, professional product photography, soft even lighting"
- Display in a 2x4 grid with code labels and available colors beneath each swatch

## Adaptation Guidelines

When adapting this template for different product categories:

| Aspect | Guidance |
|--------|----------|
| **Product type** | Replace "Jacket" with category (shirt, pant, dress, accessory). Adjust metadata bar labels and measurement points accordingly |
| **Style count** | Template supports 5-20 styles. Scale measurement tables and BOM sections accordingly |
| **Measurement points** | Adjust to garment type (e.g., inseam for pants, rise for bottoms, neck opening for tops) |
| **BOM depth** | Show full BOMs for all styles, or representative BOMs for key styles with a summary table |
| **Flat sketches** | Generate AI flat sketches for each style using the image generation tool. If sketches cannot be generated, describe the style thoroughly in construction details |
| **Fabric swatches** | Generate AI fabric texture images for the swatch grid. If unavailable, use the Fabric Specifications table alone |
| **Season** | Any season/year combination (SS/Resort/Pre-Fall/FW + year) |

## Multi-Format Consistency

When producing output in different formats:

- **DOCX**: Preserve full editability. Use native heading styles, tables, and page breaks. Apply the coral accent color system through styles. Include headers/footers with page numbers. Embed TrueType fonts (Montserrat, Open Sans).
- **PDF**: Render as finalized document. Preserve all visual styling from the style contract including cover page background, decorative elements, color system, and embedded TrueType fonts.
- **PPTX**: Convert each section to a slide. Cover page becomes title slide. Each style spec becomes 1-2 content slides. Tables maintain styling. Sign-off becomes final slide.

## Page Density Guidelines

To match the reference document's information density (33 pages for 10 styles):

- Each style spec spans exactly 2 pages
- Combine tolerance notes, secondary measurements, and colorways on the second page of each style
- Avoid near-empty pages -- consolidate content to eliminate pages with only a few lines
- Section divider pages contain only the H1 title + coral underline + one-line description
- Fabric swatches and Fabric Specifications table share the same page

## Required User Inputs

To generate a complete tech pack, the user must provide (or the agent must infer from context):

- Collection season and year
- Collection name and code
- List of styles with codes, names, categories, and price tiers
- For each style: fabric details, construction specifications, graded measurements, colorways
- Fabric library (materials, weights, origins, care instructions)
- Hardware and trims specifications
- BOM data (materials, quantities, suppliers per style)
- Packaging specifications
- Quality standards and testing requirements

If the user provides incomplete data, generate the document structure with placeholder content clearly marked for completion.
