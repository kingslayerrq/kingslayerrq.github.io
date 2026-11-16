"""Render the dependency-free portfolio from shared layout and editable content."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"\{\{([a-z_]+)\}\}")
BUILD_LABELS = {"hand": "Hand-coded", "ai": "AI-assisted"}
TRACK_LABELS = {"gameplay": "Gameplay", "software": "Software"}
TIERS = {"feature", "small"}
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"


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
        if not re.fullmatch(SLUG, slug) or slug in ids:
            raise ValueError(f"Invalid or duplicate project id: {slug}")
        ids.add(slug)
        required = ["title", "category", "summary", "year", "role"]
        if not project.get("private"):
            required += ["url", "link_label"]
        for field in required:
            if not isinstance(project.get(field), str) or not project[field].strip():
                raise ValueError(f"{slug}: {field} must be a nonempty string")
        # Provenance is a promise to the reader, so every entry must declare it.
        if project.get("build") not in BUILD_LABELS:
            raise ValueError(f"{slug}: build must be one of {sorted(BUILD_LABELS)}")
        if project.get("track") not in TRACK_LABELS:
            raise ValueError(f"{slug}: track must be one of {sorted(TRACK_LABELS)}")
        if project.get("tier") not in TIERS:
            raise ValueError(f"{slug}: tier must be one of {sorted(TIERS)}")
        if not isinstance(project.get("featured"), bool):
            raise ValueError(f"{slug}: featured must be true or false")
        if not isinstance(project.get("tags"), list) or not all(isinstance(t, str) for t in project["tags"]):
            raise ValueError(f"{slug}: tags must be a list of strings")
        if project.get("url"):
            safe_url(project["url"])
        for link in project.get("links", []):
            if not link.get("label"):
                raise ValueError(f"{slug}: every extra link needs a label")
            safe_url(link["url"])
        if project.get("image"):
            image = project["image"]
            safe_url(image)
            if urlsplit(image).scheme or not (root / "site" / image).is_file():
                raise ValueError(f"{slug}: image must exist in site/")
            if not project.get("image_alt"):
                raise ValueError(f"{slug}: provide image_alt")
        if "snippet" in project:
            snippet = project["snippet"]
            if not all(isinstance(snippet.get(key), str) and snippet[key].strip() for key in ("label", "code")):
                raise ValueError(f"{slug}: snippet needs a label and code")
        if "page" in project:
            page = project["page"]
            if not re.fullmatch(SLUG, page) or page in pages or page in {"index", "projects"}:
                raise ValueError(f"Invalid or duplicate project page: {page}")
            pages.add(page)
            if project.get("url") != page + ".html":
                raise ValueError(f"{slug}: url must match the case-study page")
            if not (root / "content" / "pages" / (page + ".html")).is_file():
                raise ValueError(f"{slug}: missing case-study content")
        elif project.get("url") and not urlsplit(project["url"]).scheme:
            raise ValueError(f"{slug}: local links require a page field")


def display_order(projects):
    """Hand-coded work always comes before AI-assisted work; features before small entries."""
    return sorted(projects, key=lambda p: (p["tier"] != "feature", p["build"] != "hand"))


def badges(project):
    html = f'<span class="badge badge-{project["build"]}">{BUILD_LABELS[project["build"]]}</span>'
    if project.get("build_extra"):
        html += f'<span class="badge badge-extra">{escape(project["build_extra"])}</span>'
    return html


def link(label, url, css):
    arrow = "↗" if urlsplit(url).scheme else "→"
    return f'<a class="{css}" href="{escape(url, quote=True)}">{escape(label)} <span aria-hidden="true">{arrow}</span></a>'


def project_links(project, primary_css):
    parts = []
    if project.get("url"):
        parts.append(link(project["link_label"], project["url"], primary_css))
    parts += [link(extra["label"], extra["url"], "text-link") for extra in project.get("links", [])]
    if project.get("private"):
        parts.append('<span class="private-label">Private repository</span>')
    return "".join(parts)


def tag_list(project):
    return "".join(f"<span>{escape(tag)}</span>" for tag in project["tags"])


def data_attrs(project):
    return f'id="{escape(project["id"], quote=True)}" data-track="{project["track"]}" data-build="{project["build"]}"'


def project_card(project, index):
    p = {key: escape(value, quote=True) for key, value in project.items() if isinstance(value, str)}
    track = TRACK_LABELS[project["track"]]
    snippet = project.get("snippet")
    if project.get("image"):
        visual, css = f'<img src="{p["image"]}" alt="{p["image_alt"]}" width="1280" height="720" loading="lazy">', "drink-visual"
    elif snippet:
        # A real excerpt stands in for a screenshot; it is selectable text, so it is never wrapped in a link.
        visual = (f'<span class="code-file">{escape(snippet["label"])}</span>'
                  f'<pre><code>{escape(snippet["code"])}</code></pre>')
        css = "drink-visual is-code"
    else:
        visual = (f'<span class="sprite-wrap" aria-hidden="true"><svg class="glass" viewBox="0 0 16 16">'
                  f'<use href="#glass-{project["track"]}"/></svg></span>'
                  f'<span class="sprite-label" aria-hidden="true">{p["category"]}</span>')
        css = "drink-visual is-sprite"
    title = f'<a href="{p["url"]}">{p["title"]}</a>' if project.get("url") else p["title"]
    if project.get("url") and not (snippet and not project.get("image")):
        visual = f'<a class="{css}" href="{p["url"]}" aria-label="Open {p["title"]}">{visual}</a>'
    else:
        visual = f'<div class="{css}">{visual}</div>'
    note = f'<p class="build-note">{p["build_note"]}</p>' if project.get("build_note") else ""
    return f'''<article class="drink win" {data_attrs(project)}>
  <div class="win-bar"><span>No.{index:02d} <i aria-hidden="true">//</i> {track} <i aria-hidden="true">//</i> {p['year']}</span><span class="badges">{badges(project)}</span></div>
  {visual}
  <div class="drink-body"><h3>{title}</h3><p class="drink-summary">{p['summary']}</p><p class="drink-role"><b>Role</b> {p['role']}</p><div class="tags">{tag_list(project)}</div>{note}<div class="drink-links">{project_links(project, "button small")}</div></div>
</article>'''


def project_row(project, index):
    p = {key: escape(value, quote=True) for key, value in project.items() if isinstance(value, str)}
    title = f'<a href="{p["url"]}">{p["title"]}</a>' if project.get("url") else p["title"]
    return f'''<li class="pour" {data_attrs(project)}>
  <span class="pour-no">No.{index:02d}<small>{p['year']}</small></span>
  <div class="pour-main"><h3>{title}</h3><p>{p['summary']}</p><div class="tags">{tag_list(project)}</div></div>
  <div class="pour-side"><span class="badges">{badges(project)}</span>{project_links(project, "text-link")}</div>
</li>'''


def case_badge(project):
    note = f'<span class="build-note">{escape(project["build_note"])}</span>' if project.get("build_note") else ""
    return f'<p class="case-badge"><span class="badges">{badges(project)}</span>{note}</p>'


def build_outputs(root=ROOT):
    profile = json.loads((root / "content/profile.json").read_text(encoding="utf-8"))
    projects = json.loads((root / "content/projects.json").read_text(encoding="utf-8"))
    validate_projects(projects, root)
    ordered = display_order(projects)
    number = {p["id"]: i for i, p in enumerate(ordered, 1)}

    def cards(test):
        return "\n".join(project_card(p, number[p["id"]]) for p in ordered if test(p))

    features = [p for p in ordered if p["tier"] == "feature"]
    values = {key: escape(value, quote=True) for key, value in profile.items()}
    values.update(
        project_count=str(len(projects)),
        hand_count=str(sum(p["build"] == "hand" for p in projects)),
        ai_count=str(sum(p["build"] == "ai" for p in projects)),
        home_hand=cards(lambda p: p["featured"] and p["build"] == "hand"),
        home_ai=cards(lambda p: p["featured"] and p["build"] == "ai"),
        menu_hand_gameplay=cards(lambda p: p in features and p["build"] == "hand" and p["track"] == "gameplay"),
        menu_hand_software=cards(lambda p: p in features and p["build"] == "hand" and p["track"] == "software"),
        menu_ai=cards(lambda p: p in features and p["build"] == "ai"),
        menu_small="\n".join(project_row(p, number[p["id"]]) for p in ordered if p["tier"] == "small"),
        bar_scene=(root / "content/art/bar-scene.svg").read_text(encoding="utf-8").strip(),
        case_badge="",
    )
    layout = (root / "templates/layout.html").read_text(encoding="utf-8")
    specs = [("index", "home", profile["name"] + " — " + profile["role"], profile["intro"], "home-page", ""),
             ("projects", "projects", "Projects — " + profile["name"],
              "Gameplay and software engineering projects by " + profile["name"] + ", labeled hand-coded or AI-assisted.",
              "projects-page", "")]
    specs.extend((p["page"], p["page"], p["title"] + " — " + profile["name"], p["summary"], "case-page", case_badge(p))
                 for p in projects if p.get("page"))
    outputs = {}
    for filename, source, title, description, body_class, badge in specs:
        page_values = {**values, "case_badge": badge}
        body = render((root / "content/pages" / (source + ".html")).read_text(encoding="utf-8"), page_values)
        page_values.update(body=body, title=escape(title), description=escape(description, quote=True), body_class=body_class)
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
            path.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        raise SystemExit("Generated pages are stale: " + ", ".join(stale) + ". Run npm run build.")
    print(f"{'Checked' if args.check else 'Built'} {len(outputs)} static pages.")


if __name__ == "__main__":
    main()
