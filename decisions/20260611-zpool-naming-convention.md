---
title: ZFS pool naming convention
date: 2026-06-11
status: accepted
---

## Context and Problem Statement

A ZFS pool needs a name at `zpool create`, and the name does more work than it looks.
`zpool import` matches on the pool name, so a portable drive that moves between hosts
imports cleanly only when no pool on the destination already carries the same name. A
generic name such as `tank`, `data`, or `zpool` collides on exactly the machines a
portable drive travels to, which forces an import by GUID and loses the name as a label.
The name also becomes the default mount root (`/<pool>`) and the prefix of every dataset
path. What convention should a pool name follow so it imports without collision, carries
its provenance, and stays filesystem-friendly?

## Decision Drivers

- A portable drive imports on hosts it has never seen, so the name needs to be unique
  enough to avoid a collision on any of them.
- The name labels the drive's owner and vintage, so a drive found on a shelf or imported
  elsewhere identifies whose it is and when it entered service.
- ZFS constrains the name: it begins with a letter, holds only alphanumeric characters
  and `_`, `-`, `:`, `.`, or space, and the tokens `mirror`, `raidz`, `draid`, `spare`,
  and `log` are reserved, as are names beginning with them.
- The name is the default mount root and every dataset's path prefix, so lowercase ASCII
  with no spaces reads and scripts cleanly.
- The repo already names archival assets `YYYYMMDD_project_description_NNNN`, so a pool
  name that echoes that shape stays consistent across the project.

## Considered Options

- A generic name (`tank`, `data`, `zpool`, `pool0`).
- A hostname-derived name tied to the machine that created the pool.
- A trademark-prefixed convention carrying owner, role, and commission week.

## Decision Outcome

Chosen option: a trademark-prefixed convention, because the brand prefix makes the name
unique on any host the drive reaches and names the owner on sight, while the commission
week dates the drive without a running counter. A hostname-derived name ties a portable
drive to the one machine that made it, and a generic name collides on import, so neither
fits a drive that travels.

The pattern:

```
<owner>-<role>-<isoyearweek>[-NN]
```

- `<owner>` is a trademark or handle slug that owns the data: `chibifire` for the
  business (github.com/chibifire) or `fire` for personal use (github.com/fire).
- `<role>` is the drive's purpose: `assets`, `backup`, `scratch`, or similar.
- `<isoyearweek>` is the ISO 8601 week of commissioning, lowercase `w`, such as
  `2026w24`. The year is the ISO week-year, so a date near the January boundary carries a
  consistent year and week together.
- `-NN` is an optional zero-padded tiebreaker, present only when two drives share the
  same owner, role, and week.

The convention follows lowercase ASCII with hyphen-separated facets, the same shape as
the archival file-naming convention
([20260606-archival-file-naming-convention.md](20260606-archival-file-naming-convention.md)).
It satisfies the ZFS rules: each name begins with a letter, uses only allowed characters,
and avoids the reserved tokens.

The first drive under this convention, a portable single disk holding project assets
commissioned in ISO week 2026-W24, takes the name:

```
chibifire-assets-2026w24
```

A pool name is a label rather than an immutable creation property: `zpool export
<name>` followed by `zpool import <old> <new>` renames it. So a name that misses the
convention corrects later, at the cost of updating any script that hardcodes the old
dataset path.

### Consequences

- Good, because the brand prefix makes the name collision-resistant on import, so the
  drive mounts by name on a host it has never seen.
- Good, because the name states the owner and the commission week, so a stray drive
  identifies whose it is and how old it is.
- Good, because the convention matches the archival file-naming shape, so one lowercase
  hyphenated style covers files and pools alike.
- Bad, because the name runs longer than `tank`, so it costs more to type at the command
  line and reads as a longer mount root.
- Bad, because a rename to fix a non-conforming name breaks any script that hardcodes the
  dataset path, so the name is worth getting right at creation even though it is mutable.

### Confirmation

`zpool list` shows the pool name matching `<owner>-<role>-<isoyearweek>[-NN]`, lowercase
with hyphen-separated facets. Importing the drive on a second host that runs no
like-named pool succeeds by name rather than falling back to a GUID.

## More Information

The naming rules and the reserved tokens follow the OpenZFS `zpoolconcepts(7)` manual
page. The convention pairs with the pool and dataset configuration baseline
([20260611-zpool-zfs-configuration.md](20260611-zpool-zfs-configuration.md)), which sets
the properties for the same drive.
