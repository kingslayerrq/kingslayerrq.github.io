"""Protect content authoring and the static publication boundary."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import build_outputs, project_card, validate_projects


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

    def test_plain_text_metadata_is_escaped(self):
        project = copy.deepcopy(self.projects[0])
        project["title"] = '<script>alert("x")</script>'
        card = project_card(project, 1)
        self.assertNotIn("<script>", card)
        self.assertIn("&lt;script&gt;", card)

    def test_personal_home_keeps_details_on_project_pages(self):
        outputs = build_outputs()
        self.assertIn("The person", outputs["index.html"].replace("THE PERSON", "The person"))
        self.assertNotIn("<pre>", outputs["index.html"])
        self.assertNotIn("<video", outputs["index.html"])
        for project in self.projects:
            self.assertIn('id="' + project["id"] + '"', outputs["projects.html"])
            if project.get("page"):
                self.assertIn(project["page"] + ".html", outputs)
        for page in outputs.values():
            self.assertIn("vibe coded by Kingslayerrq", page)
            self.assertIn("1225896471812112426", page)
            self.assertIn("mailto:rq2014@nyu.edu", page)


if __name__ == "__main__":
    unittest.main()
