# GameDev Hub — source review and reconstruction

Reviewed September 17, 2026 at public commit [0167189](https://github.com/kingslayerrq/my-web/tree/0167189858f31c9c3b05174c140699414607dbe8).

## Portfolio outcome

GameDev Hub is now the third major homepage project. `site/my-web.html` contains original UI screenshots, architecture, the publishing workflow, two source excerpts, pinned source links, and engineering reflection. No publication or cloud resource creation was performed.

## Source findings

- React 18.3.1/Vite 5.4.11 client with Chakra, Tailwind, Redux, React Hook Form, and Axios; Express API with Passport, bcrypt, JWT, Redis sessions, and a WebSocket relay.
- Prisma 5.22/PostgreSQL schema covers users, connections, Discord bots, profiles, collaborators, games, statistics, comments, devlogs, tags, media, files, and images. Self-related comment replies and explicit game/media/profile relations demonstrate relational modeling.
- `client/src/pages/UploadGamePage.jsx` initializes a game ID before a multipart update. The form serializes metadata and per-file options. `server/controllers/userController.mjs` groups media/file inserts in a Prisma transaction, then connects tags and updates the listing. S3 keys include the game ID. Error handling attempts object deletion.
- `server/controllers/gameController.mjs`, `searchGames`, matches title/description without case sensitivity, filters public/non-deleted records, counts results, paginates with take/skip, and includes card relationships.
- `server/middleware/passportMiddleware.mjs` handles local credentials and Discord account linking. Client bearer-token handling and Redux profile state connect the UI and API.
- `server/controllers/discordController.mjs` tracks gateway sequences and session IDs, sends heartbeats, handles reconnect signals, and includes a resume path. Events feed the browser log console. A separate interceptor handles API 429 retry delays.

## Factual limits

This is an archived development project. No adoption or performance numbers were inferred from placeholder landing-page counters. Screenshots contain synthetic records, zero statistics, and supplied gameplay images. They do not verify persistence, S3, real authentication, or Discord operation.

The transaction excludes S3 objects and the later game update. Upload visibility flags exist in metadata, but the uploader uses `public-read`; private-file security is not claimed. Error cleanup uses asynchronous callbacks that need awaiting. Collaborator uniqueness constraints deserve review before claiming unrestricted many-to-many collaboration. Some navigation/provider UI is unfinished, so the case study does not claim every visible control works.

## Reproduce the local UI

The original clone is under ignored `research/my-web/`. Dependencies were installed from its existing pnpm lockfile with `pnpm install --frozen-lockfile`; Prisma's client was generated. No dependencies were added to the portfolio and no real credentials were supplied.

`research/my-web-preview-api.mjs` is a separate Node standard-library fixture server, not the original backend. It binds only to loopback port 3000. It provides synthetic login/profile/catalog/search data and local images; unsupported endpoints return 501. It normalizes duplicated `/api/api/` prefixes from the original client in this environment. It connects to no external services and stores no durable data.

The only original client source change is a reconstruction banner in `client/index.html`. To run in two PowerShell terminals, starting in the portfolio workspace:

```powershell
node research/my-web-preview-api.mjs
```

```powershell
Set-Location research/my-web/client
$env:VITE_API_BASE_URL='/api'
node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173 --strictPort
```

Visit `http://127.0.0.1:5173/games`. For the publishing form, use the original login screen with `demo@example.test` and any nonempty password. This is fixture-only access; use a made-up password. Upload submission is unavailable. These ignored research files stay local and are not included in the public portfolio package.

## Verification

- Original ESLint: `node node_modules/eslint/bin/eslint.js client server` from clone root, exit 0.
- Prisma generation: `node node_modules/prisma/build/index.js generate --schema prisma/schema.prisma` from `server/`, completed.
- Original client build: `node node_modules/vite/bin/vite.js build` from `client/`, exit 0. Warnings include missing `./src/output.css`, a large JS chunk, and outdated browser data.
- Original Jest: `node --experimental-vm-modules node_modules/jest/bin/jest.js --runInBand --coverage`, with `NODE_ENV=test`, from `server/`. All four suites and 41 assertions passed, but the command exited 1 because Redis failed to connect after teardown. This is not a clean passing test run. Log: `research/my-web-tests.log`.
- Docker's daemon was unavailable. No databases or retired cloud services were restored.
- Three real browser captures are in `site/assets/`: `my-web-catalog.png`, `my-web-publishing.png`, and `my-web-upload-options.png`.
- Portfolio lint validates both HTML pages, including cross-page anchors. All three theme tests pass.

A fuller restoration would require disposable PostgreSQL/Redis instances, migrations, infrastructure isolation in tests, and a storage adapter or local object store. Those are separate from this portfolio reconstruction and are not presented as completed.
