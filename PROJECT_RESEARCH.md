# Portfolio project selection

Reviewed September 16, 2026. The public GitHub inventory contained 32 repositories; the user also explicitly supplied the private Unity-2D project. Selected five complementary projects rather than filling the portfolio with forks and sparse coursework.

| Project | Reason to feature | Evidence |
| --- | --- | --- |
| Balatro-Clone | Strong visual centerpiece; gameplay rules, data structures, and presentation | `Assets/Scripts/ManagerScripts/HandAnalyzer.cs`, `ScoreCalculator.cs`, ScriptableObject definitions; supplied gameplay |
| Unity-2D / Slay the Spire clone | More extensive gameplay architecture; action queue, effects, progression, build workflow | `CombatActionQueue.cs`, action/effect and persistence file inventory, README; supplied gameplay |
| balatro-ai | Connects the game-development and CS narratives | `ai/balatro_env.py`, `ai/train.py`, replay/evaluation file inventory |
| discord-last-login | Shows maintainable software structure and testing beyond games | README, `src/core/presence-tracker.js`, core/integration split, test inventory |
| AI-search | Clear algorithmic fundamentals | README documenting iterative deepening and hill climbing with random restarts |

## Public source links

Added at the owner's request: **my-web / GameDev Hub**, a prominent full-stack project with a dedicated case study. Inspected the React client, Express controllers, Prisma schema, upload/auth middleware, Discord gateway relay, and tests. Source: https://github.com/kingslayerrq/my-web/tree/0167189858f31c9c3b05174c140699414607dbe8. See `MY_WEB_REVIEW.md` for the detailed evidence and reconstruction limits. This adds a sixth selected project.

- Profile/biography: https://github.com/kingslayerrq/kingslayerrq
- Balatro: https://github.com/kingslayerrq/Balatro-Clone/tree/437cb76f8d5d429ce0fe1fb67dae548e46150add
- Balatro AI: https://github.com/kingslayerrq/balatro-ai/tree/2e6e65d79c26920b3360fd8aaa8cea9eab031568
- Last Seen: https://github.com/kingslayerrq/discord-last-login/tree/60a8049a86dfb5e44b926aadaec2fcfaebfc31f5
- AI-search: https://github.com/kingslayerrq/AI-search/tree/6d2b7ca4851a8d3affa9e7c9400527f985a9bccb

Unity-2D is private. Owner approved publishing the short `CombatActionQueue.cs` excerpt in this session. Descriptions and excerpt correspond to commit `5996ab8cd3d20b6ca6d52f04b5e0a3a747cb74b8`.

Expanded at the owner's request into `site/slay-the-spire.html`: action scheduling, typed buff hooks versus C# UI events, per-target damage resolution, ScriptableObject/runtime separation, custom effect authoring, procedural map search, and versioned progression persistence. Includes the existing queue excerpt and a short damage pipeline excerpt. Full evidence and limitations are in `UNITY_2D_REVIEW.md`; the Unity checkout was not modified.

## Considered but not selected

- AI-RL: read README and `helper.py`; a small dice-learning exercise. Balatro AI offers a richer systems story.
- Credit-Card-Fraud-Detection-Project: read README. Its headline 99% accuracy is uninformative for the documented 0.172% positive-class rate, so the portfolio does not repeat it as a success claim.
- Ecosystem: source inventory is small and no matching supplied footage; lower priority than the two requested game projects.
- Game-jam entries: potential future additions once role, contribution, and gameplay materials are established.
- mindcraft, pensieve_ai, and other forks: omitted because upstream functionality alone does not establish the owner's contributions.

No claims of production adoption, performance gains, measured AI win rate, passing upstream tests, or complete feature parity with commercial games were added. The visual Last Seen panel and AI/search diagrams are illustrative UI, not screenshots or measured results.
