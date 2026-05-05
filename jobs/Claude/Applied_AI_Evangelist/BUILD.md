# [Dani's Resume](https://droxey.com/resume)

Reusable workflow for generating ATS-safe, job-tailored resume variants from a canonical Markdown source.

## Overview

This repository contains:

- the canonical Markdown resume
- a build script that generates HTML, PDF, LinkedIn copy, and packaged assets
- formatting, ATS, validation, and packaging rules for tailored resume variants

## Table of Contents

- [Overview](#overview)
- [Source of Truth](#source-of-truth)
- [File Roles](#file-roles)
- [Quick Rebuild](#quick-rebuild)
- [Build Workflow](#build-workflow)
- [Git and Delivery Workflow](#git-and-delivery-workflow)
- [Tailoring Workflow](#tailoring-workflow)
- [Content Rules](#content-rules)
- [No-Repetition Rules](#no-repetition-rules)
- [ATS Rules](#ats-rules)
- [Markdown Rules](#markdown-rules)
- [HTML Rules](#html-rules)
- [PDF Rules](#pdf-rules)
- [LinkedIn Rules](#linkedin-rules)
- [Validation Checklist](#validation-checklist)
- [Troubleshooting](#troubleshooting)

---

## Source of Truth

The canonical resume source is:

```text
2026-05-05_Resume_AI_Technologist_ATS.md
```

All generated artifacts must be derived from this Markdown source through the build script.

Do not hand-edit generated HTML or PDF files.

---

## File Roles

### Edited manually

- `2026-05-05_Resume_AI_Technologist_ATS.md` - canonical resume source
- `jobs/Company_Name/JOB_TITLE/BUILD.md` - variation-local build spec copied from the root `README.md`
- `jobs/Company_Name/JOB_TITLE/JOB.md` - pasted job description for a tailored variant
- `jobs/Company_Name/JOB_TITLE/GUIDE.md` - best-practice notes for the target role
- `jobs/Company_Name/JOB_TITLE/README.md` - tailored Markdown resume source
- `README.md` - repository documentation and operating spec

### Generated

- `2026-05-05_Resume_AI_Technologist_ATS.html`
- `2026-05-05_Resume_AI_Technologist_ATS.pdf`
- `LINKEDIN.md`
- `2026-05-05_Resume_AI_Technologist_ATS_assets.zip`
- `jobs/Claude/Applied_AI_Evangelist/index.html`
- `jobs/Claude/Applied_AI_Evangelist/resume.pdf`

### Never hand-edit

- generated HTML files
- generated PDF files
- generated ZIP packages

---

## Quick Rebuild

Run from the repository root:

```bash
python build_resume_assets.py
```

This regenerates:

```text
2026-05-05_Resume_AI_Technologist_ATS.html
2026-05-05_Resume_AI_Technologist_ATS.pdf
LINKEDIN.md
README.md
2026-05-05_Resume_AI_Technologist_ATS_assets.zip
```

---

## Build Workflow

Use this order every time:

1. Update the Markdown resume.
2. Audit for repeated project names and repeated bullet claims.
3. Apply the user's voice pass: direct, clear, human, technical, and free of AI-sounding filler.
4. Regenerate HTML from Markdown.
5. Regenerate PDF from HTML.
6. Regenerate LinkedIn copy blocks.
7. Validate page count, links, typography, and ATS safety.

---

## Git and Delivery Workflow

After build and validation pass:

1. Create a branch named `YYYY-MM-DD_JOB_NAME`.
2. Commit the updated source and generated artifacts.
3. Open a pull request.
4. Return the pull request link to the user.

---

## Tailoring Workflow

When customizing this resume for a specific job:

1. Create a folder at `jobs/Company_Name/JOB_TITLE/`.
2. Copy the root `README.md` into `jobs/Company_Name/JOB_TITLE/BUILD.md`.
3. Save the job description as `jobs/Company_Name/JOB_TITLE/JOB.md`.
4. Research current best practices for the target role and summarize them in `jobs/Company_Name/JOB_TITLE/GUIDE.md`.
5. Use `BUILD.md`, `JOB.md`, and `GUIDE.md` as the variation-local instruction set.
6. Start from the canonical resume source and tailor it using the local instruction set.
7. Save the tailored Markdown resume as `jobs/Company_Name/JOB_TITLE/README.md`.
8. Generate HTML from the tailored Markdown and save it as `jobs/Company_Name/JOB_TITLE/index.html`.
9. Lint and fix Markdown and HTML issues.
10. Generate `jobs/Company_Name/JOB_TITLE/resume.pdf` from the linted HTML.
11. Update `RESUMES.md` with the variation record, ordered by most recently updated date first.
12. Validate links, layout, page count, ATS safety, and repetition rules before delivery.

Use this `GUIDE.md` template. Replace `$MONTH_LONG_NAME` and `$YYYY` with the current month and year, for example `May 2026`.

```text
# Best Practices $MONTH_LONG_NAME $YYYY

- Best practice 1
  Source: [RESULT TITLE]($RESULT_URL)
- Best practice 2
  Source: [RESULT TITLE]($RESULT_URL)

---

_last updated: $MONTH_LONG_NAME $YYYY_
```

Research guidance:

- Search for `$CURRENT_MONTH $CURRENT_YEAR best practices: apply for $JOB_TITLE`.
- Review 3 to 5 sources.
- Compare them.
- Condense the results into a concise bulleted list.
- Cite each bullet with its source.

Tailoring guidance:

1. Extract the role title, required skills, preferred skills, tools, leadership scope, and outcome language.
2. Compare the job language against the resume.
3. Add exact-match terms only where truthful.
4. Prefer edits in this order:
   1. Professional Experience
   2. Core Skills
   3. Selected AI Leadership Results
   4. Summary
5. Do not invent metrics.
6. Do not repeat project descriptions.
7. Keep the resume generic enough for leadership unless applying to a very specific role.
8. Rebuild with:

```bash
python build_resume_assets.py
```

9. Validate before sending.

---

## Content Rules

- The resume is a generic **AI Technologist / AI Leadership** resume.
- It should work for AI Technologist, Applied AI Leader, Head of AI, AI Platform Lead, AI Transformation Lead, AI Architect, AI Engineering Leader, and agent-systems leadership roles.
- Keep language focused on turning AI strategy into execution: architecture, code, operations, governance, adoption, and measurable business value.
- Preserve truthful numbers and claims:
  - 22+ years shipping production software
  - 9 years teaching and developer enablement
  - 4 startups
  - 2x CTO
  - 1 U.S. patent
  - 500+ technical talks / sessions
  - 60+ engineers across 5 courses and twice-yearly hackathons
  - 200+ submissions weekly
  - 80% feedback turnaround reduction
  - 50% course development time reduction
  - 16-course applied CS program
  - 60+ GitHub stars and 100+ forks
  - 250+ junior engineers coached at Make School
- Keep the patent link in the patent description, not the patent heading.
- Use `Skillsport`, not `Skillsport / skillsctl`.
- Keep contact and URL lines separate from the headline and location line.
- Center the header, location, phone/email, and URL line in Markdown, HTML, and PDF.

---

## No-Repetition Rules

Never repeat the same project reference or project description across sections.

Project-reference hierarchy:

1. **Selected AI Leadership Results** can describe a capability or result.
2. **Selected Applied AI Projects** can name and describe specific projects.
3. **Professional Experience** must use capability or outcome language when a project was already named above.
4. **Open Source** must stay broad and must not re-describe the selected projects.
5. **LinkedIn Experience** must not repeat LinkedIn Projects wording.

Specific repetition rules:

- If a project appears in **Selected Applied AI Projects**, avoid repeating its project description in Experience.
- If a project name must appear again for ATS value, reword the sentence completely and make it about business or technical impact, not project features.
- Do not repeat identical metric bullets in both Achievements and Experience unless the second version adds new context.
- Do not repeat `Clincher` as a lower-section project description after Selected Applied AI Projects.
- Do not repeat `GrainDL` as a lower-section project description after Selected Applied AI Projects.
- Do not repeat `Skillsport` as a lower-section project description after Selected Applied AI Projects.
- Avoid repeated phrases like `safe-by-default`, `deployment harness`, `production-grade`, `developer mindshare`, and `working prototypes` unless each use adds a distinct point.

Manual verification guidance:

1. Search for each selected project name.
2. Keep the strongest mention.
3. Reword or remove lower mentions.
4. Search for repeated metrics and repeated opening phrases.

---

## ATS Rules

- Use a single-column layout only.
- Use no tables.
- Use no icons.
- Use no graphics.
- Use no sidebars.
- Use no text boxes.
- Use no image-only text.
- Use standard headers:
  - Summary
  - Core Skills
  - Selected AI Leadership Results
  - Selected Applied AI Projects
  - Professional Experience
  - Earlier Experience
  - Education
  - Patents
  - Open Source
- Use exact AI leadership vocabulary when true:
  - AI strategy
  - applied AI
  - AI transformation
  - AI platform
  - AI infrastructure
  - LLMOps
  - MLOps
  - model lifecycle
  - AI observability
  - guardrails
  - responsible AI
  - governance
  - production AI deployment
  - RAG
  - agentic workflows
  - multi-agent systems
  - model routing
  - evaluation loops
  - prompt systems
  - cloud-native architecture
  - distributed systems
  - stakeholder alignment
  - business outcomes
- Put key terms in Summary, Core Skills, Results, and Experience, not only in a skills dump.
- Keep bullets outcome-oriented and specific.
- Use ASCII punctuation where possible.
- Preserve selectable text and parseable hyperlinks in the PDF.

---

## Markdown Rules

- Keep Markdown copy/paste friendly.
- Use this header block:

```html
<div align="center">
...
</div>
```

- Include these items in the header block:
  - name
  - headline
  - location
  - phone/email line
  - URL line
- Alphabetize Core Skills by bold label.
- Alphabetize Selected Applied AI Projects by project name.
- Use Markdown links for all URLs.
- Use this patent section:

````markdown
## Patents

### US20140199046A1 - Conversations on Time-Shifted Content

**[Invented live-streaming video technology](https://www.google.com/patents/US20140199046)** for timestamp-anchored conversations and viewer interaction on live and recorded media.
````

---

## HTML Rules

- Generate HTML from Markdown with `build_resume_assets.py`.
- Do not manually change HTML content unless the Markdown changes first.
- Preserve all Markdown links in HTML.
- Center the header.
- Use simple, ATS-safe typography:
  - Arial / Helvetica
  - black text
  - blue underlined links
  - no decorative graphics
- Use Letter page size.
- Use compact margins that still leave smooth reading room.
- Render section headings in uppercase in HTML and PDF.
- Keep heading spacing readable but compact enough to hold the PDF to 3 pages.
- Start `Selected Applied AI Projects` on page 2.
- Start `FrameBuzz` on page 3.

---

## PDF Rules

- Generate the PDF from HTML.
- Keep the PDF to exactly 3 pages.
- Preserve all Markdown links in the PDF.
- Match PDF links exactly to Markdown links.
- Keep PDF text selectable and parseable.
- Use no blank bullet artifacts.
- Use no clipping.
- Use no overlapping text.
- Use no broken glyphs.
- Do not let content move unexpectedly across pages except for these intended layout controls:
  - `Selected Applied AI Projects` starts on page 2.
  - `FrameBuzz` starts on page 3.
- Render all pages to PNG and inspect them visually before delivery.
- Return PNGs to the user in the response.

---

## LinkedIn Rules

- `LINKEDIN.md` is a step-by-step copy/paste guide for updating LinkedIn.
- Include a Table of Contents.
- Include discrete copy blocks for:
  - profile basics
  - headline
  - about
  - featured links
  - each experience entry
  - projects
  - patent
  - education
  - skills
- Use plain-text blocks, not resume Markdown formatting.
- LinkedIn Projects may name and describe projects.
- LinkedIn Experience should avoid repeating the same project descriptions.
- Keep LinkedIn copy human, direct, and technical.

---

## Validation Checklist

Before delivery, verify the following.

### Automated checks

- Markdown exists.
- HTML exists.
- PDF exists.
- LinkedIn copy exists.
- README exists.
- Build script exists.
- ZIP exists.
- PDF page count is exactly 3.
- Markdown files pass a Markdown linter.
- HTML files pass an HTML linter.

### Manual or visual checks

- Markdown and PDF links match exactly.
- PDF text is selectable.
- The removed hybrid/travel phrase did not reappear.
- Header, contact, and URL lines are centered.
- `Selected Applied AI Projects` starts on page 2.
- `FrameBuzz` starts on page 3.
- Core Skills are alphabetized.
- Selected Applied AI Projects are alphabetized.
- Project names and descriptions are not repeated below their first strong mention.
- PNG renders of all PDF pages have been visually inspected before delivery.

---

## Troubleshooting

If the PDF goes to 4 pages:

1. Reduce margins slightly before cutting content.
2. Reduce section spacing slightly.
3. Shorten lower-priority Earlier Experience text.
4. Remove the least interesting bullets from the job that spills across pages.
5. Do not remove core AI leadership terms unless absolutely necessary.

If links do not match:

1. Check Markdown links first.
2. Regenerate HTML from Markdown.
3. Regenerate PDF from HTML.
4. Re-run script validation.

If content repeats:

1. Search for each selected project name.
2. Keep the strongest mention.
3. Reword or remove lower mentions.
4. Search for repeated metrics and repeated opening phrases.
