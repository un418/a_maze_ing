# Prompt: update the code diagrams

These diagrams started as a simple experiment: testing the Excalidraw MCP
with [Claude Code](https://claude.com/claude-code). I found it cool and
actually useful, so I kept it in the repo for the curious ones passing by.

This file is the prompt I give it whenever the code has moved and the
diagrams need to catch up.

**How to use it:** in Claude Code, at the repo root, send
`Follow @docs/diagram/UPDATE_PROMPT.md`.

---

`docs/diagram/` holds the code diagrams, each one as an editable `.excalidraw`
source plus its `.png` export:

| File | Shows |
|---|---|
| `01-modules` | which package imports which (A → B: A imports B) |
| `02-classes` | classes, attributes, methods, relations, enums of `core` |
| `03-data-flow` | config → generation → solving → output, step by step |
| `04-dfs-flowchart` | `MazeGenDFS.gen()` as a flowchart |
| `05-braiding-flowchart` | `Braider.gen_braiding()` (non-perfect mode) as a flowchart |
| `06-cell-walls` | a cell's walls as a bitmask, carving two cells, hex output |
| `07-dead-end-flowchart` | `DeadEndSolver` (perfect mode) as a flowchart |
| `08-bfs-flowchart` | `BFSsolver.solver()` (non-perfect mode) as a flowchart |
| `09-makefile` | Makefile targets, prerequisites and recursive `$(MAKE)` calls |

The goal: the diagrams describe the code **as it is on the current branch**,
and nothing else.

## 1. Audit, then wait

1. Read the code: every package `__init__.py` (`__all__`), the entry point
   `a_maze_ing.py`, the `maze_app` orchestration layer, and the imports.
2. Read the text of each `.excalidraw` (a small Python script that prints
   the `text` of each element is enough).
3. List the gaps per diagram: renamed or removed names, new packages or
   classes, new imports, changed signatures, outdated notes
   ("not wired yet", "hardcoded"...), files that no longer exist.
4. Say whether a new diagram is worth adding (e.g. a new package or flow
   no current diagram covers).

**Stop here**: show the list and wait for the go before editing anything.

## 2. Edit the `.excalidraw` files

- Edit the JSON with a Python script kept in the scratchpad, not by hand
  and not in the repo.
- Keep what is still correct: same ids, same positions. Move elements only
  when an addition needs the room.
- New elements follow the conventions below.
- Stay readable: if a diagram becomes too dense, propose a split rather
  than squeezing it.

## 3. Check

- Every text fits inside its container (text width ≤ container width
  minus padding); widen the container if needed.
- Every arrow is bound at both ends (`startBinding` / `endBinding`) and
  the shapes list it in `boundElements`.
- No stale name is left: grep the old names in `docs/diagram/*.excalidraw`.
- Every name shown in a diagram still exists in the code.

## 4. Export the PNGs

Render with the Excalidraw CLI through `npx`, with every cache in the
scratchpad so nothing stays on the machine:

```bash
T=<scratchpad>/npx-tmp
export npm_config_cache=$T/npm PLAYWRIGHT_BROWSERS_PATH=$T/pw \
       EXCALIDRAW_NO_UPDATE_NOTIFIER=1 npm_config_update_notifier=false
cd docs/diagram
npx --yes @excalidraw/cli@0.2.0 render 01-modules.excalidraw --out 01-modules.png
# same for each changed diagram
```

- Needs `node`. If it is missing, stop and ask: never install anything.
- Open each PNG and look at it: overlaps, cut text, crossed arrows.
- Afterwards: `rm -rf "$T"` and check that no process is left
  (`pgrep -fl 'chrom|playwright|excalidraw'`).

## 5. Hand over

- Do not commit: give a short summary per diagram (what changed and why)
  and let the user review the PNGs.
- If the README or another doc points to a diagram that changed, say so.

## Conventions

- **One color per package**, stroke / fill:
  - `core`: `#0ca678` / `#c3fae8`
  - `maze_generator`: `#4a9eed` / `#a5d8ff`
  - `maze_solver`: `#8b5cf6` / `#d0bfff`
  - `maze_render`: `#22c55e` / `#b2f2bb`
  - `config_parser`: `#f59e0b` / `#ffd8a8` (light `#fff3bf` for inputs and
    flowchart decisions)
  - `maze_app`: `#e64980` / `#fcc2d7`
  - `output_file`: `#1098ad` / `#99e9f2`
  - errors and exceptions: `#ef4444` / `#ffc9c9`
  - data, external libs, scripts, terminal: `#868e96` / `#f1f3f5`
- A new package with no color yet gets one: propose it during the audit.
- Step frames: same colors at 30 % opacity, label in a darker shade.
- Class box = colored header + white body (`#ffffff`) with the same stroke.
- Dashed stroke = grouping frame (a package, a pipeline step) or something
  external.
- Font `fontFamily: 5`, `roughness: 1`; title 28, labels 16–18, small notes 14.
- Each diagram starts with a title `a_maze_ing — <subject>` and a legend if
  the colors or arrows need one.
- Element ids are readable (`gen_h`, `gen_h_t`), not random.
- Every text in English, names copied exactly from the code.
