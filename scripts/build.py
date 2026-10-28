#!/usr/bin/env python3
"""Synchronize series labels, generate the sitemap, and stage public files."""
import argparse
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://jamesmldoesml.github.io"


def pages():
    return sorted([*ROOT.glob("*.html"), *ROOT.glob("blogs/*.html"),
                   *ROOT.glob("blogs/*/index.html")])


def synchronize(check=False):
    catalog = json.loads((ROOT / "data/series.json").read_text())
    # Derive secondary labels so a title is edited only once in the catalog.
    for key, values in catalog.items():
        title = values["title"]
        catalog[key] = {
            "page_title": f"{title} · James Ming Liang Ang",
            "description": f"{title}. A series by James Ming Liang Ang.",
            "taster_label": f"{title} · Taster Series",
            "citation_label": f"{title}: Taster Series",
            **values,
        }
    stale = []
    for path in pages():
        source = path.read_text()

        def replace(match):
            tag, attrs, body, close = match.groups()
            key = re.search(r'data-series="([^"]+)"', attrs)[1]
            field = re.search(r'data-field="([^"]+)"', attrs)[1]
            value = catalog[key]["title" if field == "aria_label" else field]
            if field in ("description", "aria_label"):
                attribute = "content" if field == "description" else "aria-label"
                attrs = re.sub(rf'{attribute}="[^"]*"',
                               lambda _: f'{attribute}="{html.escape(value, quote=True)}"', attrs)
                return f"<{tag}{attrs}>" + (body or "") + (close or "")
            return f"<{tag}{attrs}>{html.escape(value)}{close}"

        # Bound elements contain plain text, except article containers whose label
        # is an attribute. Match those opening tags separately to avoid nesting.
        opening = re.compile(r'<(meta|article)(\b[^>]*data-series="[^"]+"[^>]*data-field="[^"]+"[^>]*)>()()', re.S)
        updated = opening.sub(replace, source)
        text = re.compile(r'<(title|h1|a|p|span)(\b[^>]*data-series="[^"]+"[^>]*data-field="[^"]+"[^>]*)>([^<]*)(</\1>)', re.S)
        updated = text.sub(replace, updated)
        if updated != source:
            stale.append(str(path.relative_to(ROOT)))
            if not check:
                path.write_text(updated)
    if check and stale:
        raise SystemExit("Run python3 scripts/build.py to synchronize: " + ", ".join(stale))


def sitemap():
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    tree = ET.Element(ns + "urlset")
    for path in pages():
        if 'http-equiv="refresh"' in path.read_text():
            continue
        relative = path.relative_to(ROOT).as_posix()
        route = "/" + relative
        if route.endswith("index.html"):
            route = route[:-10]
        ET.SubElement(ET.SubElement(tree, ns + "url"), ns + "loc").text = ORIGIN + route
    ET.indent(tree)
    (ROOT / "sitemap.xml").write_bytes(ET.tostring(tree, encoding="utf-8", xml_declaration=True))


def stage():
    destination = ROOT / "dist"
    # Stage into a new folder first; replace only the generated deployment copy.
    staging = ROOT / "tmp/site-build"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    for path in [*pages(), ROOT / "sitemap.xml", ROOT / ".nojekyll"]:
        target = staging / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    shutil.copytree(ROOT / "assets", staging / "assets")
    # Downloads are explicitly public, tracked resources. Never copy ignored
    # tutorial files, project notes, Python sources, or rendering caches.
    tracked = subprocess.check_output(["git", "ls-files", "-z", "--", "blogs"], cwd=ROOT).decode().split("\0")
    public_extensions = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".mp4", ".webp", ".pdf", ".ipynb", ".zip", ".npz", ".json"}
    for name in tracked:
        if not name:
            continue
        path = ROOT / name
        if path.is_file() and path.suffix.lower() in public_extensions:
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    subprocess.run([sys.executable, str(ROOT / "scripts/check_links.py"), str(staging)], check=True)
    if destination.exists():
        shutil.rmtree(destination)
    staging.rename(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check catalog synchronization without writing files")
    args = parser.parse_args()
    synchronize(args.check)
    if not args.check:
        sitemap()
        stage()
        print("Built dist/; series labels and sitemap synchronized.")
