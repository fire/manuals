---
title: Archival file naming convention for committed assets
date: 2026-06-06
status: accepted
tier: baseline
---

## Context and Problem Statement

The manuals repo now commits binary assets alongside prose, starting with
screenshots under `decisions/attachments/`. Ad-hoc names like `image.png` collide,
sort poorly, and lose their provenance once they leave the page that referenced
them. What naming convention should committed assets follow so they stay unique,
sortable, and self-describing?

## Decision Drivers

- Names should be unique and not collide across decisions.
- Names should sort chronologically and read as self-describing.
- Names should survive being copied out of the repo (provenance in the name).
- The convention should match established digital-preservation guidance.

## Considered Options

- Keep source names (`image.png`, `screenshot (1).png`).
- Content hash names (`a1b2c3.png`).
- A Library of Congress style descriptive convention.

## Decision Outcome

Chosen option: "A Library of Congress style descriptive convention", because it
follows recognized preservation guidance and yields names that sort and explain
themselves.

The pattern:

```
YYYYMMDD_project_description_NNNN.ext
```

Following the Library of Congress file-naming guidance:

- Lowercase ASCII only; no spaces or special characters.
- ISO 8601 date first (`YYYYMMDD`) so names sort chronologically.
- Facets separated by underscores (`_`); words within a facet by hyphens (`-`).
- A zero-padded sequence (`NNNN`) to keep same-day captures unique and ordered.
- Descriptive but reasonably short.

Example, used for the first committed screenshot:

```
20260606_vsekai-mpf_xr-grid-debug-orbs_0001.png
```

Each committed asset also gets a BibTeX entry in `references.bib` recording its
capture date and archived path, so the References page lists it.

### Consequences

- Good: assets are unique, sort by date, and carry their provenance in the name.
- Good: the convention matches preservation practice and is mechanical to apply.
- Bad: names are longer than source names, and renaming on import is a manual step.

### Confirmation

Assets under `decisions/attachments/` match `YYYYMMDD_project_description_NNNN.ext`
and have a matching `references.bib` entry. The first example is
`20260606_vsekai-mpf_xr-grid-debug-orbs_0001.png`, cited from the
[presence-demo decision](20260606-multiplayer-presence-demo-orbs.md).

## More Information

Based on the Library of Congress guidance on file naming for digital
preservation (descriptive, no spaces, lowercase, ISO dates, zero-padded
sequences).
