---
title: Commit messages use sentence case without Conventional Commits prefixes
date: 2026-06-09
status: accepted
---

## Context and Problem Statement

A commit subject is the first line a reader meets in `git log`, a blame, or a release
note. Two conventions compete for how it reads. Conventional Commits prefixes each
subject with a machine-readable type and optional scope, such as `feat:` or
`fix(parser):`, and lower-cases the summary that follows. Plain prose writes the subject
as an ordinary capitalised sentence. How should a commit subject in this repo read?

## Decision Drivers

- A reader scans the subject as a sentence first, and the meaning sits at the front
  rather than after a colon.
- The repos here run no tooling that consumes a commit type: no semantic-release, no
  changelog keyed on `feat` or `fix`.
- One rule covers every commit, so review needs no judgement about which type applies.

## Considered Options

- Conventional Commits, with a `type(scope):` prefix on every subject.
- Sentence-case prose subjects with no prefix.
- Free choice of style per author.

## Decision Outcome

Chosen option: sentence-case prose with no prefix, because the subject stays a sentence
a reader understands on sight, and the repos gain nothing from a commit type that no
tool reads.

A commit subject opens with a capital letter and reads as a plain sentence, such as
`Add the macOS and Windows release workflows`. It carries no `feat:`, `fix:`, `chore:`,
or `type(scope):` prefix, and no trailing period. The body, where present, states what
the change makes true of the system and why.

### Consequences

- Good, because the subject reads as a summary on its own, with nothing to strip before
  the meaning.
- Good, because the rule holds for every commit, so no author weighs whether a change
  counts as a `feat` or a `fix`.
- Bad, because a changelog tool that groups commits by type finds no signal here, so
  adopting one later needs a different marker or a history rewrite.

### Confirmation

Review reads each subject as a capitalised sentence with no type prefix and no trailing
period. The history after this decision shows subjects in that form.

## More Information

This pairs with the tenseless continuous-present voice
([20260607-tenseless-continuous-present-voice.md](20260607-tenseless-continuous-present-voice.md)):
a commit body states what the change makes true of the system, the same way comments and
docs do.
