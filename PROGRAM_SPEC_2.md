# PROGRAM_SPEC_2 - Job-Variation Build Pipeline

Phase 2 extends the existing canonical-resume build system with an automated, per-variation build pipeline. Phase 1 (the canonical build) is documented in `README.md` and implemented in `build_resume_assets.py`. Phase 2 adds full support for building, validating, and packaging job-specific resume variations stored under `jobs/`.

## Table of Contents

- [Scope](#scope)
- [File Layout](#file-layout)
- [CLI Interface](#cli-interface)
- [Agent Tailoring Session](#agent-tailoring-session)
- [Build Pipeline - Variation](#build-pipeline---variation)
- [Validation Rules - Variation](#validation-rules---variation)
- [RESUMES.md Update Rules](#resumesmd-update-rules)
- [Git and Delivery Workflow](#git-and-delivery-workflow)
- [Error Handling](#error-handling)
- [Validation Checklist](#validation-checklist)
- [Troubleshooting](#troubleshooting)

---

## Scope

Phase 2 implements:

1. `build_resume_assets.py --job <variation_path>` - builds one job variation.
2. `build_resume_assets.py --all-jobs` - builds all job variations under `jobs/`.
3. A complete agent tailoring session protocol.
4. Automated `RESUMES.md` updates after every successful variation build.
5. Per-variation ZIP packaging.
6. Git branch creation, commit, PR, and delivery link.

Phase 2 does **not** change the canonical build. Running `python build_resume_assets.py` without arguments continues to rebuild only the canonical resume exactly as Phase 1 defined.

---

## File Layout

### Inputs (edited manually or by agent)

```text
jobs/<Company_Name>/<JOB_TITLE>/JOB.md       # raw job description, unmodified
jobs/<Company_Name>/<JOB_TITLE>/GUIDE.md     # researched best practices, cited
jobs/<Company_Name>/<JOB_TITLE>/BUILD.md     # copy of root README.md at tailoring time
jobs/<Company_Name>/<JOB_TITLE>/README.md    # tailored Markdown resume source
```

### Outputs (generated, never hand-edited)

```text
jobs/<Company_Name>/<JOB_TITLE>/index.html
jobs/<Company_Name>/<JOB_TITLE>/resume.pdf
jobs/<Company_Name>/<JOB_TITLE>/resume_assets.zip
```

### Shared files updated by the pipeline

```text
RESUMES.md   # variation log, most recently updated first
```

### Naming rules

- `<Company_Name>` - CamelCase, no spaces, no special characters. Example: `Claude`, `Anthropic`, `OpenAI`.
- `<JOB_TITLE>` - CamelCase, no spaces. Example: `Applied_AI_Evangelist`, `Head_of_AI`, `AI_Platform_Lead`.
- The combination `<Company_Name>/<JOB_TITLE>` must be unique across the `jobs/` tree.

---

## CLI Interface

### Build one variation

```bash
python build_resume_assets.py --job jobs/<Company_Name>/<JOB_TITLE>
```

- Resolves `<variation_path>/README.md` as the Markdown source.
- Outputs `index.html`, `resume.pdf`, and `resume_assets.zip` inside `<variation_path>`.
- Updates `RESUMES.md`.
- Exits non-zero and prints the first failing check if validation fails.

### Build all variations

```bash
python build_resume_assets.py --all-jobs
```

- Discovers all directories under `jobs/` that contain a `README.md`.
- Builds each variation in the order returned by `Path.glob("jobs/*/*")` sorted alphabetically.
- Prints a pass/fail summary line for each variation.
- Exits non-zero if any variation fails.

### Canonical build (unchanged from Phase 1)

```bash
python build_resume_assets.py
```

- Behavior is identical to Phase 1.
- Does not touch any `jobs/` directories.

---

## Agent Tailoring Session

When a user provides a new job description and asks for a tailored resume, the agent runs the following steps in order. Do not skip steps. Do not reorder steps.

### Step 1 - Scaffold the variation folder

1. Derive `<Company_Name>` and `<JOB_TITLE>` from the job description.
2. Create `jobs/<Company_Name>/<JOB_TITLE>/` if it does not exist.
3. Copy the root `README.md` into `jobs/<Company_Name>/<JOB_TITLE>/BUILD.md`.
4. Save the raw job description text, unmodified, as `jobs/<Company_Name>/<JOB_TITLE>/JOB.md`.

### Step 2 - Research best practices

1. Search for `<CURRENT_MONTH> <CURRENT_YEAR> best practices: apply for <JOB_TITLE>`.
2. Review 3 to 5 sources.
3. Compare sources and condense into a concise bulleted list.
4. Cite each bullet with its source URL.
5. Write the result into `jobs/<Company_Name>/<JOB_TITLE>/GUIDE.md` using this template:

```text
# Best Practices <MONTH_LONG_NAME> <YYYY>

- <best practice>
  Source: [<RESULT TITLE>](<RESULT_URL>)
- <best practice>
  Source: [<RESULT TITLE>](<RESULT_URL>)

---

_last updated: <MONTH_LONG_NAME> <YYYY>_
```

### Step 3 - Extract job requirements

Read `JOB.md` and extract into a structured working note (not committed):

- role title
- required skills
- preferred skills
- tools and platforms
- leadership scope
- outcome language used in the job description
- domain-specific terminology
- exact-match terms that are truthful to include in the resume

### Step 4 - Tailor the resume

1. Start from the canonical resume at `2026-05-05_Resume_AI_Technologist_ATS.md`.
2. Compare extracted job terms against the resume section by section.
3. Apply edits in this priority order:
   1. Professional Experience
   2. Core Skills
   3. Selected AI Leadership Results
   4. Summary
4. Add exact-match terms only where truthful. Do not invent metrics.
5. Enforce all Content Rules, No-Repetition Rules, and ATS Rules from `BUILD.md`.
6. Run a voice pass: direct, clear, human, technical, free of AI-sounding filler.
7. Save the tailored resume as `jobs/<Company_Name>/<JOB_TITLE>/README.md`.

### Step 5 - Build

Run:

```bash
python build_resume_assets.py --job jobs/<Company_Name>/<JOB_TITLE>
```

If the build fails, fix the cause, then re-run. Do not skip validation to force a passing build.

### Step 6 - Visual inspection

Render each page of `resume.pdf` to PNG. Inspect and confirm:

- No clipping.
- No overlapping text.
- No broken glyphs.
- No blank bullet artifacts.
- Header, contact, and URL lines are centered.
- `Selected Applied AI Projects` starts on page 2.
- `FrameBuzz` starts on page 3.

Return the PNG renders to the user in the response.

### Step 7 - Deliver

Run the Git and Delivery Workflow defined below and return the pull request link.

---

## Build Pipeline - Variation

The variation build pipeline mirrors the canonical build pipeline with these differences.

### Inputs

| Item | Path |
|------|------|
| Markdown source | `jobs/<Company_Name>/<JOB_TITLE>/README.md` |
| Base URL for asset resolution | `jobs/<Company_Name>/<JOB_TITLE>/` |

### Outputs

| Item | Path |
|------|------|
| HTML | `jobs/<Company_Name>/<JOB_TITLE>/index.html` |
| PDF | `jobs/<Company_Name>/<JOB_TITLE>/resume.pdf` |
| ZIP | `jobs/<Company_Name>/<JOB_TITLE>/resume_assets.zip` |

### ZIP contents

```text
README.md         (the tailored Markdown source)
index.html
resume.pdf
JOB.md
GUIDE.md
BUILD.md
build_resume_assets.py  (root script, included for reproducibility)
```

### HTML generation

Use the same `build_html_from_markdown()` logic as the canonical build. Source the Markdown from `<variation_path>/README.md` and write the HTML to `<variation_path>/index.html`.

### PDF generation

Use the same WeasyPrint render call as the canonical build. Source the HTML from `<variation_path>/index.html` and write the PDF to `<variation_path>/resume.pdf`. Set `base_url` to `<variation_path>/`.

---

## Validation Rules - Variation

All canonical validation rules apply to every variation. Additionally:

### Page count

PDF must be exactly 3 pages.

### Link parity

Every URL in `<variation_path>/README.md` must appear in `<variation_path>/resume.pdf`. No extra or missing URLs.

### Header text

PDF must contain `Dani Roxberry` and `AI Technologist` in the full text.

### Removed phrase

PDF must not contain the string `Open to San Francisco`.

### Page layout anchors

- `SELECTED APPLIED AI PROJECTS` must appear in page 2 text.
- `FrameBuzz - Founder / Inventor / Chief Technology Officer` must appear in page 3 text.

### File existence

Before packaging, verify all of the following exist:

- `<variation_path>/README.md`
- `<variation_path>/index.html`
- `<variation_path>/resume.pdf`
- `<variation_path>/JOB.md`
- `<variation_path>/GUIDE.md`
- `<variation_path>/BUILD.md`

### Markdown linting

`<variation_path>/README.md` must pass the same Markdown linter as the canonical source.

### HTML linting

`<variation_path>/index.html` must pass the same HTML linter as the canonical HTML.

---

## RESUMES.md Update Rules

After every successful variation build, update `RESUMES.md`.

### Format

Each variation is a level-2 section headed by the ISO date of the most recent build (`YYYY-MM-DD`). Within each date, the variation record is a flat list. Order: most recently updated date first.

```markdown
## <YYYY-MM-DD>

- Company: `<Company_Name>`
- Role: `<JOB_TITLE>`
- Folder: `jobs/<Company_Name>/<JOB_TITLE>/`
- Build Spec: `jobs/<Company_Name>/<JOB_TITLE>/BUILD.md`
- Inputs:
  - `jobs/<Company_Name>/<JOB_TITLE>/JOB.md`
  - `jobs/<Company_Name>/<JOB_TITLE>/GUIDE.md`
- Resume Source:
  - `jobs/<Company_Name>/<JOB_TITLE>/README.md`
- Outputs:
  - `jobs/<Company_Name>/<JOB_TITLE>/index.html`
  - `jobs/<Company_Name>/<JOB_TITLE>/resume.pdf`
- Status: `delivered`
- Notes: <one-line summary of what was tailored>
```

### Update logic

1. If a record for this `<Company_Name>/<JOB_TITLE>` already exists, update its date, status, and notes in place. Move the section to the top if the date changed.
2. If no record exists, prepend a new section above all existing sections.
3. Do not remove any existing records.
4. `Status` values: `draft`, `delivered`. Set to `delivered` after a successful full build + validation.

---

## Git and Delivery Workflow

Run this after a successful build and visual inspection pass.

1. Create a branch named `<YYYY-MM-DD>_<Company_Name>_<JOB_TITLE>` from the current default branch.
2. Stage these files:
   - `jobs/<Company_Name>/<JOB_TITLE>/README.md`
   - `jobs/<Company_Name>/<JOB_TITLE>/BUILD.md`
   - `jobs/<Company_Name>/<JOB_TITLE>/JOB.md`
   - `jobs/<Company_Name>/<JOB_TITLE>/GUIDE.md`
   - `jobs/<Company_Name>/<JOB_TITLE>/index.html`
   - `jobs/<Company_Name>/<JOB_TITLE>/resume.pdf`
   - `jobs/<Company_Name>/<JOB_TITLE>/resume_assets.zip`
   - `RESUMES.md`
3. Commit with the message: `Add <Company_Name> <JOB_TITLE> variation`.
4. Open a pull request. Title: `<Company_Name> - <JOB_TITLE> resume variation`.
5. Return the pull request link to the user.

---

## Error Handling

### Missing README.md

If `<variation_path>/README.md` does not exist, exit with:

```text
ERROR: <variation_path>/README.md not found. Run the agent tailoring session first.
```

### PDF page count wrong

If the PDF is not exactly 3 pages:

1. Reduce margins slightly (step of 0.02in) before cutting content.
2. Reduce section spacing slightly.
3. Shorten lower-priority Earlier Experience text.
4. Remove the least interesting bullets from the job section that spills across pages.
5. Do not remove core AI leadership terms unless absolutely necessary.
6. Re-run the build. Repeat up to 3 times before stopping and reporting.

### Link mismatch

If Markdown and PDF links do not match:

1. Audit `README.md` links.
2. Regenerate HTML from Markdown.
3. Regenerate PDF from HTML.
4. Re-run validation.

### Content repetition detected

If a project name appears in more than one section with the same description:

1. Identify the strongest mention.
2. Reword or remove the weaker mention.
3. Re-run the build.

### Build fails for unknown reason

Print the full traceback. Do not suppress the error. Do not deliver a build that has not passed all validation checks.

---

## Validation Checklist

Before delivering any variation, verify all items below. Items marked **auto** are checked by `build_resume_assets.py --job`. Items marked **visual** require human or agent inspection.

### File existence

- [auto] `README.md` exists in variation folder.
- [auto] `index.html` exists in variation folder.
- [auto] `resume.pdf` exists in variation folder.
- [auto] `resume_assets.zip` exists in variation folder.
- [auto] `JOB.md` exists in variation folder.
- [auto] `GUIDE.md` exists in variation folder.
- [auto] `BUILD.md` exists in variation folder.

### PDF quality

- [auto] PDF page count is exactly 3.
- [auto] PDF text contains `Dani Roxberry` and `AI Technologist`.
- [auto] PDF does not contain the removed hybrid/travel phrase.
- [auto] `SELECTED APPLIED AI PROJECTS` is on page 2.
- [auto] `FrameBuzz - Founder / Inventor / Chief Technology Officer` is on page 3.
- [auto] All Markdown links appear in the PDF.
- [visual] PDF text is selectable.
- [visual] No clipping, overlapping text, blank bullet artifacts, or broken glyphs.
- [visual] Header, contact, and URL lines are centered.

### Content quality

- [visual] Core Skills are alphabetized by bold label.
- [visual] Selected Applied AI Projects are alphabetized by project name.
- [visual] No project name or description is repeated below its first strong mention.
- [visual] All numbers and claims are truthful and preserved from the canonical resume.
- [visual] No AI-sounding filler language.
- [visual] Voice is direct, clear, human, and technical.

### RESUMES.md

- [auto] RESUMES.md contains a record for this variation with `Status: delivered`.

### Git

- [auto] Branch exists and is named `<YYYY-MM-DD>_<Company_Name>_<JOB_TITLE>`.
- [auto] Pull request is open.

---

## Troubleshooting

### PDF spills to 4 pages

1. Reduce `@page` margin by 0.02in on all sides.
2. Reduce `h2` `margin-top` by 1px.
3. Shorten the last two bullets of the least relevant Earlier Experience entry.
4. If still 4 pages, remove the lowest-value bullet from the Experience section that spills.
5. Never remove a term from the ATS vocabulary list unless absolutely necessary.
6. Never remove truthful numbers or claims.

### HTML differs from Markdown content

1. Check that `build_html_from_markdown()` is reading the variation `README.md`, not the canonical source.
2. Confirm `base_url` points to the variation folder, not the root.

### ZIP is missing a file

1. List the ZIP contents with `python -c "import zipfile; zipfile.ZipFile('resume_assets.zip').printdir()"`.
2. Identify which file is missing.
3. Verify the file was generated before the ZIP step.
4. Re-run the full `--job` build.

### RESUMES.md not updated

1. Confirm the build exited with code 0.
2. Confirm `RESUMES.md` is writable.
3. Re-run with `--job`. The update step runs after validation passes.
