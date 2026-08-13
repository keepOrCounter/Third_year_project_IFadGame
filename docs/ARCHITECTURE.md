# Architecture

Design notes for the IFadGame engine. This document assumes you have read the
[README](../README.md) and want to change or extend the code.

---

## 1. The boundary

There is exactly one architectural rule, and every module is placed relative to it:

> **The simulation owns all state. GPT owns none of it.**

Concretely, GPT-3.5 is invoked at exactly four points, and at each one its output is either pure prose or a
value constrained to a set the engine defined:

| Call site | `interactionSys.py` | What the model may return |
|---|---|---|
| Describe the current location | `OutputGenerator.locationDescription` :200 | Prose only |
| Name and describe a triggered event | `OutputGenerator.eventDescription` :283 | Prose only |
| Decide how an event develops | `OutputGenerator.eventDevelopment` :318 | Prose **+ indices into engine-supplied reward/penalty lists** |
| Describe an arbitrary state change | `OutputGenerator.generalDescriptor` :364 | Prose only |

A fifth call, `foodGenerate` :351, asks the model to invent a new `Food` item against a fixed JSON schema. It
is the one place where GPT authors content rather than describing it, and it is not wired into the main loop —
it exists as a demonstration of schema-constrained content generation.

`interactionSys.py` is the only engine module that imports `openai` (`modules/test.py` is a scratch script, not
part of the engine). If you are adding a feature and find yourself wanting the model to decide a fact, add the
fact to the simulation and let the model describe it instead.

---

## 2. Module map

Dependencies point downward only; `status_record` knows about nothing above it.

```
                       main.py
                   (turn loop, rules)
                          │
          ┌───────────────┼────────────────┐
          ▼               ▼                ▼
     PCGsys.py     interactionSys.py   Pre_definedContent.py
   (generation)     (GPT + parsing)    (commands + content)
          │               │                │
          └───────────────┴────────────────┘
                          ▼
                  status_record.py
                (pure state, no logic)
```

| Module | Responsibility | Explicitly not its job |
|---|---|---|
| `status_record.py` | Data classes for everything that exists: items, NPCs, locations, terrain, player, world, events, actions, buffs. Getters/setters only. | Any game rule, any generation, any I/O |
| `Pre_definedContent.py` | `Commands` (verb implementations), `MapPcgRule` (CA rules), `character_effectSys` (buff engine), `DefininedSys` (content registry), `OutputTransfer` (numeric→linguistic table) | Deciding *when* things happen |
| `PCGsys.py` | Generating map, objects, NPCs and events; `PCGController` sequences them each turn | Mutating player state directly (it calls `Commands`) |
| `interactionSys.py` | The GPT client, prompt assembly, response parsing, and the natural-language command parser | Knowing any game rule |
| `main.py` | `rule_system` — per-turn survival rules, clamping, scoring, death — and the loop that orders everything | Content definitions |

---

## 3. The turn cycle

From [`main.py:160`](../modules/main.py):

```python
while begin:
    if not worldStatus.skipTurn:
        game_rule.scoring()                     # main.py:57
        game_rule.eachTurn_handler()            # main.py:65
        pcgSystem.locationPCG_each_turn()       # PCGsys.py:602
        game_rule.turnInfoClear()               # main.py:104
    else:
        worldStatus.skipTurn = False

    descriptionGenerator.text_output()          # flush accumulated descriptions
    user_input = input("What would you do?>>>")
    inputAdapter.command_translator(user_input) # interactionSys.py:583
```

**`skipTurn`** is the engine's way of saying "that input did not count as a move": it is set when the spell
checker had to correct the player's typing (so they can confirm), and when a command failed to find its
target. The world does not advance on a turn the player did not really take.

### `eachTurn_handler` — survival rules

1. `buffHandler()` — evaluate every buff's trigger/end condition, run active buff effects, expire buffs whose
   `timeLimit` has elapsed.
2. `naturalChange()` — decrement `freshness` on every tracked item (food past zero becomes inedible), then
   apply `naturalAP_reduce = 2` and `naturalThirst_reduce = 4`.
