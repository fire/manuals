---
title: Feature classification — proof of concept, baseline, stretch
date: 2026-06-06
status: accepted
tier: baseline
decision-makers: K. S. Ernest (iFire) Lee
consulted: lyuma
---

## Context and Problem Statement

The capabilities table lists features with a free-text status ("working", "loses
about 90%"). Free text does not say whether a feature is a throwaway experiment, a
committed part of the product, or a nice-to-have. The team needs one shared
vocabulary for how far along and how committed a feature is, so planning and the
docs agree on what "done" means for each one.

## Decision Drivers

- One vocabulary shared between planning and the manuals.
- A reader should know at a glance whether a feature is committed or exploratory.
- Cheap to apply and to move as a feature matures.

## Considered Options

- Keep free-text status only.
- A maturity ladder (alpha / beta / stable).
- A three-tier commitment classification: proof of concept, baseline, stretch.

## Decision Outcome

Chosen option: "A three-tier commitment classification", because it captures
commitment, not just maturity, which is what planning needs.

The tiers:

1. A proof of concept demonstrates the idea works end to end, in partial or
   throwaway form. It may be unreliable or lossy, and nothing depends on it yet.
2. The baseline is the committed minimum the product ships. It works reliably
   across the target platforms, and is the bar.
3. A stretch goal goes beyond baseline. It is pursued if time allows; cutting it
   does not block the release.

Each feature in the [capabilities table](../index.md#capabilities-and-where-they-live)
carries one tier. A feature moves between tiers as it matures or as commitment
changes; the tier is the current call, not a permanent label.

### Initial triage

- Native video playback — baseline.
- Scene baking via OpenUSD — baseline.
- Spatial audio (HRTF + audio probes) — baseline.
- Speech — baseline.
- Pen stroke creation (cassie) — proof of concept (patch surface creation loses
  about 90%).

### Consequences

- Good: planning and docs share one word per feature for its commitment level.
- Good: the tier is a small, reversible edit as features move.
- Bad: a tier is a judgement call and can drift from reality if the table is not
  kept current.

### Confirmation

The capabilities table has a Tier column, and every row carries one of the three
tiers. New capabilities are added with a tier.
