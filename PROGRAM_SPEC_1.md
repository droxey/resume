# PROGRAM_SPEC_1

## Title

Canonical Resume Asset Build Pipeline

## Objective

Implement and maintain a single-root build pipeline that converts the canonical resume Markdown source into synchronized HTML and PDF artifacts, validates required companion documents, and packages the root resume set into a ZIP archive, with rules that preserve ATS safety, link integrity, page layout, and artifact completeness.

## Primary Outcome

Given the canonical source file:

```text
2026-05-05_Resume_AI_Technologist_ATS.md
```

the program must generate these root-level outputs:

```text
2026-05-05_Resume_AI_Technologist_ATS.html
2026-05-05_Resume_AI_Technologist_ATS.pdf
2026-05-05_Resume_AI_Technologist_ATS_assets.zip
```

The program must also validate and package these required companion documents:

```text
LINKEDIN.md
README.md
```

## Scope

This specification covers the root resume build system only.

It includes:

- canonical source file handling
- Markdown-to-HTML transformation
- HTML-to-PDF generation
- validation of structural and layout invariants
- packaging final artifacts into a ZIP archive

It does not include:

- job-specific variation folders
- remote deployment
- browser-based editing
- hand-editing generated HTML or PDF output

## Source of Truth

The canonical resume Markdown file is the only editable source for generated root artifacts.

Rules:

- `2026-05-05_Resume_AI_Technologist_ATS.md` is the source of truth
- generated HTML must be derived from that Markdown file
- generated PDF must be derived from that HTML file
- ZIP contents must be derived from the validated root artifacts
- generated HTML, PDF, and ZIP files must never be hand-edited

## Program Entry Point

The build system must provide a single command-line entry point:

```bash
python build_resume_assets.py
```

Running this command from the repository root must execute the full pipeline in this order:

1. read the canonical Markdown source
2. generate root HTML output
3. generate root PDF output
4. validate generated and required artifacts
5. package artifacts into a ZIP archive
6. print a success message containing the ZIP filename

If any required validation fails, the program must exit with an error and must not silently report success.

## Required Files

### Inputs

- `2026-05-05_Resume_AI_Technologist_ATS.md`
- `LINKEDIN.md`
- `README.md`

### Generated outputs

- `2026-05-05_Resume_AI_Technologist_ATS.html`
- `2026-05-05_Resume_AI_Technologist_ATS.pdf`
- `2026-05-05_Resume_AI_Technologist_ATS_assets.zip`

### Program file

- `build_resume_assets.py`

## Functional Requirements

### 1. Markdown ingestion

The program must:

- read the canonical Markdown file as UTF-8 text
- process the file line-by-line
- treat blank lines as separators, not as standalone rendered blocks

### 2. Supported Markdown features

The renderer only needs to support the resume’s required subset of Markdown.

It must support:

- level-1 headings using `# `
- level-2 headings using `## `
- level-3 headings using `### `
- unordered list items using `- `
- fenced header wrapper using:

```html
<div align="center">
...
</div>
```

- inline code using backticks
- bold text using `**bold**`
- Markdown links using `[label](https://example.com)`
- horizontal rules using `---`

The implementation does not need to be a general-purpose Markdown engine. It must be deterministic for the repository’s resume format.

### 3. HTML generation

The program must generate a complete HTML document with:

- `<!DOCTYPE html>`
- `<html lang="en">`
- UTF-8 charset metadata
- viewport metadata
- a `<title>` element
- inline CSS required for PDF-safe rendering
- a `<main>` wrapper around the rendered resume body

The HTML renderer must preserve link destinations from the Markdown source.

### 4. Header rendering

When the Markdown contains:

```html
<div align="center">
```

the renderer must open a centered resume header container.

Within this container:

- the level-1 heading must render as the main name heading
- bold-only lines must render as the title line
- remaining lines must render as centered contact lines

The closing `</div>` must terminate the header container.

### 5. Section rendering

The renderer must:

- map `##` headings to HTML section headings
- map `###` headings to subsection headings
- open and close unordered lists correctly
- escape text safely before applying inline formatting
- avoid malformed nesting between paragraphs, lists, and job sections

