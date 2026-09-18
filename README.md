# Richard Qu / Kingslayerrq — portfolio

A personal portfolio inspired by the quiet, analog atmosphere of *Serial Experiments Lain* and the Wired. The homepage introduces Richard; a separate project directory leads to detailed case studies. Both dark and light themes are supported.

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

`lint` checks JavaScript syntax, stale generated HTML, balanced HTML, local assets/links and cross-page anchors, duplicate IDs, image alternative text, and GitHub file-size limits. Tests cover theme defaults/persistence, metadata escaping, invalid project configuration, page registration, shared footer details, and the separation between the personal homepage and detailed project pages.

There is no automatic file watcher. If a preview server is already running, leave it running, execute `npm run build`, and refresh. CSS and JavaScript edits require only a refresh.

## Where to edit

| File | Purpose |
| --- | --- |
| `content/profile.json` | Name, handle, role, biography, contact details, and footer credit |
| `content/projects.json` | Project order, card text, tags, images, destination, and homepage selection |
| `content/pages/home.html` | Personal homepage sections |
| `content/pages/projects.html` | Project-directory introduction and layout |
| `content/pages/<project>.html` | Full case-study content, diagrams, media, and source excerpts |
| `templates/layout.html` | Shared head, navigation, theme button, and footer for every page |
| `site/styles.css` | Design tokens, light/dark palettes, typography, shared components, responsive layouts |
| `site/theme.js`, `site/app.js` | Saved theme, toggling, code disclosures, legacy anchors, and video coordination |
| `site/assets/` | Gameplay clips, screenshots, illustration, and favicon |
| `scripts/build_site.py` | Dependency-free generator and project schema checks |

**Do not edit generated `site/*.html` directly.** A build will replace those files. Keep generated HTML committed so it is easy to preview or copy as a static package.

## Add a project

Add an object to `content/projects.json`. Array order is display order. Use `featured: true` to also show it on the homepage; keeping that to three makes the homepage personal and concise.

```json
{
  "id": "new-project",
  "title": "New Project",
  "category": "Game development",
  "summary": "A short, factual description of what the project does.",
  "tags": ["C#", "Unity"],
  "image": "assets/new-project.jpg",
  "image_alt": "Describe what the screenshot shows",
  "url": "new-project.html",
  "link_label": "Read case study",
  "featured": false,
  "page": "new-project"
}
```

1. Use a unique lowercase hyphenated ID and page name.
2. Put the image in `site/assets/`. `image` and `image_alt` can both be omitted; the generator supplies a typographic panel.
3. Copy `content/pages/_case-study-template.html` to `content/pages/new-project.html`, then write the content. Do not copy a header/footer; they come from the layout automatically.
4. Run build, lint, and tests; inspect the result in both themes and at mobile width.

For a repository-only project, omit `page` and use an HTTPS URL in `url`. A local case-study URL must match `page + ".html"`. No navigation or build-script edit is needed to add a registered page.

To expand an existing project, edit its file in `content/pages/`. Shared classes such as `case-section`, `case-columns`, `case-code`, `case-shot`, and `project-media` support text, code, images, and video. For code, escape `<` as `&lt;` and `&` as `&amp;`. These HTML files are trusted authored content; project JSON strings are escaped automatically.

Removing a project from the registry stops generating it but does not delete a previously generated HTML file. Remove that stale output deliberately if you no longer want its old URL available.

## Publish with GitHub Pages

Live site: https://kingslayerrq.github.io/ . Push updates to `main` to rebuild and deploy automatically.

1. Create a public repository named `kingslayerrq.github.io` for a user site, or another name for a project site.
2. Commit `content/`, `templates/`, `scripts/`, `tests/`, `site/`, `package.json`, `.github/workflows/pages.yml`, `.gitignore`, and documentation. Never upload original recordings, `research/`, or private Unity source.
3. In Settings → Pages, choose GitHub Actions.
4. Run the existing deployment workflow, which builds, lints, tests, and uploads **only `site/`**.

Relative URLs support both user and project sites. The portfolio requires no secrets or environment variables. GitHub Pages is free for public repositories on GitHub Free; custom domains are optional and separate.

References: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages and https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Design and media

See `DESIGN_NOTES.md` for references, the generated illustration prompt, and font choices. Fonts load from Google Fonts with local fallbacks. All other assets are local. There is no autoplay audio, flashing text, or continuous animation. Reduced-motion preferences disable transitions and smooth scrolling.

The generated `site/assets/wired-sky.png` is original atmospheric artwork, not a frame from the anime. Project imagery remains actual gameplay or labeled reconstructions.

Original recordings remain unchanged in the workspace root. Balatro uses a silent cropped 34-second excerpt of `Screen Recording 2025-04-09 at 22.30.15.mov`; Slay the Spire uses a silent cropped 58-second excerpt of `20260916-1736-33.3503293.mp4`. Clips have WebM sources and H.264 MP4 fallbacks, loaded on demand. The Discord conversation recording is excluded.

The clones are educational projects. Balatro and Slay the Spire names and third-party artwork belong to their creators. The previous in-app browser crashed during video playback; the video files passed FFmpeg decoding, but playback should be reviewed in a regular browser. This redesign preserves the same video files.

## Project research

- `PROJECT_RESEARCH.md`: selection rationale and source references.
- `MY_WEB_REVIEW.md`: GameDev Hub source findings and fixture-based local reconstruction instructions. Its retired cloud deployment remains offline.
- `UNITY_2D_REVIEW.md`: inspected gameplay systems and their limits. Private source is not copied wholesale; short excerpts and explanations are included with authorization.

The portfolio build and tests do not assert that either upstream application's tests or builds have been rerun.