3. Clamp and cascade: exhausted action points bleed into HP; zero thirst bleeds into HP; HP ≤ 0 ends the game.

### `locationPCG_each_turn` — world advance

From [`PCGsys.py:602`](../modules/PCGsys.py):

1. Flush any pending narration (`generalDescriptor`).
2. `npcChoice` — each NPC in the current location attacks or flees; wounded NPCs (HP ≤ 0.2) get a rising
   escape probability.
3. `map_info_update` — if the player has crossed an area boundary, generate the new area.
4. `event_handler` — advance every in-flight event: ask GPT how it develops, apply the chosen
   rewards/penalties, retire it if it succeeded or failed.
5. `surroundingLocation` — resolve the four neighbouring cells for the description prompt.
6. Branch on whether the player has been here before:
   - **Visited** → reuse the stored `Location` object, including its previously generated description.
   - **New** → spawn objects (`objectGeneration(1, 3, terrain)`) and NPCs (`npcGeneration(0, 2, terrain)`),
     store the `Location`, and ask GPT for a fresh description.
7. `event_triger` — evaluate untriggered event conditions and promote at most one per turn.

---

## 4. State model

All in `status_record.py`. The item hierarchy is a plain single-inheritance tree:

```
Items  (item_name, possibleWeight, weight, commandSuitable)
├── Liquid              thirst_satisfied
├── Food                AP_recovery, freshness, eatable, thirst_satisfied
├── Tool                durability
├── LandscapeFeature    immovable; may hold a Liquid  (streams, grass, aloe vera)
├── EnvironmentElement  immovable; harvestable
├── Transportation      suitablePlace, APReduce
├── Weapon              attack, durability
├── Container           capacity, currentCapacity, liquid
└── Suit                worn equipment
```

`possibleWeight` is the single mechanism controlling where an item appears: a dict from terrain name to a
0–20 weight. `DefininedSys.__init__` inverts these dicts once at startup into per-terrain spawn tables
(`definitely_Object` for weight ≥ 20, `possible_Object` + `possible_Object_Weight` otherwise), so generation
at runtime is a weighted sample rather than a scan.

Three objects are threaded through nearly every constructor:

- **`Player_status`** — HP, AP, thirst, carry weight, inventory (`dict[str, list[Items]]`, keyed by item name
  so duplicates stack), buffs, equipment, current action.
- **`Map_information`** — the current area's terrain grid, the area coordinate, and `visitedPlace`
  (`dict[(x, y) -> Location]`), which is the engine's memory of everywhere the player has been.
- **`globalInfo`** — per-turn scratch space and world-level dials: `move_dLevel` (accumulated movement
  difficulty), `skipTurn`, `current_description` (the buffer flushed to the terminal), `descriptor_prompt`
  (the JSON being assembled for the next GPT call), and the natural drain rates.

---

## 5. Procedural generation

### Seeding: reproducible without persistence

[`MapGenerator.map_Seed`](../modules/PCGsys.py) (:35) keeps `__generated_map: dict[area_coord -> seed]`.
Seeds are drawn from a pool of 100 consecutive integers, refilled from a new random base when exhausted.
Because the seed is looked up by area coordinate, `np.random.seed(map_seed)` before generation guarantees an
area regenerates identically on every visit — the terrain is *reproducible* rather than *stored*.

Layered terrains derive their own seeds by offsetting the area seed by the terrain's index, so each layer
varies independently while staying deterministic.

### Cellular automata: noise to landmass

[`game_map_generation`](../modules/PCGsys.py) (:101):

1. Seeded random noise over the grid, with land probability taken from the area type (sea areas and land areas
   have different base ratios).
2. Evolve with `cellpylib.evolve2d` for `cellular_timesteps` generations under the base land rule
   (`MapPcgRule.random_map_update_SIslands`, a death-limit/birth-limit smoothing rule) — this is the step that
   turns the left-hand image in the README into the right-hand one.
3. For each remaining terrain in ID order: randomly seed it onto cells whose current terrain is in its
   `allowedAppearUpon` list, evolve it under its own rule, then merge — cells the rule left as `-1` keep their
   previous terrain.

