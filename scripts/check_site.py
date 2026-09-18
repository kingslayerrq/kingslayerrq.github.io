"""Validate the static site's HTML structure, IDs, links, and local assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1] / "site"
VOID = set("area base br col embed hr img input link meta param source track wbr".split())


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = set()
        self.refs = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"Duplicate ID: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "img" and not attrs.get("alt"):
            self.errors.append("Image is missing alternative text")
        for name in ("href", "src", "poster"):
            if attrs.get(name):
                self.refs.append(attrs[name])

    def handle_endtag(self, tag):
        if not self.stack or self.stack.pop() != tag:
            self.errors.append(f"Unbalanced closing tag: {tag}")


pages = {}
errors = []
for page in ROOT.rglob("*.html"):
    parser = SiteParser()
    parser.feed(page.read_text(encoding="utf-8"))
    if parser.stack:
        parser.errors.append(f"Unclosed tags: {parser.stack}")
    pages[page.resolve()] = parser
    errors.extend(f"{page.name}: {error}" for error in parser.errors)
for page, parser in pages.items():
    for ref in parser.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        target = (page.parent / unquote(url.path)).resolve() if url.path else page
        if url.path and not target.is_file():
            errors.append(f"{page.name}: Missing local asset: {ref}")
        if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"{page.name}: Missing anchor: {ref}")
for asset in ROOT.rglob("*"):
    if asset.is_file() and asset.stat().st_size >= 100 * 1024 * 1024:
        errors.append(f"Asset exceeds GitHub's file limit: {asset.name}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"Static validation passed: {len(pages)} pages, balanced HTML, local links/anchors, asset sizes.")
