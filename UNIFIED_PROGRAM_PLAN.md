# UNIFIED PROGRAM PLAN

## Goal
Create one cohesive build system that:
1. Preserves the existing canonical resume pipeline exactly.
2. Adds job-variation pipelines under `jobs/`.
3. Enforces deterministic validation, packaging, and delivery workflow.

## Constraints
- `python build_resume_assets.py` (no args) must remain canonical-only behavior.
- Canonical source of truth remains `2026-05-05_Resume_AI_Technologist_ATS.md`.
- Generated files (`.html`, `.pdf`, `.zip`) are never hand-edited.
- Variation builds must use `jobs/<Company>/<Job>/README.md` as source and produce outputs in the same folder.
- Validation failures must fail fast with non-zero exit status.

## Spec Comparison (PROGRAM_SPEC_1 vs PROGRAM_SPEC_2)

### What matches cleanly
- Both define deterministic, scripted build flow from Markdown -> HTML -> PDF -> ZIP.
- Both require validation before packaging success.
- Both require ATS-safe formatting and page-layout anchors.
- Both assume `build_resume_assets.py` is the single build entry point.

### Additive extensions in Spec 2
- New CLI options:
  - `--job jobs/<Company>/<Job>`
  - `--all-jobs`
- Variation-specific input/output conventions.
- Variation ZIP content requirements.
- Additional variation validation (page count, phrase removal, link parity, anchors).
- `RESUMES.md` update automation.

### Potential conflicts and resolution
1. **Scope conflict:** Spec 1 excludes job-specific variations; Spec 2 adds them.
   - **Resolution:** Keep Phase 1 as default path. Add Phase 2 only behind explicit CLI flags.

2. **Validation baseline ambiguity:** Spec 2 says canonical rules apply to variations, but canonical rules may reference canonical filenames.
   - **Resolution:** Refactor validators into reusable content/layout checks parameterized by source/output paths.

3. **Delivery workflow in spec vs script boundary:** Spec 2 includes git/PR delivery steps, which are process concerns.
   - **Resolution:** Keep build script focused on build + validate + package + update `RESUMES.md`; keep git/PR as operational workflow.

## Unified Execution Model

### Mode A: Canonical build (default)
Command:
```bash
python build_resume_assets.py
```
Pipeline:
1. Load canonical Markdown.
2. Generate canonical HTML.
3. Generate canonical PDF.
4. Validate canonical artifacts.
5. Package canonical ZIP.
6. Print success with ZIP filename.

### Mode B: Single variation build
Command:
```bash
python build_resume_assets.py --job jobs/<Company>/<Job>
```
Pipeline:
1. Resolve variation directory and `README.md`.
2. Generate `index.html`.
3. Generate `resume.pdf`.
4. Run shared + variation-specific validations.
5. Package `resume_assets.zip` with required files.
6. Update `RESUMES.md` (prepend newest entry).
7. Print success with variation ZIP filename.

### Mode C: Build all variations
Command:
```bash
python build_resume_assets.py --all-jobs
```
Pipeline:
1. Discover `jobs/*/*` folders containing `README.md`.
2. Sort alphabetically.
3. Build each variation via Mode B internals.
4. Print per-variation pass/fail summary.
5. Exit non-zero if any variation fails.

## Implementation Plan (Minimal, Safe Sequence)

### Phase 1: CLI and routing
- Add argument parsing for `--job` and `--all-jobs`.
- Enforce mutual exclusivity with default canonical path.

### Phase 2: Refactor shared pipeline primitives
- Introduce reusable functions:
  - `build_html_from_markdown(src_md, out_html)`
  - `build_pdf_from_html(src_html, out_pdf, base_url)`
  - `validate_common(...)`
  - `package_zip(...)`
- Keep canonical behavior path byte-for-byte equivalent where possible.

### Phase 3: Variation build support
- Implement per-variation path resolver.
- Implement variation packaging manifest:
  - `README.md`, `index.html`, `resume.pdf`, `JOB.md`, `GUIDE.md`, `BUILD.md`, `build_resume_assets.py`.

### Phase 4: Variation-specific validation
- Exact 3-page PDF check.
- URL parity: Markdown URLs == PDF URLs.
- Required header text checks.
- Removed phrase check (`Open to San Francisco` absent).
- Page anchor checks:
  - `SELECTED APPLIED AI PROJECTS` on page 2.
  - `FrameBuzz - Founder / Inventor / Chief Technology Officer` on page 3.

### Phase 5: `RESUMES.md` logging
- Prepend successful variation builds with timestamp + path + artifact status.
- Ensure idempotent formatting.

### Phase 6: Failure model hardening
- Fail fast on first blocking validation error for single build.
- Continue aggregation for `--all-jobs`, then return non-zero if any failure.

## Acceptance Criteria
- Canonical command still only touches root canonical artifacts.
- `--job` generates expected variation outputs and ZIP manifest.
- `--all-jobs` iterates deterministic set and exits correctly on mixed outcomes.
- Variation validations enforce all stated checks.
- `RESUMES.md` updates only on successful variation builds.

## Recommendation: What to do next
1. **Implement Phase 1 + Phase 2 first** (CLI routing + shared primitives) to reduce regression risk.
2. Add **one golden-path test run**:
   - canonical build
   - one known-good variation build
3. Then implement variation-only validations and `RESUMES.md` updates.
4. Finally run `--all-jobs` as integration verification.

This sequence gives the quickest safe path to shipping Phase 2 without breaking Phase 1.
