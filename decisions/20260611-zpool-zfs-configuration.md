---
title: ZFS pool and dataset configuration baseline
date: 2026-06-11
status: accepted
---

## Context and Problem Statement

A new ZFS pool on a portable single disk stores project assets and moves between hosts,
and several of its properties fix themselves at creation time and stay immutable for the
life of the pool or dataset. A pool gets one `ashift` per vdev, and a dataset gets one
`casesensitivity` and one `normalization` setting, none of which a later `zfs set` can
change. A wrong choice here costs a full recreate-and-copy, so the layout needs deciding
before the first write lands. What `zpool create` and `zfs create` settings should the
baseline pool use? The pool name follows the naming convention
([20260611-zpool-naming-convention.md](20260611-zpool-naming-convention.md)), which
gives this drive the name `chibifire-vault-2026w24`.

## Decision Drivers

- Asset and content paths reach ZFS from clients that disagree on case, so a lookup of
  `Texture.png` and `texture.png` resolves to one file.
- Stored data compresses well, and the compressor trades a little CPU for a smaller
  footprint and less disk traffic.
- The immutable settings (`ashift`, `casesensitivity`, `normalization`, `utf8only`)
  carry their cost for the life of the pool, so each one decides at creation.
- The mutable settings (`compression`, `atime`, `recordsize`, `xattr`, `acltype`) tune
  in place later, so the baseline sets a sane default and leaves room to revise.
- The pool runs on Linux through OpenZFS, so Linux ACL and extended-attribute storage
  apply.

## Considered Options

The record settles eight questions. The first two come from the request; the rest are
the immutable or high-impact settings that ride alongside them.

- Case sensitivity: `sensitive` (default), `insensitive`, or `mixed`.
- Compression: `lz4` (default), `zstd`, or `zstd-N` at a chosen level.
- Unicode normalization: `none` (default) or `formD`, and the `utf8only` it implies.
- Vdev sector size: `ashift=12` (4 KiB) or `ashift=9` (512 B), or autodetect.
- Redundancy topology: single disk, mirror, or raidz1/raidz2/raidz3, and the `copies`
  count on a single-disk pool.
- Access-time updates: `atime=on` (default), `relatime=on`, or `atime=off`.
- Extended-attribute storage: `xattr=on` (default) or `xattr=sa`, with `acltype=posix`.
- Record size: the `128K` default or a workload-specific value.

## Decision Outcome

Chosen settings, with the reason each one holds:

Case sensitivity uses `casesensitivity=insensitive`, because clients reach the same
asset under different case and a single file answers each name. The setting fixes at
dataset creation and never changes afterward.

Compression uses `compression=zstd`, because zstd reaches a smaller footprint than lz4
at a CPU cost the workload absorbs, and the default zstd level (3) sits at the knee of
the size-versus-speed curve. The level revises later with `zfs set compression=zstd-N`
without recreating the dataset.

Unicode normalization uses `normalization=formD`, because case folding compares names
correctly only when their Unicode form matches, and `formD` makes ZFS store and compare
names in a single normal form. `normalization=formD` forces `utf8only=on`, so the
dataset rejects non-UTF-8 names; both settings fix at creation alongside
`casesensitivity`.

Sector size uses `ashift=12`, because current drives present 4 KiB physical sectors
even when they report 512 B, and a 4 KiB-aligned pool avoids the write amplification a
mismatched `ashift=9` pool carries for its whole life. `ashift` fixes per vdev at
`zpool create`.

Redundancy topology is a single disk, because the pool runs on one drive. A single-disk
vdev carries no redundancy, so a drive failure loses the pool, and a backup or
replication target holds the recovery copy rather than the pool itself. The dataset sets
`copies=1`, ZFS's default of one copy of each block, because the off-pool backup rather
than an on-disk second copy carries the recovery, and a single-disk vdev loses
everything on a whole-drive failure regardless of the copy count. A dataset that values
block-level self-healing from bad sectors over footprint raises `copies` to `2`, which
keeps two copies of each block on the one disk and roughly doubles the space each file
occupies.

Access-time updates use `atime=off`, because the workload reads assets without needing a
per-read metadata write, and turning `atime` off removes that write amplification. The
setting tunes in place later if some tool needs access times.

Extended-attribute storage uses `xattr=sa` with `acltype=posix`, because storing
extended attributes in the inode rather than a hidden directory cuts the extra I/O that
ACL and xattr lookups otherwise cost on Linux.

Record size keeps the `128K` default for general data, because the default suits mixed
file sizes, and a dataset holding a single large-record or small-record workload sets
its own `recordsize` at creation.

A creation command carrying these settings reads:

```sh
zpool create -o ashift=12 chibifire-vault-2026w24 /dev/disk/by-id/<single-disk>

zfs create \
  -o casesensitivity=insensitive \
  -o normalization=formD \
  -o compression=zstd \
  -o copies=1 \
  -o atime=off \
  -o xattr=sa \
  -o acltype=posix \
  chibifire-vault-2026w24/files
```

### Consequences

- Good, because the case-insensitive, normalized dataset resolves one file per name
  regardless of the client's case or Unicode form.
- Good, because zstd shrinks the stored footprint and the disk traffic, and the level
  retunes without a recreate.
- Good, because `ashift=12`, `atime=off`, and `xattr=sa` each remove a class of write
  amplification for the life of the pool.
- Bad, because `casesensitivity`, `normalization`, `utf8only`, and `ashift` fix at
  creation, so a wrong value here costs a full recreate-and-copy.
- Bad, because `utf8only=on` rejects any name that is not valid UTF-8, so a legacy tool
  emitting non-UTF-8 names fails on this dataset.
- Bad, because zstd spends more CPU per write than lz4, which shows on a CPU-bound host.
- Bad, because a single-disk vdev holds no redundancy, so a drive failure loses the pool
  and recovery depends on an off-pool backup; `copies=1` keeps one copy per block, so
  raising it to `copies=2` would heal bad blocks but not a dead drive while doubling the
  space each file occupies.
- Good, because the case-insensitive, normalized layout reads consistently across the
  hosts a portable drive visits, so the same asset resolves the same way on each.
- Bad, because a portable drive needs `zpool export chibifire-vault-2026w24` before it
  unplugs, since pulling a live pool risks an unclean export and an import that needs
  `-f` on the next host.

### Confirmation

`zpool get ashift chibifire-vault-2026w24` reports `12`, and `zfs get
casesensitivity,normalization,utf8only,compression,copies,atime,xattr,acltype
chibifire-vault-2026w24/files` reports `insensitive`, `formD`, `on`, `zstd`, `1`,
`off`, `sa`, and `posix`. A lookup of a file under two different cases resolves to the
same inode, which `ls -i` confirms.

## More Information

The immutable settings (`casesensitivity`, `normalization`, `utf8only`, and `ashift`)
follow the OpenZFS property documentation, which marks them settable only at creation.
The single-disk topology carries no redundancy, so the recovery plan rests on an
off-pool backup or replication target.
