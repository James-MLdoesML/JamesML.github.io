#!/usr/bin/env python3
"""Check local pages, fragments, navigation, CSS images and public downloads."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href", "src", "poster"):
            if key in attrs:
                self.links.append(attrs[key])
        for item in attrs.get("srcset", "").split(","):
            if item.strip():
                self.links.append(item.strip().split()[0])
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.links.append(attrs["content"].split("url=", 1)[1])
        if "aria-labelledby" in attrs:
            self.links.extend("#" + value for value in attrs["aria-labelledby"].split())
        if "aria-controls" in attrs:
            self.links.extend("#" + value for value in attrs["aria-controls"].split())


def check(root):
    root = root.resolve()
    parsed = {p: Page(p.read_text()) for p in root.rglob("*.html")}
    errors = []
    count = 0

    def verify(source, url):
        nonlocal count
        parts = urlsplit(url)
        if parts.scheme or parts.netloc:
            if parts.netloc.lower() != "jamesmldoesml.github.io":
                return
            path = root / unquote(parts.path).lstrip("/")
        else:
            path = (root / unquote(parts.path).lstrip("/")) if parts.path.startswith("/") else source.parent / unquote(parts.path)
            if not parts.path:
                path = source
        path = path.resolve()
        if not path.is_relative_to(root):
            errors.append(f"{source.relative_to(root)}: outside site: {url}")
            return
        if path.is_dir():
            path /= "index.html"
        count += 1
        if not path.is_file():
            errors.append(f"{source.relative_to(root)}: missing {url}")
        elif parts.fragment and path in parsed and unquote(parts.fragment) not in parsed[path].ids:
            errors.append(f"{source.relative_to(root)}: missing fragment {url}")

    for path, page in parsed.items():
        for name, n in Counter(page.ids).items():
            if n > 1:
                errors.append(f"{path.relative_to(root)}: duplicate ID {name}")
        for url in page.links:
            verify(path, url)
    for path in root.rglob("*.css"):
        for url in re.findall(r'url\([\'"]?([^\)\'"\s]+)[\'"]?\)', path.read_text()):
            verify(path, url)
    sitemap = root / "sitemap.xml"
    if sitemap.exists():
        for node in ET.parse(sitemap).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            verify(sitemap, node.text)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(parsed)} pages; {count} local links, fragments, assets and sitemap routes.")


if __name__ == "__main__":
    check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "dist")
