#!/usr/bin/env python3
"""Page metadata and backlinks for the manuals site.

Frontmatter stays the single source of truth. This filter:
  * shows ``tier`` and ``status`` at the top of a page (so authors never repeat
    them in the body), rendering a ``superseded by <file>.md`` status as a link;
  * appends a Related section listing every other content page this one links to
    plus every page that links to it (symmetric), and a breadcrumb trail on top.
"""
import glob
import os
import posixpath
import re

from panflute import (
    BulletList,
    Emph,
    Header,
    Link,
    ListItem,
    Para,
    Space,
    Str,
    Strong,
    run_filter,
    stringify,
)

_STEM = r"[0-9]{8}-[a-z0-9-]+"
_SUPERSEDED = re.compile(r"^superseded by\s+(\S+)\.md\s*$", re.IGNORECASE)
_LINK = re.compile(r"\]\(([^)\s]+)\)")
_PAGE_EXT = (".md", ".qmd", ".html")
_SKIP_DIRS = ("_site/", "decisions/attachments/", "filters/")


def _posix(path):
    return path.replace(os.sep, "/")


def _strip_ext(target):
    for ext in _PAGE_EXT:
        if target.endswith(ext):
            return target[: -len(ext)]
    return target


def _key(path):
    return _strip_ext(_posix(path))


def _parse_frontmatter(text):
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end >= 0 else ""


def _parse_title(text, fallback):
    match = re.search(r"^title:\s*(.+?)\s*$", _parse_frontmatter(text), re.MULTILINE)
    if match:
        title = match.group(1).strip()
        if len(title) >= 2 and title[0] in "\"'" and title[-1] == title[0]:
            title = title[1:-1]
        return title
    heading = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return fallback


def _resolve(from_dir, target):
    target = _strip_ext(target.split("#")[0].split("?")[0])
    if not target:
        return None
    joined = posixpath.normpath(posixpath.join(from_dir, target)) if from_dir else posixpath.normpath(target)
    if joined.startswith(".."):
        return None
    return joined


def _project_root():
    # Quarto sets QUARTO_PROJECT_DIR for filters; the filter's own cwd is the
    # document's directory, so anchor scanning to the project root instead.
    return os.environ.get("QUARTO_PROJECT_DIR") or "."


def _scan():
    """Map every page key (relative to the project root) to its title and the set
    of page keys it links to, independent of the filter's working directory."""
    root = _project_root()
    graph = {}
    paths = set(glob.glob(os.path.join(root, "**", "*.md"), recursive=True)) | set(
        glob.glob(os.path.join(root, "**", "*.qmd"), recursive=True)
    )
    for path in paths:
        key = _strip_ext(_posix(os.path.relpath(path, root)))
        if any((key + "/").startswith(d) for d in _SKIP_DIRS):
            continue
        from_dir = posixpath.dirname(key)
        try:
            text = open(path, encoding="utf-8").read()
        except OSError:
            continue
        out = set()
        for target in _LINK.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if not target.split("#")[0].split("?")[0].endswith(_PAGE_EXT):
                continue
            resolved = _resolve(from_dir, target)
            if resolved and resolved != key:
                out.add(resolved)
        for stem in re.findall(_STEM + r"\.md", _parse_frontmatter(text)):
            resolved = _resolve(from_dir, stem)
            if resolved and resolved != key:
                out.add(resolved)
        graph[key] = {"title": _parse_title(text, posixpath.basename(key)), "out": out}
    return graph


def _status_inlines(status):
    match = _SUPERSEDED.match(status)
    if match:
        stem = match.group(1)
        return [Str("superseded by"), Space(), Link(Str(stem), url=stem + ".html")]
    return [Str(status)]


_SECTIONS = {"decisions": "Decisions", "changelog": "Changelog"}


def _breadcrumb(current, title):
    """Hierarchy trail for the top of a page: Manuals › Section › Title."""
    if current == "index":
        return None
    here = posixpath.dirname(current)
    prefix = "../" * len([p for p in here.split("/") if p])
    crumbs = [Link(Str("Manuals"), url=prefix + "index.html")]
    seg0 = current.split("/")[0] if "/" in current else None
    if seg0 in _SECTIONS:
        crumbs.append(Link(Str(_SECTIONS[seg0]), url=prefix + seg0 + ".html"))
    crumbs.append(Str(title))
    inlines = []
    for i, crumb in enumerate(crumbs):
        if i:
            inlines.extend([Space(), Str("›"), Space()])
        inlines.append(crumb)
    return Para(Emph(*inlines))


def action(elem, doc):
    return None


def finalize(doc):
    head = []

    def add(label, parts):
        if head:
            head.extend([Space(), Str("·"), Space()])
        head.append(Strong(Str(label + ":")))
        head.append(Space())
        head.extend(parts)

    tier = doc.get_metadata("tier")
    status = doc.get_metadata("status")
    if tier:
        add("Tier", [Str(str(tier))])
    if status:
        add("Status", _status_inlines(str(status)))
    if head:
        doc.content.insert(0, Para(*head))

    # Navigation must never break a render; degrade to nothing on any error.
    try:
        title = stringify(doc.metadata["title"]) if "title" in doc.metadata else None
        if not title:
            return
        graph = _scan()
        current = next((k for k, info in graph.items() if info["title"] == title), None)
        if current is None:
            return

        # Related (symmetric) at the bottom: pages this one links to, plus pages
        # that link here. Limited to content pages (keys with a path), so the
        # hub/listing pages (index, decisions, changelog, references) stay out.
        outbound = graph[current]["out"]
        inbound = {k for k, info in graph.items() if current in info["out"]}
        related = sorted(
            k for k in (outbound | inbound) if k != current and "/" in k and k in graph
        )
        if related:
            here = posixpath.dirname(current)
            items = []
            for key in related:
                href = posixpath.relpath(key, here) if here else key
                items.append(ListItem(Para(Link(Str(graph[key]["title"]), url=href + ".html"))))
            doc.content.append(Header(Str("Related"), level=2, identifier="related"))
            doc.content.append(BulletList(*items))

        # Breadcrumb trail at the top (inserted last so it sits above the meta line).
        crumb = _breadcrumb(current, title)
        if crumb is not None:
            doc.content.insert(0, crumb)
    except Exception:
        return


def main(doc=None):
    return run_filter(action, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
