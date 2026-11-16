# Repository index and project selection

Indexed November 16, 2026 through the GitHub API: 67 repositories under `kingslayerrq` (58 owned, 9 forks). For each owned repository the index recorded commit count, languages, root files, commit authors, and recent commit messages. Forks are omitted from the portfolio because upstream code does not establish the owner's contribution. Private repositories were reviewed; only the ones shown on the site are named here.

Audience: recruiters for software engineering and gameplay engineering roles. Ordering rule: hand-coded work first, AI-assisted work second, every entry labeled.

## How provenance was classified

Labels marked **owner-confirmed** were set by Richard on November 16, 2026 and override repository signals. The rest were classified from evidence, strongest first:

1. **Agent files in the repository** — `CLAUDE.md`, `AGENTS.md`, `.claude/`.
2. **Commit trailers and branches** — `Co-Authored-By` agent trailers, `claude/…` or `codex/…` branches.
3. **Shape of the history** — a large, fully documented codebase arriving in one or two commits.
4. **Date** — work from 2023 and early 2024 predates the agent tooling used later.

Entries marked *inferred* rest on signal 3 only. Changing a label is a one-field edit in `content/projects.json`.

## Featured — hand-coded

| Project | Repository | Track | Basis |
| --- | --- | --- | --- |
| Slay the Spire Clone | `Unity-2D` | Gameplay | **Owner-confirmed.** 39 solo commits, Mar–Nov 2026. |
| Balatro Clone | `Balatro-Clone` | Gameplay | **Owner-confirmed.** 20 hand commits, Mar–Jun 2025. AI was used only for a recent refactor (pull request #1, Nov 2026), noted at the end of its recipe page. |
| UnderWatch | `Booomjam2026` | Gameplay | **Owner-confirmed:** Richard wrote most of the code himself (32 of 39 commits). The repository does contain a `CLAUDE.md`. |
| GameDev Hub | `my-web` | Software | 143 solo commits, Nov 2024–Feb 2025, no agent files or trailers. |
| Multithreaded Run-Length Encoder | `lab3`, `lab4` | Software | NYU Operating Systems labs, late 2023: pthread worker pool; FAT32 recovery tool. |
| Hollow Knight–Style Platformer | `IntermediateGamDevFinal` | Gameplay | 135 commits, 65 PRs, Fall 2023; four contributors, owner has the most commits (55). Uses third-party art. |
| GGJ 2026 Jam Game | `GGJ2026` | Gameplay | 44 commits, owner 30; no agent files or trailers. *Inferred.* |

## Featured — AI-assisted

| Project | Repository | Track | Basis |
| --- | --- | --- | --- |
| Heritage Afterlife | `heritage-afterlife` (private) | Software | `CLAUDE.md`, `AGENTS.md`, agent trailers, `codex/…` branches. 85 commits, 17 PRs. |
| Network — Playdate Prototype & Level Editor | `playdate` (private) | Gameplay | *Inferred:* editor, tests, and six variants landed in a handful of commits. Listed on the résumé. |
| Heritage Devlog | `heritage-devlog` | Software | `CLAUDE.md`, `AGENTS.md`, agent trailers. Live on GitHub Pages. |
| AI Resume Factory | `VB_Resume` | Software | `AGENTS.md` in the repository. |

## Small pours

| Project | Repository | Label | Basis |
| --- | --- | --- | --- |
| Search Under a Budget | `AI-search` | Hand-coded | 15 commits, early 2024. |
| Endless Dodger | `InfScrollBg` | Hand-coded | 4 commits, Dec 2024. |
| Ecosystem | `Ecosystem` | Hand-coded | 2023 coursework. |
| Cloud Duel | `IntroGameDevFinal` | Hand-coded | 2023 GameMaker coursework. |
| Balatro AI | `balatro-ai` | AI-assisted | *Inferred:* ~180 KB of Python and Lua across 6 commits. |
| Last Seen | `discord-last-login` | AI-assisted | *Inferred:* full plugin, docs, and tests in 2 commits. |

## Where the card images come from

| Image | Source |
| --- | --- |
| `underwatch.jpg` | The local WebGL build run in headless Chrome; frame from the gym camera feed during a new game. |
| `platformer.jpg` | `Assets/Scenes/Main.unity` rendered from the main camera in Unity 6000.3 batch mode (project is 2022.3; edit-mode render, cropped). |
| `ggj-2026.jpg` | `Assets/Scenes/RQScene.unity` rendered the same way. Edit-mode render: runtime-spawned objects are absent. |
| `heritage-devlog.jpg` | The live site in headless Chrome. |
| `network-editor.jpg` | `tools/editor/index.html` from the repository, opened locally with the bundled “Chase map”. |
| Code cards | Verbatim excerpts: `nyuenc.c` (lab3, debug comments trimmed) and `main.py` (VB_Resume, dedented). The Heritage Afterlife card is a diagram summarized from its README, not source code. |
| `spire.jpg`, `balatro.jpg`, `my-web-*.png` | Earlier local recordings and a local reconstruction; see `MY_WEB_REVIEW.md` and `UNITY_2D_REVIEW.md`. |

## Profile content

Experience, education, skills, certification, and the Overwatch line come from Richard's résumé. The character sheet section comes from his Duke GDDI character sheet; the “special skills” meter levels are read off its radar chart by eye. The phone number and photos are deliberately not published.

## Considered but not shown

- **OpenJetLag** (`openjetlag.github.io`): removed at the owner's request — not his project.
- **Forks** (`mindcraft`, `pensieve_ai`, `LeetHub`, and others): upstream work.
- **Credit-Card-Fraud-Detection-Project** (2017): its headline accuracy is uninformative for a 0.172% positive class.
- **AI-RL**, **OOPFinalProject**, **Froglid**, and empty or scaffold-only repositories: too small to help a recruiter.
- **Current Duke coursework**: in progress.
- **Profile, notes, and practice repositories**: not projects.

## Source notes

- Balatro excerpt pinned to commit `437cb76`, which predates the refactor.
- Slay the Spire recipe page describes commit `5996ab8`; the repository is now public.
- GameDev Hub recipe page describes commit `0167189`; its cloud deployment is offline. See `MY_WEB_REVIEW.md`.
- No claims of production adoption, measured AI win rates, or feature parity with commercial games are made beyond what the résumé states.
