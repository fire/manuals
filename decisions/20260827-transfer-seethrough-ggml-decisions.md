---
title: Transfer the see-through ggml decisions out of an archived repository
date: 2026-08-27
status: accepted
tier: baseline
---

## Context and Problem Statement

`weftspun/interactor-seethrough-ggml` was archived on 2026-08-20. It holds a
See-Through port (anime illustration to inpainted semantic layers and depth) written
against ggml in C++, and twelve decision records covering GGUF conversion,
quantisation, and numerical parity.

Archiving does not delete: the repository is readable and every file is still there.
What archiving removes is the expectation that anyone will look. The decisions in it
answer questions that recur — how weights reach C++, which quantisation to serve, how
to know a port is numerically right — and the next person to face those questions has
no reason to search an archived repository they may not know exists.

## Decision Drivers

- Reasoning outlives the code it was written for. A port can be abandoned while the
  argument for its file format stays correct.
- A decision nobody can find gets made again, usually differently.
- The archived repository must stay the provenance, not become a second source of
  truth that drifts.

## Considered Options

1. Leave it. The repository is public and readable.
2. Unarchive and maintain it.
3. Copy the decisions here, keeping the archive as provenance.

## Decision Outcome

Option 3. Twelve records move to `decisions/`, renamed to this repository's
`YYYYMMDD-short-title` convention, each carrying a note naming the file it came from.
Content is verbatim apart from front matter replacing the original heading and status
line.

Option 1 loses them by attrition rather than by deletion. Option 2 claims a maintenance
commitment nobody has made — the port itself is not being continued, and pretending
otherwise is worse than archiving it honestly.

## What was NOT transferred, and why

The code stays in the archive. `src/` is a complete ggml diffusion pipeline — CLIP,
VAE, UNet, scheduler, LaMa inpainting, PSD layer writing — and `verify/` builds Slang
shaders from a Lean DSL. Neither is dead, but copying source without its build,
weights and tests produces something that looks maintained and is not. The decisions
record where it lives.

Three pieces are worth reading before similar work starts again:

- `verify/EmitShaders.lean` and `verify/Compute/*.lean` — a typed Lean 4 DSL that
  constructs Slang shader ASTs and emits `.slang`, compiled by `slangc` to `cpp`,
  `spirv` and `metal` from one source, with the CPU target kept as a validation
  anchor. Anyone building an emitter that turns a graph into portable IR is walking
  the same ground.
- `scripts/convert_diffusers_to_gguf.py` and `repack_q4_to_q8.py` — conversion and
  requantisation that ADR 0002 and 0005 argue for.
- `docs/quantization-ladder.md` — the ladder those ADRs reference.

## A correction worth recording

`verify/` contains **no theorems or lemmas**. It was described during this transfer as
formal verification of compute kernels, which it is not: `ComputeVerify.lean` checks
that each emitted shader string is non-empty and nothing more. The Lean is a typed
construction DSL whose value is that a malformed shader fails to build, not that a
correct one is proved. The directory name invites the stronger reading, and the
stronger reading was wrong.

## Consequences

- The reasoning is searchable in the published manuals.
- The archive stays the provenance for code, and each transferred file says so.
- Numbering gaps are preserved by date rather than renumbered: the original had no
  0006, and `0012-3d-pipeline` carried no date, so it takes 2026-07-20 from the
  records either side of it. That is a guess and is written here rather than hidden.
