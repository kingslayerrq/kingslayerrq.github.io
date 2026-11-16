"""Protect content authoring, provenance labels, and the static publication boundary."""
import copy
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import build_outputs, display_order, project_card, validate_projects


class ContentBuildTests(unittest.TestCase):
    def setUp(self):
        self.projects = json.loads((ROOT / "content/projects.json").read_text(encoding="utf-8"))

    def test_rejects_duplicate_ids_missing_pages_and_unsafe_links(self):
        for mutation in ("duplicate", "page", "url"):
            projects = copy.deepcopy(self.projects)
            if mutation == "duplicate":
                projects.append(copy.deepcopy(projects[0]))
            elif mutation == "page":
                projects[0].update(page="missing-page", url="missing-page.html")
            else:
                projects[0]["url"] = "javascript:alert(1)"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_projects(projects)

    def test_every_project_must_declare_how_it_was_built(self):
        for field, value in (("build", None), ("build", "mostly-hand"), ("track", "other"), ("tier", "huge")):
            projects = copy.deepcopy(self.projects)
            if value is None:
                del projects[0][field]
            else:
                projects[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                validate_projects(projects)

    def test_code_snippets_are_escaped_and_never_wrapped_in_links(self):
        project = copy.deepcopy(self.projects[0])
        project.pop("image", None)
        project["snippet"] = {"label": "a.c", "code": "if (a < b && c) { x<y>(); }"}
        card = project_card(project, 1)
        self.assertIn("a &lt; b &amp;&amp; c", card)
        self.assertIn('<div class="drink-visual is-code">', card)
        project["snippet"] = {"label": "a.c"}
        with self.assertRaises(ValueError):
            validate_projects([project])

    def test_plain_text_metadata_is_escaped(self):
        project = copy.deepcopy(self.projects[0])
        project["title"] = '<script>alert("x")</script>'
        card = project_card(project, 1)
        self.assertNotIn("<script>", card)
        self.assertIn("&lt;script&gt;", card)

    def test_hand_coded_work_is_listed_before_ai_assisted_work(self):
        for tier in ("feature", "small"):
            builds = [p["build"] for p in display_order(self.projects) if p["tier"] == tier]
            self.assertEqual(builds, sorted(builds, key=lambda build: build != "hand"), tier)
        outputs = build_outputs()
        for page in ("index.html", "projects.html"):
            for kind in ("drink win", "pour"):
                builds = re.findall('class="' + kind + '" id="[^"]+" data-track="[^"]+" data-build="([a-z]+)"', outputs[page])
                self.assertEqual(builds, sorted(builds, key=lambda build: build != "hand"), page + " " + kind)
            self.assertIn('data-build="hand"', outputs[page])
            self.assertIn('data-build="ai"', outputs[page])

    def test_every_entry_is_labeled_on_the_menu(self):
        menu = build_outputs()["projects.html"]
        for project in self.projects:
            start = menu.index('id="' + project["id"] + '"')
            entry = menu[start:start + 3000]
            label = "Hand-coded" if project["build"] == "hand" else "AI-assisted"
            self.assertIn('badge-' + project["build"] + '">' + label, entry, project["id"])

    def test_home_stays_light_and_pages_share_contact_details(self):
        outputs = build_outputs()
        self.assertIn("How to read the labels", outputs["index.html"])
        self.assertNotIn("<video", outputs["index.html"])
        for project in self.projects:
            if project.get("page"):
                page = outputs[project["page"] + ".html"]
                self.assertIn('class="case-badge"', page)
        for page in outputs.values():
            self.assertIn("vibe coded by Kingslayerrq", page)
            self.assertIn("1225896471812112426", page)
            self.assertIn("mailto:rq2014@nyu.edu", page)


if __name__ == "__main__":
    unittest.main()