Finally, in **land** areas every remaining sea cell is rewritten to `river` — which is why inland water in a
land area reads as river rather than ocean, and why `river` has `possibilityOfGenerate = 0` and no CA rule of
its own: it is never seeded, only substituted.

The ordering plus `allowedAppearUpon` is what produces geological plausibility without any explicit
constraint solver:

| Terrain | ID | Grows on | Rule | Move cost |
|---|---|---|---|---|
| sea | 0 | — | islands | 4 |
| land | 1 | sea | islands | 1 |
| river | 2 | sea | — | 4 |
| forest | 3 | land | default | 1 |
| beach | 4 | land | sand | 2 |
| desert | 5 | land | desert | 3 |
| mountain | 6 | land, forest, beach, desert | default | 4 |
| highland snowfield | 7 | mountain | snowfield | 5 |
| town | 8 | everything habitable | town | 1 |
| grassland | 9 | land | default | 1 |

### Area paging

[`map_info_update`](../modules/PCGsys.py) (:229) checks whether the player's coordinate still falls inside the
current area's bounds; if not it computes the new area coordinate, decides its type from the parity of the
normalised coordinates (both odd → land area, otherwise sea area), and generates it. The world is therefore
unbounded, and only the current area's grid is ever held in memory — visited *locations* persist in
`visitedPlace`, but visited *terrain* is recovered from its seed.

---

## 6. Events

Events are declared in `DefininedSys.__pre_def_events_frameWork` (:1243) as data, with conditions as lambdas
over `(player, mapInfo, events, worldStatus)`:

```python
PassivityEvents(
    "", "survival crisis", "low action point",
    ["increase action point", "increase maximum action point"],   # possible_reward
    ["decrease action point", "decrease maximum action point"],   # possible_penalty
    -1,                                                           # time_limit, -1 = unbounded
    "",
    lambda player, mapInfo, events, worldStatus: player.get_action_point() < 40,
)
```

Lifecycle, managed by `EventsTriggered`:

```
UnTriggered_passivity_events ──(condition true)──▶ eventsHappening ──(success/fail)──▶ eventsTriggered
        ▲                                                                                    │
        └────────────────────────(condition no longer true)──────────────────────────────────┘
```

Each turn, `event_handler` (:525) asks GPT how each in-flight event develops. The reward/penalty indices in
the reply are looked up in `eventCommandMap` (:1314), which maps a human-readable effect name to a
`(command_name, args)` pair, and then in `commandTranslate` (:1336), which maps the command name to the actual
bound method. **This two-step indirection is the containment mechanism**: the model chooses from a list of
strings; only the engine knows what those strings do.

`DisasterEvents` differ by carrying an explicit `end_condition` — a dust storm ends when you leave the desert,
not when the model says so.

---

## 7. Buffs

`character_effectSys` (:1035) is a small scheduler. A `Buff` carries an `exe_function` run every turn while
active, an `end_Function` run on expiry, a `timeLimit` (`-1` = until its end condition fires), and a `level`
(`potential` / `low` / `median` / `high`) that scales severity. `rule_system.buff_triggered` evaluates every
registered buff's trigger and end conditions once per turn, so buffs can appear from the world state alone —
`thirsty` applies itself when thirst reaches zero, without any command asking for it.

---

## 8. The numeric→linguistic layer

`OutputTransfer.outputWordMap` (:16) is a nested dict of the form:

```python
"precentageHP": {
    "name": "HP",
    "function":   [lambda p: p == 1, lambda p: 0.8 <= p < 1, lambda p: 0.41 <= p < 0.8, lambda p: p < 0.41],
    "map_result": ["no hurt",        "little hurt",          "moderate hurt",           "intense hurt"],
}
```

`generalTransfer` (:204) walks an object's `vars()`, finds each attribute in the table, evaluates the
predicates in order and substitutes the matching word. Attributes absent from the table are dropped entirely —
so the table is also the allowlist deciding what the model is even *told about*. Adding a field to a state
class does not leak it into prompts until you add it here.

The special `map_result` value `"<origin>"` passes the raw value through, used for names.

---

## 9. Natural-language input

[`InputTranslator.command_translator`](../modules/interactionSys.py) (:583):

