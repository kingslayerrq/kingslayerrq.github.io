# Richard Qu / Kingslayerrq — portfolio

A recruiter-facing portfolio for software and gameplay engineering roles, styled as a late-night cyberpunk bar terminal: pixel-window panels, a visual-novel dialogue box, and projects presented as a menu. Projects are grouped by role (gameplay or software); each carries one small **Hand-coded** or **AI-assisted** tag, and the larger ones link to a recipe page.

The site uses a small Python standard-library generator. Its output is ordinary static HTML, CSS, and JavaScript in `site/`, compatible with free GitHub Pages hosting. No npm dependencies, backend, framework, or API key are required.

## Run and verify

Requires Node.js 22+ and Python 3.13+ for the development commands. No dependency installation is needed.

```sh
npm start
```

This builds the pages and serves them at http://127.0.0.1:4173. After editing content, rebuild and refresh the browser:

```sh
npm run build
npm run lint
npm test
```

`lint` checks JavaScript syntax, stale generated HTML, balanced HTML, local assets/links and cross-page anchors, duplicate IDs, image alternative text, and GitHub file-size limits. Tests cover the effects preference, metadata escaping, invalid project configuration, required build tags, and recipe-page headers.

There is no automatic file watcher. CSS and JavaScript edits require only a refresh.

## Where to edit

| File | Purpose |
| --- | --- |
| `content/profile.json` | Name, handle, role, biography, contact details, and footer credit |
| `content/projects.json` | Every project: text, tags, role, links, and its `build` / `track` / `tier` labels |
| `content/pages/home.html` | Homepage: hero, dialogue lines, featured projects, experience, about, character sheet |
| `content/pages/projects.html` | Full menu layout and filters |
| `content/pages/<project>.html` | Recipe pages: a project's deep dive with diagrams, media, and source excerpts |
| `content/art/bar-scene.svg` | Generated pixel-art scene (do not edit by hand; see below) |
| `templates/layout.html` | Shared head, status bar, glass sprites, and footer for every page |
| `site/styles.css` | Design tokens, window/panel components, recipe-page styles, responsive layouts |
| `site/fx.js`, `site/app.js` | CRT effects preference, dialogue box, clock, filters, video coordination |
| `scripts/build_site.py` | Generator, project schema checks, and display ordering |
| `scripts/make_scene.py` | Regenerates `content/art/bar-scene.svg` |

**Do not edit generated `site/*.html` directly.** A build will replace those files.

## Project fields

```json
{
  "id": "new-project",
  "title": "New Project",
  "category": "Gameplay engineering",
  "track": "gameplay",
  "build": "hand",
  "tier": "feature",
  "year": "2026",
  "role": "Solo developer",
  "summary": "A short, factual description of what the project does.",
  "tags": ["C#", "Unity"],
  "url": "https://github.com/kingslayerrq/new-project",
  "link_label": "View source",
  "featured": false
}
```

| Field | Values | Effect |
| --- | --- | --- |
| `build` | `hand` or `ai` | The small tag on the card and recipe page. Required; the build fails without it. It does not affect ordering. |
| `build_note` | text, optional | Shown only as the tag's tooltip, e.g. which agent was used. |
| `track` | `gameplay` or `software` | Section on the menu page, filter value, and glass sprite. |
| `tier` | `feature` or `small` | Full card, or a compact row under “Small pours”. |
| `featured` | `true` or `false` | Also show the card on the homepage. |
| `private` | `true`, optional | Allows omitting `url`; the card shows “Private repository”. |
| `links` | list of `{label, url}`, optional | Secondary links such as source or a live build. |
| `image`, `image_alt` | optional | Screenshot in `site/assets/`, ideally 1280×720. |
| `snippet` | `{label, code}`, optional | A real code excerpt shown instead of a screenshot. Used when there is no image; with neither, the card shows a pixel glass. |
| `page` | optional | Recipe page name; `url` must be `<page>.html` and `content/pages/<page>.html` must exist. |

Cards appear in the order of `projects.json` (features before small entries). To add a recipe page, copy `content/pages/_recipe-template.html`, set `page` and an optional `drink` name on the project, and keep the `{{recipe_head}}` token: it prints the build tag, menu number, and drink name at the top of the page.

## The pixel scene

`python scripts/make_scene.py` draws the homepage bar scene from rectangles on a 320×180 grid and writes `content/art/bar-scene.svg`, which the build inlines. Animation (rain, neon flicker, blinking windows) is CSS in `site/styles.css` and stops when the visitor turns **CRT FX** off or prefers reduced motion.

## Publish with GitHub Pages

Live site: https://kingslayerrq.github.io/ . Pushing to `main` runs `.github/workflows/pages.yml`, which builds, lints, tests, and uploads **only `site/`**.

Commit `content/`, `templates/`, `scripts/`, `tests/`, `site/`, `package.json`, the workflow, `.gitignore`, and documentation. Original recordings and `research/` stay local.

## Design and media

See `DESIGN_NOTES.md` for the visual direction and `PROJECT_RESEARCH.md` for the repository index and how each project was classified. Fonts load from Google Fonts with local fallbacks; all other assets are local. All artwork is original — no third-party game assets are used.

Balatro uses a silent cropped excerpt of a local recording; Slay the Spire likewise. Clips have WebM sources and H.264 MP4 fallbacks, loaded on demand.

The clones are educational projects. Balatro and Slay the Spire names and third-party artwork belong to their creators.

## Project research

- `PROJECT_RESEARCH.md`: repository index, selection rationale, and provenance evidence.
- `MY_WEB_REVIEW.md`: GameDev Hub source findings and local reconstruction notes.
- `UNITY_2D_REVIEW.md`: inspected gameplay systems and their limits.
