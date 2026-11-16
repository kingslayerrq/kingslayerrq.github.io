"""Protect content authoring, build tags, and the static publication boundary."""
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

    def test_projects_are_grouped_by_role_not_by_how_they_were_built(self):
        tiers = [p["tier"] for p in display_order(self.projects)]
        self.assertEqual(tiers, sorted(tiers, key=lambda tier: tier != "feature"))
        outputs = build_outputs()
        for name, page in outputs.items():
            text = page.lower()
            for phrase in ("case study", "case-study", "ai-title", "how to read the labels", "data-build"):
                self.assertNotIn(phrase, text, name)

    def test_every_entry_carries_one_small_build_tag(self):
        menu = build_outputs()["projects.html"]
        for project in self.projects:
            start = menu.index('id="' + project["id"] + '"')
            entry = menu[start:menu.index("</article>" if project["tier"] == "feature" else "</li>", start)]
            label = "Hand-coded" if project["build"] == "hand" else "AI-assisted"
            self.assertEqual(entry.count('class="badge"'), 1, project["id"])
            self.assertIn(">" + label + "</span>", entry, project["id"])

    def test_home_stays_light_and_pages_share_contact_details(self):
        outputs = build_outputs()
        self.assertNotIn("<video", outputs["index.html"])
        for project in self.projects:
            if project.get("page"):
                page = outputs[project["page"] + ".html"]
                self.assertRegex(page, r'<p class="eyebrow accent"><span class="badge">[^<]+</span>Recipe No\.\d\d / ' + re.escape(project["drink"].replace("&", "&amp;")))
        for page in outputs.values():
            self.assertIn("vibe coded by Kingslayerrq", page)
            self.assertIn("1225896471812112426", page)
            self.assertIn("mailto:rq2014@nyu.edu", page)


if __name__ == "__main__":
    unittest.main()