1. **Spell-check** (`spell_checker` :487, pyspellchecker) with an in-game whitelist (`aloe`, `vera`,
   `unequip`). If anything changed, the engine asks the player to confirm and sets `skipTurn`.
2. **Grammar classification** (`grammarClassifier` :506, spaCy `en_core_web_sm`): noun chunks give the object,
   a `Matcher` pattern of `VERB (+ ADP)` gives the verb phrase, and `NUM` tokens give quantities. Several
   verbs that spaCy reliably mis-tags as nouns (`attack`, `equip`, `unequip`, `rest`) are special-cased.
3. **Fuzzy match**: Levenshtein distance from the extracted verb to each key of `DefininedSys.get_Actions()`.
   Distance ≤ 1 dispatches the command; anything else returns `<Rejected>`.
4. **Dispatch**: the matched `Actions` object holds a list of methods (`command_executed`) and a parallel list
   of argument lists (`command_args`), each pre-seeded with the action itself. The parsed noun is appended,
   every method is called in order, and the noun is popped again so the action stays reusable.

A `systemRole` prompt for GPT-based command translation is built at :587 but the shipped path is the local
pipeline above — the LLM route was kept for comparison, not used for parsing.

---

## 10. Extension guide

**Add an item.** Append to `DefininedSys.__def_items` (:1145) with a `possibleWeight` entry for every terrain.
Nothing else — the spawn tables are rebuilt from it at startup. If the item has attributes you want narrated,
add them to `OutputTransfer.outputWordMap["items"]`.

**Add a terrain.** Add a `Terrain_type` to `__terrain_type` (:1352) with a unique `terrain_ID`, an
`allowedAppearUpon` list, a rule from `MapPcgRule` (or a new one), a `move_dLevel` and a `visualizedColor`
(BGR, for `cv2`). Then add that terrain's key to the `possibleWeight` dict of **every** existing item and NPC —
they are read by key, and a missing key raises `KeyError` at startup.

**Add a verb.** Implement it as a method on `Commands` taking `(self, action: Actions, ...)`, then register it
in `__def_actions` (:1277):

```python
"Craft": Actions("Craft",
                 [preDefinedCommands.craft, preDefinedCommands.ActionCost],
                 [[], []],      # extra args per method, beyond the action itself
                 3,             # action point cost
                 1,             # thirst cost
                 ["craft"])     # tags
```

The parser picks it up automatically — the command vocabulary is `get_Actions().keys()`. Note that the
registry key is what the player's input is matched against, while `actionName` is what the rules see.

**Add an event.** Append a `PassivityEvents` or `DisasterEvents` to `__pre_def_events_frameWork` (:1243). Every
string in `possible_reward` / `possible_penalty` must exist as a key in `eventCommandMap` (:1314), otherwise
the lookup fails when GPT selects it.

**Add a buff.** Write the effect and expiry methods on `character_effectSys`, register a `Buff` in
`__def_buff` (:1301), and add `"add …"` / `"remove …"` / `"upgrade …"` entries in `eventCommandMap` if events
should be able to apply it.

---

## 11. Fine-tuning data pipeline

`data/` holds the supervised fine-tuning experiment described in the README.

```
backup.json          hand-written (game state → ideal narration) pairs, alternating user/assistant
    │
    ├─ transfer.py   pairs them up, prepends the system role, emits OpenAI chat JSONL
    ▼
output.jsonl         16 training examples for the general descriptor
eventTune.jsonl       9 training examples for event narration
    │
    └─ check.py      format validation + tiktoken token accounting (adapted from the OpenAI cookbook)
```

`check.py` reports missing keys, unrecognised roles, examples lacking an assistant turn, and per-example token
distributions — worth running before any paid fine-tune. Note that `transfer.py` hard-codes its input and
output filenames at the bottom of the file.

A copy of the abstraction table from §8 sits in `transfer.py` as a local `table` variable. It is assigned but
never read — a leftover from a version that inlined the vocabulary into each training prompt. If this
experiment is resumed, either wire it in deliberately or import the real table from `OutputTransfer` rather
than keeping a second copy that can drift.