### 6. Experience section grouping

Within these sections:

- `Professional Experience`
- `Earlier Experience`

each `###` heading must begin a distinct job section container.

The renderer must close any currently open job section before opening a new one.

### 7. Forced page layout controls

The HTML must enforce these layout rules:

- `Selected Applied AI Projects` must start on page 2
- `FrameBuzz - Founder / Inventor / Chief Technology Officer` must start on page 3

The implementation may use CSS classes and page-break controls to enforce these requirements.

### 8. HTML styling requirements

The generated HTML and printable layout must use:

- a single-column layout
- Arial or Helvetica style typography
- black body text
- blue underlined links
- no tables
- no icons
- no graphics
- no sidebars
- no text boxes
- no decorative elements that reduce ATS safety
- Letter page size
- compact margins suitable for a 3-page PDF
- uppercase rendered section headings in HTML/PDF

### 9. PDF generation

The program must generate the PDF from the generated HTML file.

The resulting PDF must:

- be exactly 3 pages
- preserve selectable text
- preserve clickable hyperlinks
- match the Markdown link set exactly
- avoid clipping, overlap, broken glyphs, and blank bullet artifacts

### 10. Validation requirements

Before packaging, the program must validate all of the following.

#### Required file presence

- `LINKEDIN.md` exists
- `README.md` exists

#### Documentation structure

- `LINKEDIN.md` contains `## Table of Contents`
- `README.md` contains `## Table of Contents`

#### PDF structure

- the PDF page count is exactly 3
- the PDF contains resume header text including `Dani Roxberry`
- the PDF contains resume title text including `AI Technologist`

#### Content guardrails

- the phrase `Open to San Francisco` must not appear in the generated PDF text

#### Layout invariants

- page 2 must contain `SELECTED APPLIED AI PROJECTS`
- page 3 must contain `FrameBuzz - Founder / Inventor / Chief Technology Officer`

#### Link integrity

- all unique Markdown hyperlinks from the source file must match all unique PDF hyperlinks exactly

Validation failures must raise a hard error with a specific message describing the failed invariant.

### 11. Packaging requirements

After successful validation, the program must create:

```text
2026-05-05_Resume_AI_Technologist_ATS_assets.zip
```

The ZIP archive must include exactly these root-level files:

- `2026-05-05_Resume_AI_Technologist_ATS.md`
- `2026-05-05_Resume_AI_Technologist_ATS.html`
- `2026-05-05_Resume_AI_Technologist_ATS.pdf`
- `LINKEDIN.md`
- `README.md`
- `build_resume_assets.py`

Files must be stored in the ZIP by filename, not by absolute path.

## Non-Functional Requirements

The implementation must be:

- deterministic across repeated runs on unchanged input
- local-only, with no network dependency
- readable and maintainable as a small single-script utility
- strict about validation failures
- safe for ATS-oriented output constraints

## Error Handling

The program must fail fast when:

- the canonical Markdown source is missing
- required companion documents are missing
- PDF generation fails
- layout validation fails
- link validation fails
- ZIP creation fails

Errors must not be swallowed. The build must stop on the first unrecoverable failure.

## Implementation Constraints

- use Python
- keep the implementation in `build_resume_assets.py`
- use local filesystem paths rooted at the repository root
- keep the HTML renderer purpose-built for this resume format
- do not replace the focused renderer with a large generalized content system unless required by a future spec

## Acceptance Criteria

The program is complete when all of the following are true:

1. Running `python build_resume_assets.py` from the repository root produces the required HTML, PDF, and ZIP files.
2. The generated PDF is exactly 3 pages.
3. Page 2 begins the selected projects section.
4. Page 3 begins the FrameBuzz experience entry.
5. All Markdown hyperlinks are preserved exactly in the PDF.
6. `LINKEDIN.md` and `README.md` are present and each includes a table of contents heading.
7. The generated ZIP contains the canonical Markdown, generated outputs, and build script.
8. The build exits with a clear error if any invariant is violated.

## Delivery Notes

This specification is implementation-ready. A compliant implementation should be verifiable entirely through local execution of the build command and inspection of the generated artifacts and validation behavior.
