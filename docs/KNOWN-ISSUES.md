# Known issues

The state of the code as submitted in April 2024. Each problem below comes with the fix it needs.

Summarised in both READMEs ([English](../README.md#known-limitations) /
[中文](../README.zh-CN.md#已知限制)); this page holds the detail.

---

## 1. The GPT integration is pinned to a configuration that no longer exists

Three separate problems, all in `interactionSys.Gpt3`:

1. `self.model` is a fine-tuned checkpoint (`ft:gpt-3.5-turbo-0125:3rdprojectgroup:…`) private to the account
   that trained it, so any other key gets a 404.
2. The call is `openai.ChatCompletion.create`, removed in `openai>=1.0`, hence the `openai<1.0` pin in
   `requirements.txt`.
3. `gpt-3.5-turbo` is a legacy generation being wound down regardless.

**The fix**: stop hard-coding a model. Have `Gpt3` read `api_key`, `model` and `base_url` from the
environment, and port `inquiry` to the 1.x client. A configurable `base_url` additionally lets the narrator be
any OpenAI-compatible endpoint, local models via Ollama or vLLM included.

That change would not touch the state model, content definitions, command layer or turn loop; all stay
byte-identical.

## 2. Response parsing is not hardened

The narration layer trusts the model more than it should:

| Where | Problem |
|---|---|
| `interactionSys.py:260, 303, 338, 390` | Bare `except:` swallows everything, including `KeyboardInterrupt`, and hides the real cause |
| `interactionSys.py:266, 308, 316, 345, 414` | After three failed retries `gpt_response` / `result` were never bound, raising `NameError` |
| `interactionSys.py:258, 388` | `parsed_output[keyList[1]]` reads the description by **key order**; a different key order returns the wrong field |
| `interactionSys.py:252-254` | A newline round-trip hack, needed only to make `ast.literal_eval` accept the reply |
| throughout | `ast.literal_eval` and `json.loads` are used at different call sites; the former rejects JSON `true`/`false`/`null` |
| `PCGsys.py:550, 560` | Reward and penalty indices from the model are not validated: out of range raises `IndexError`, non-numeric raises `ValueError`, and the `eventCommandMap` lookup has no `KeyError` guard |

**The fix**: request JSON mode or structured outputs so most parse failures stop happening at all; validate the
reply against the expected schema and clamp indices to the menu the engine supplied; and when retries are
exhausted, fall back to an engine-generated template description. A dead narrator should degrade the prose,
not stop the game; today it stops the game.

## 3. The test suite has drifted

`modules/testMain.py` was written against a mid-project revision of the command API, and 1 of its 7 cases
passes today:

| Test | Why it fails |
|---|---|
| `test_move` | Looks up `get_Actions()["Move"]`; the registry key is now `"Go"` |
| `test_pickUp`, `test_equip`, `test_consume` | Pass `None` where the command layer now writes `action.nameForDescription`, so a real `Actions` object is required |
| `test_generator` | `npcGenerator.__init__` gained a `worldStatus` parameter |
| `test_attack` | Blocks on the interactive disambiguation prompt (see below) |
| `test_add_itemsOR_drop_items` | Passes |

**The fix**: mechanical. Update the registry key, construct real `Actions` objects, pass `worldStatus`, and
patch `builtins.input` for the interactive paths.

## 4. Smaller things

- **Disambiguation blocks on `input()`.** When several matching items are in reach, `consume` and `pickUp`
  prompt on stdin from inside the command layer, coupling game logic to the terminal, which is what makes
  those paths awkward to test.
- **No save/load.** The world is reproducible from its seeds, but player and inventory state is not persisted.
- **The map visualiser needs a desktop.** `MapGenerator.visualized` uses `cv2.imshow`; on a headless machine
  use `cv2.imwrite` instead, which is how the map images in the README were produced.
