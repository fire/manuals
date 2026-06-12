# manuals

Architecture decisions, changelogs, and reference documentation for the v-sekai-multiplayer-fabric stack. Published as a Quarto website.

## Build

```sh
uv sync           # install Python deps
quarto render     # build to _site/
quarto preview    # local preview
```

## Adding a decision

Create a Markdown file in `decisions/` named `YYYYMMDD-short-title.md` following the
[MADR](https://adr.github.io/madr/) template:

```markdown
---
title: Short title representative of the problem and solution
date: YYYY-MM-DD
status: proposed | accepted | rejected | deprecated | superseded by YYYYMMDD-...
---

## Context and Problem Statement

## Decision Drivers

## Considered Options

## Decision Outcome

Chosen option: "...", because ...

### Consequences

### Confirmation
```

Optional MADR sections (`Pros and Cons of the Options`, `More Information`) may follow.
To supersede an earlier decision, set the old file's `status` to `superseded by <new filename>`
and link back from the new one.

A decision that records a product feature also carries a `tier` in its frontmatter —
`proof of concept`, `baseline`, or `stretch` — per the feature classification decision.
Process and infrastructure decisions carry no tier. The decisions index shows the
`tier` and `status` columns.

## Adding a changelog entry

```sh
elixir create_changelog_entry.exs        # uses today's date
elixir create_changelog_entry.exs 20260512
```

## Checks

Pull requests run `prek` (prettier on Markdown) and a static tropes check, and land
through the `main` merge queue. Run them locally before pushing:

```sh
prek run --all-files          # prettier + tropes (scripts/check_tropes.sh)
```

The tropes check enforces [tropes.fyi](https://tropes.fyi/) style: no negative
parallelism (`not X, but/it's Y`) and no bold lead-in list items (`- **Term:** ...`).

## Assets

Commit images under `decisions/attachments/` using the archival naming convention
`YYYYMMDD_project_description_NNNN.ext` (lowercase, no spaces, ISO date, zero-padded
sequence), and add a matching `references.bib` entry. See the naming-convention decision.

## Key files

| Path                         | Purpose                       |
| ---------------------------- | ----------------------------- |
| `_quarto.yml`                | Site config                   |
| `index.md`                   | Landing page                  |
| `decisions/`                 | Architecture Decision Records |
| `decisions.qmd`              | ADR index                     |
| `changelog/`                 | Changelog entries by year     |
| `changelog.qmd`              | Changelog index               |
| `create_changelog_entry.exs` | Generate new changelog entry  |

## Conventions

- Decision filenames: `YYYYMMDD-kebab-title.md`
- Feature decisions carry a `tier:` (`proof of concept` / `baseline` / `stretch`)
- Changelog filenames: `YYYYMMDD-deck-log.md` inside `changelog/YYYY/`
- Asset filenames: `YYYYMMDD_project_description_NNNN.ext` in `decisions/attachments/`, with a `references.bib` entry
- Prose follows tropes.fyi style; `prek run --all-files` must pass before pushing
- No hardcoded absolute filesystem paths; use env vars or placeholders (e.g. `$GODOT_SRC`)
- Do not commit `_site/` — it is build output
- Commit style: sentence case, no `type(scope):` prefix
- One concern per PR; PRs land via the `main` merge queue
