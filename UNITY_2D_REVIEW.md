# Unity-2D / Slay the Spire clone — systems review

Reviewed September 17, 2026. Repository metadata confirms `kingslayerrq/Unity-2D` remains private. Inspected the existing local checkout at `C:/Users/Richard/Documents/GitHub/2D`, which resolves through OneDrive. HEAD: `5996ab8cd3d20b6ca6d52f04b5e0a3a747cb74b8`. The only reported working-tree modification was an existing font asset; it was not touched. No Unity project files were changed.

## Portfolio changes

Added `site/slay-the-spire.html`, expanded the homepage feature, and preserved `#code-spire`. The case study reuses supplied gameplay, the previously approved queue excerpt, and a short damage-resolution excerpt. It does not expose a full private source tree or private repository links. Publication remains deferred.

## Evidence map

Paths below are relative to `Assets/Scripts/CardGame/` unless specified otherwise.

| Topic | Evidence | Supported description |
| --- | --- | --- |
| Action queue | `Actions/CombatActionQueue.cs`, `ICombatAction.cs`, `PlayCardAction.cs`, `RequireDiscardSelectionAction.cs` | FIFO queue, coroutine execution, callbacks, selection action waiting for confirmation/cancellation. Nested enqueued work does not complete before the parent callback automatically. |
| Resolution | `CombatSystem.cs`, `Managers/CombatManager.cs` | Spend/play wrappers; trigger and condition evaluation; gameplay mutation delegated from actions. |
| Damage | `Actions/DamageAction.cs`, `Events/DamageEvent.cs`, `Unit/BaseUnitInstance.cs` | Fresh payload per living target; outgoing then incoming modifiers; block before health; before/after hooks; deferred defeat/disposal via completion callback. |
| Typed hooks | `Combat/Hooks/CombatHooks.cs`, `Managers/BuffManager.cs` | Interface-based dispatch across active buffs, cleanup after each hook phase; no ScriptableObject event bus. |
| Concrete buffs | `Buff/BuffInstances/StrengthBuffInstance.cs`, `VulnerableBuffInstance.cs`, `TempStrengthBuffInstance.cs` | Attack-only additive Strength, rounded-up 1.5x Vulnerable, temporary Strength clears at turn end. |
| UI observers | `UI/UnitHealthbar.cs`, `Buff/BuffListView.cs`, `Deck/CardPile.cs` | C# events notify views, explicit initialization and unsubscription; healthbar tweens independently of action completion. |
| Data/runtime split | `Card/CardData.cs`, `Card/CardInstance.cs`, `Buff/BuffData.cs`, `Buff/BuffInstance.cs` | Shared asset definitions versus mutable costs, ownership, upgrades, stacks. |
| Rule authoring | `Card/CardEffects/CardEffectData.cs`, `Configs/DmgCardEffectConfig.cs`, `Effects/DmgCardEffect.cs`, `Card/DynamicValue.cs` | SerializeReference polymorphic classes, typed configs, triggers, all-pass conditions, dynamic scaling and multi-hit actions. |
| Editor tools | `Assets/Editor/CardEffectDataDrawer.cs` | Type picker, reorderable conditions, validation, automatic config matching through RequiredConfigType. |
| Movement semantics | `CombatSystem.cs` | OnDiscard rules for CardEffect-caused movement, distinct from EndTurn; OnExhaust rules and buff hooks. |
| Turns/intents | `Managers/CombatManager.cs`, `Unit/BaseEnemyUnitInstance.cs`, enemy intent implementations | Explicit states and shared actions. Intent choice is random from available entries; snapshot informs targets, not advanced planning. |
| Maps | `Map/MapGenerator.cs`, `SeedUtility.cs`, `Nodes/NodeFactory.cs` | Graph construction/reachability; fixed floors; MRV heuristic with weighted candidate ordering and backtracking; per-node category seeds. |
| Run randomness | `Managers/RunManager.cs`, `Deck/CardPile.cs` | Category-specific System.Random streams; Fisher–Yates-style pile shuffle. Other paths still use UnityEngine.Random, so no full replay-determinism claim. |
| Progression | `Compendium/GlobalProgressionManager.cs`, catalogs, unlock evaluators, `Unlock/CompositeUnlockCondition.cs` | ID-indexed records, progression notifications, All/Any unlock composition. |
| Saves | `Compendium/Persistence/IProgressionStore.cs`, `LocalJsonProgressionStore.cs` | Version migration, dictionary serialization, temporary-write validation, backup fallback, corrupt-file archival, checkpoints. File.Replace has a copy fallback, so universal atomicity is not claimed. |
| Tests/build | `Assets/Editor/Tests/`, repository README/workflow | Existing tests for reload/checkpoints, dictionary round trips, v1 migration, card IDs, entry scene, WebGL Discord exclusion. Source inspected; not rerun for this website-only change. |

## Important distinctions

- The damage example (6 base + 2 Strength, then ceil × 1.5, minus 5 block = 7 health damage) is illustrative, explicitly labeled, and assumes an Attack card and sufficient target health. It is not a measured screenshot result.
- DamageEvent.Amount is incoming damage after modifiers, not post-block health loss.
- EnemyDmgIntent currently passes CardType.None, so the Attack-only Strength/Vulnerable implementations do not apply there.
- BuffManager iterates its active list directly and follows list order. There is no explicit modifier priority or mutation-safe dispatch guarantee.
- Damage effects resolve their DynamicValue before enqueuing their hits. This is not necessarily re-evaluated between individual hits.
- The callback in DmgCardEffect checks the original context targets even when a secondary target configuration chooses a different list; do not claim complete target-routing correctness.
- Map generation contains the documented search algorithm, but a complete invariant proof or automated map validation was not performed. Several noncombat node handlers remain placeholders.
- Relic catalogs/progression exist; no blanket claim of a complete relic gameplay system.
- A local font asset was already modified. It and all other Unity files remain untouched.

## Verification scope

Run `npm run lint` and `npm test` in the portfolio workspace. The HTML validator discovers the new case-study page and checks cross-page anchors. Browser QA covers the new homepage link, both themes, source-code wrapping/scrolling, and responsive diagrams/table. Existing Unity tests were read, not run, because the change is portfolio content and styling; gameplay behavior is described from inspected code and supplied footage.

Unity ScriptableObject terminology was checked against the official Manual via Context7. No new dependencies or Unity configuration changes were needed.
