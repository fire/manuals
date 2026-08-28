---
title: GGUF weights via one self-contained converter
date: 2026-07-17
status: accepted
tier: baseline
---

::: {.callout-note appearance="simple"}
Transferred from the archived `weftspun/interactor-seethrough-ggml` repository, originally `docs/decisions/0002-gguf-weights-self-contained-converter.md`. The repository is archived and read-only; this copy is the one that stays maintained. Content follows the original apart from the front matter, which replaces the original heading and status line, and bold-label list openers, which this repository's prose check rejects as an AI-writing tell.
:::

## Context and Problem Statement

Five diffusers components (LayerDiff SDXL UNet, SDXL VAE, TransparentVAE,
Marigold SD2 UNet, SD VAE) must reach the C++ side with their
hyperparameters. What format and tooling?

## Considered Options

1. One generic diffusers→GGUF script, self-contained writer
   (trellis2cpp house style: no `gguf` package, no torch).
2. Per-component converter scripts (trellis2cpp has one per checkpoint).
3. Reuse stable-diffusion.cpp's converters.

## Decision Outcome

Option 1. All five components share the same on-disk shape (safetensors +
`config.json`), so one script with a component table suffices — maximal
trim. Choices inside it:

- Tensor names — original diffusers state-dict keys, verbatim. The C++
  graph builder looks weights up by name; no rename table to maintain.
- Config — the component's `config.json` travels as ONE string KV
  (`seethrough.<component>.config_json`). The C++ loader owns
  interpretation; the converter never grows per-arch flattening code.
- safetensors parsing — manual (~30 lines, handles BF16 by bit-shift)
  instead of the `safetensors` package — the only Python deps are numpy +
  huggingface_hub.
- ftype policy — f16 for 2D+ weights except names containing "norm";
  f32 for the rest (norm gammas/betas, biases, all 1-D).

Consequences: `convert_diffusers_to_gguf.py` is the whole phase-1 surface.
Rejected option 3 because sd.cpp's converters rename tensors to its own
schema, which would couple our graph code to sd.cpp's naming. Stock CLIP
text encoders are deliberately NOT converted yet (see ADR 5).
