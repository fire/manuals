---
title: Comments and docs use a tenseless continuous-present voice
date: 2026-06-07
status: accepted
---

## Context and Problem Statement

Comments and documentation drift out of sync with code as the system changes. A
comment written as history ("added a cache", "we removed the old path") or as a plan
("will solve this", "TODO: wire X") describes a moment that has passed or has not yet
arrived, so a reader cannot check it against the code in front of them. How should
prose in this repo phrase what it says about the system?

## Decision Drivers

- A reader trusts a comment when it matches the code as it stands.
- History lives in git; plans live in issues and decision records.
- The rule stays mechanical enough to apply in review without debate.

## Considered Options

- Free choice of tense per author.
- Past-tense changelog voice inside code comments.
- A tenseless continuous-present voice where every sentence states what is currently
  true of the system.

## Decision Outcome

Chosen option: "a tenseless continuous-present voice", because a sentence that states a
present truth stays correct as long as the code it describes stays the same, and goes
stale visibly the moment the code changes.

Every comment and documentation sentence states what is currently true of the system.
Prose describes behaviour ("the parser streams tokens"), and an unfinished area reads
as a present gap ("the parser handles no Unicode escapes yet") rather than as a task or
a past edit. The voice covers code comments, doc pages, and decision records alike.

The voice rules out three habits:

- Past-tense narration of edits, such as "removed the legacy path" or "we switched to a
  queue".
- Future or imperative planning, such as "will add validation" or "TODO: handle
  retries".
- Temporal qualifiers that age, such as "now", "currently changed", or "previously".

A TODO document states each open item as a present gap, so the file reads as a
description of where the system stands rather than a logbook of intentions.

### Consequences

- Good, because a stale sentence signals a real divergence from the code, which makes
  review catch it.
- Good, because one voice covers code comments, doc pages, and decision records.
- Bad, because a present-gap phrasing reads less naturally than an imperative TODO, and
  authors need practice to phrase work that way.

### Confirmation

Review checks that new comments and prose state present truths, with no past-tense edit
narration, no future or imperative planning, and no aging temporal qualifiers. The
existing decision records in this repo already read this way.

## More Information

This generalizes the house rule applied across the sinew Lean spec and its native
viewer prose, where comments describe current behaviour and `todo.md` lists each open
item as a present gap.
