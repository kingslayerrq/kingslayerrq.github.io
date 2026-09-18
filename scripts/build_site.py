"""Render the dependency-free portfolio from shared layout and editable content."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"\{\{([a-z_]+)\}\}")


def render(template, values):
    """Only replace template tokens, never recursively interpret content."""
    return TOKEN.sub(lambda match: values[match[1]], template)


def safe_url(value):
    parsed = urlsplit(value)
    if parsed.scheme:
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"Only HTTPS external URLs are supported: {value}")
    elif parsed.netloc or value.startswith(("/", "\\")) or ".." in Path(parsed.path).parts:
        raise ValueError(f"Expected a relative site path: {value}")
    return value


def validate_projects(projects, root=ROOT):
    ids, pages = set(), set()
    for project in projects:
        slug = project["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in ids:
            raise ValueError(f"Invalid or duplicate project id: {slug}")
        ids.add(slug)
        for field in ("title", "category", "summary", "url", "link_label"):
            if not isinstance(project.get(field), str) or not project[field].strip():
                raise ValueError(f"{slug}: {field} must be a nonempty string")
        if not isinstance(project.get("featured"), bool):
            raise ValueError(f"{slug}: featured must be true or false")
        if not isinstance(project.get("tags"), list) or not all(isinstance(t, str) for t in project["tags"]):
            raise ValueError(f"{slug}: tags must be a list of strings")
        safe_url(project["url"])
        if project.get("image"):
            image = project["image"]
            safe_url(image)
            if urlsplit(image).scheme or not (root / "site" / image).is_file():
                raise ValueError(f"{slug}: image must exist in site/")
            if not project.get("image_alt"):
                raise ValueError(f"{slug}: provide image_alt")
        if "page" in project:
            page = project["page"]
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", page) or page in pages or page in {"index", "projects"}:
                raise ValueError(f"Invalid or duplicate project page: {page}")
            pages.add(page)
            if project["url"] != page + ".html":
                raise ValueError(f"{slug}: url must match the case-study page")
            if not (root / "content" / "pages" / (page + ".html")).is_file():
                raise ValueError(f"{slug}: missing case-study content")
        elif not urlsplit(project["url"]).scheme:
            raise ValueError(f"{slug}: local links require a page field")


def project_card(project, index):
    p = {key: escape(value, quote=True) for key, value in project.items() if isinstance(value, str)}
    if project.get("image"):
        visual = f'<img src="{p["image"]}" alt="{p["image_alt"]}" width="1280" height="746" loading="lazy">'
    else:
        visual = f'<div class="directory-art" aria-hidden="true"><span>[ {index:02d} ]</span><span>{p["category"]}</span><i>↗</i></div>'
    tags = "".join(f"<span>{escape(tag)}</span>" for tag in project["tags"])
    return f'''<article class="catalog-card" id="{p['id']}">
  <a class="catalog-visual" href="{p['url']}" aria-label="Explore {p['title']}">{visual}</a>
  <div class="catalog-copy"><p class="eyebrow">{index:02d} / {p['category']}</p><h3><a href="{p['url']}">{p['title']}</a></h3><p>{p['summary']}</p><div class="tags">{tags}</div><a class="text-link" href="{p['url']}">{p['link_label']} <span aria-hidden="true">↗</span></a></div>
</article>'''


def build_outputs(root=ROOT):
    profile = json.loads((root / "content/profile.json").read_text(encoding="utf-8"))
    projects = json.loads((root / "content/projects.json").read_text(encoding="utf-8"))
    validate_projects(projects, root)
    values = {key: escape(value, quote=True) for key, value in profile.items()}
    values["project_count"] = str(len(projects))
    values["featured_projects"] = "\n".join(project_card(p, i) for i, p in enumerate(projects, 1) if p["featured"])
    values["all_projects"] = "\n".join(project_card(p, i) for i, p in enumerate(projects, 1))
    layout = (root / "templates/layout.html").read_text(encoding="utf-8")
    specs = [("index", "home", profile["name"] + " — " + profile["handle"], profile["intro"], "home-page"),
             ("projects", "projects", "Projects — " + profile["name"], "Games, AI, and software projects by " + profile["name"], "projects-page")]
    specs.extend((p["page"], p["page"], p["title"] + " — " + profile["name"], p["summary"], "case-page") for p in projects if p.get("page"))
    outputs = {}
    for filename, source, title, description, body_class in specs:
        body = render((root / "content/pages" / (source + ".html")).read_text(encoding="utf-8"), values)
        page_values = {**values, "body": body, "title": escape(title), "description": escape(description, quote=True), "body_class": body_class}
        outputs[filename + ".html"] = render(layout, page_values)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated HTML is stale; do not write files")
    args = parser.parse_args()
    outputs = build_outputs()
    stale = []
    for filename, content in outputs.items():
        path = ROOT / "site" / filename
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(filename)
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Generated pages are stale: " + ", ".join(stale) + ". Run npm run build.")
    print(f"{'Checked' if args.check else 'Built'} {len(outputs)} static pages.")


if __name__ == "__main__":
    main()
