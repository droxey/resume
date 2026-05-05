# Resume Build Instructions

## Table of Contents

- [Source of Truth](#source-of-truth)
- [Quick Rebuild](#quick-rebuild)
- [Required Build Order](#required-build-order)
- [Content Rules](#content-rules)
- [No-Repetition Rules](#no-repetition-rules)
- [ATS Rules](#ats-rules)
- [Markdown Rules](#markdown-rules)
- [HTML Rules](#html-rules)
- [PDF Rules](#pdf-rules)
- [LinkedIn Rules](#linkedin-rules)
- [Validation Checklist](#validation-checklist)
- [Customizing for a Specific Job](#customizing-for-a-specific-job)
- [Troubleshooting](#troubleshooting)

---

## Source of Truth

The source of truth for resume content is:

```text
2026-05-05_Resume_AI_Technologist_ATS.md
```

The PDF is generated from the HTML, and the HTML is generated from the Markdown by the build script.

Do not hand-edit the PDF.

---

## Quick Rebuild

From inside the unzipped folder:

```bash
python build_resume_assets.py
```

The script regenerates:

```text
2026-05-05_Resume_AI_Technologist_ATS.html
2026-05-05_Resume_AI_Technologist_ATS.pdf
LINKEDIN.md
README.md
2026-05-05_Resume_AI_Technologist_ATS_assets.zip
```

---

## Required Build Order

Use this order every time.

1. Update the Markdown resume.
2. Audit for repeated project names and repeated bullet claims.
3. Apply the user's voice pass: direct, clear, human, technical, no AI-sounding filler.
4. Regenerate HTML from Markdown.
5. Regenerate PDF from HTML.
6. Regenerate LinkedIn copy blocks.
7. Validate page count, links, typography, and ATS safety.
8. Rebuild ZIP.

---

## Content Rules

- The resume is a generic **AI Technologist / AI Leadership** resume.
- It should work for AI Technologist, Applied AI Leader, Head of AI, AI Platform Lead, AI Transformation Lead, AI Architect, AI Engineering Leader, and agent-systems leadership roles.
- Keep language focused on AI strategy becoming real execution: architecture, code, operations, governance, adoption, and measurable business value.
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
- Project name must be `Skillsport`, not `Skillsport / skillsctl`.
- Do not include the old phrase `Open to San Francisco / New York hybrid schedules and regular travel`.
- Contact and URL lines must be separate from the headline/location line.
- Header, location, phone/email, and URL line must be centered in Markdown, HTML, and PDF.

---

## No-Repetition Rules

Never repeat the same project reference or project description in multiple sections.

Project-reference hierarchy:

1. **Selected AI Leadership Results** can describe a capability or result.
2. **Selected Applied AI Projects** can name and describe specific projects.
3. **Professional Experience** must use capability/outcome language when a project was already named above.
4. **Open Source** must stay broad and must not re-describe the selected projects.
5. **LinkedIn Experience** must not repeat LinkedIn Projects wording.

Specific repetition rules:

- If a project appears in **Selected Applied AI Projects**, avoid repeating its project description in Experience.
- If a project name must appear again for ATS value, reword the sentence completely and make it about business/technical impact, not project features.
- Do not repeat identical metric bullets in both Achievements and Experience unless the second version adds new context.
- Do not repeat `Clincher` as a lower-section project description after Selected Applied AI Projects.
- Do not repeat `GrainDL` as a lower-section project description after Selected Applied AI Projects.
- Do not repeat `Skillsport` as a lower-section project description after Selected Applied AI Projects.
- Avoid repeated phrases like `safe-by-default`, `deployment harness`, `production-grade`, `developer mindshare`, and `working prototypes` unless each use adds a distinct point.

---

## ATS Rules

- Single-column layout only.
- No tables.
- No icons.
- No graphics.
- No sidebars.
- No text boxes.
- No image-only text.
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
- Put key terms in Summary, Core Skills, Results, and Experience, not just in a skills dump.
- Keep bullets outcome-oriented and specific.
- Use ASCII punctuation where possible.
- Preserve selectable text and parseable hyperlinks in the PDF.

---

## Markdown Rules

- Markdown must stay copy-paste friendly.
- Header block must use:

```html
<div align="center">
...
</div>
```

- Header block must include:
  - name
  - headline
  - location
  - phone/email line
  - URL line
- Core Skills must be alphabetized by bold label.
- Selected Applied AI Projects must be alphabetized by project name.
- Use Markdown links for all URLs.
- Patent section must be:

```markdown
## Patents

### US20140199046A1 - Conversations on Time-Shifted Content

**[Invented live-streaming video technology](https://www.google.com/patents/US20140199046)** for timestamp-anchored conversations and viewer interaction on live and recorded media.
```

---

## HTML Rules

- HTML is generated from Markdown by `build_resume_assets.py`.
- Do not manually change content in HTML unless the Markdown changes first.
- HTML must preserve all Markdown links.
- Header must be centered.
- Typography must be simple and ATS-safe:
  - Arial / Helvetica
  - black text
  - blue underlined links
  - no decorative graphics
- Use Letter page size.
- Use compact margins that still leave smooth reading room.
- Section headings must be uppercase in the PDF/HTML rendering.
- Heading spacing must be readable but compact enough to keep the PDF to 3 pages.
- `Selected Applied AI Projects` must start on page 2.
- `FrameBuzz` must start on page 3.

---

## PDF Rules

- PDF must be generated from HTML.
- PDF must be exactly 3 pages.
- PDF must preserve all Markdown links.
- PDF links must match Markdown links exactly.
- PDF text must be selectable and parseable.
- No blank bullet artifacts.
- No clipping.
- No overlapping text.
- No broken glyphs.
- No content should unexpectedly move pages except intended layout controls:
  - Selected Applied AI Projects starts page 2.
  - FrameBuzz starts page 3.
- Render all pages to PNG and visually inspect before delivery.

---

## LinkedIn Rules

- `LINKEDIN.md` is a step-by-step copy/paste guide for updating LinkedIn.
- It must include a Table of Contents.
- It must include discrete copy blocks for:
  - profile basics
  - headline
  - about
  - featured links
  - each experience entry
  - projects
  - patent
  - education
  - skills
- LinkedIn copy should use plain text blocks, not resume Markdown formatting.
- LinkedIn Projects may name and describe projects.
- LinkedIn Experience should avoid repeating the same project descriptions.
- LinkedIn copy should stay human, direct, and technical.

---

## Validation Checklist

Before delivering assets, verify:

- Markdown exists.
- HTML exists.
- PDF exists.
- LinkedIn copy exists.
- README exists.
- Build script exists.
- ZIP exists.
- PDF page count is exactly 3.
- Markdown and PDF links match exactly.
- PDF text is selectable.
- Removed hybrid/travel phrase did not reappear.
- Header/contact/URL lines are centered.
- Selected Applied AI Projects starts on page 2.
- FrameBuzz starts on page 3.
- Core Skills are alphabetized.
- Selected Applied AI Projects are alphabetized.
- Project names/descriptions are not repeated below their first strong mention.
- ZIP includes every required asset.

---

## Customizing for a Specific Job

When tailoring this resume to a particular job:

1. Paste the full job description into the working chat.
2. Extract role title, required skills, preferred skills, tools, leadership scope, and outcome language.
3. Compare job language against the resume.
4. Add exact-match terms only where truthful.
5. Prefer edits in this order:
   1. Professional Experience
   2. Core Skills
   3. Selected AI Leadership Results
   4. Summary
6. Do not invent metrics.
7. Do not repeat project descriptions.
8. Keep the resume generic enough for leadership unless applying to a very specific role.
9. Rebuild with:

```bash
python build_resume_assets.py
```

10. Validate before sending.

---

## Troubleshooting

If PDF goes to 4 pages:

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
4. Search for repeated metrics and repeated first phrases.

