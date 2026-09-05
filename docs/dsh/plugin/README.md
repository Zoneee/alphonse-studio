# DSH plugins — central management

This directory documents the DSH plugin layer managed by `alphonse-studio`.

## Scope

`alphonse-studio` is the **source of truth** for two parallel extension
mechanisms of DeepSeek Harness:

1. **Skills** — markdown prompt packs DSH loads from disk.
   Path: `agents/skills/` (symlinked to `~/.agents`).
2. **Plugins** — Node packages registered into a DSH profile.
   Path: install recipes under `agents/dsh/plugin/`; plugin code itself
   lives in the user's profile (e.g. `~/.dsh/profiles/web/node_modules/`).

This directory covers the second mechanism only.

## Convention

* One Python script per plugin under `agents/dsh/plugin/<name>.py`.
* Each script exposes four subcommands:
  * `install` — adds the plugin to a DSH profile (the only mutating command).
  * `uninstall` — removes it.
  * `status` — reports install state without changing anything.
  * `verify` — filesystem-only check, no DSH state mutation.
* Default profile is `web`. Override with `--profile <name>`.
* Install source defaults to a GitHub ref (e.g. `github:owner/repo`),
  pinned by tag for reproducible installs.
* Plugin node_modules are **not** vendored into this repo — `pnpm install`
  resolves them at install time, same as a normal Node project.
* Plugin profiles (`~/.dsh/profiles/<name>/`) are machine-local and stay
  out of git. Only the recipe to install them lives here.

## Layout

| Path | Purpose | Tracked? |
|---|---|---|
| `agents/dsh/plugin/<name>.py` | install / uninstall recipe | yes |
| `docs/dsh/plugin/<name>.md` | per-plugin notes | yes |
| `docs/dsh/plugin/README.md` | this index | yes |
| `~/.dsh/profiles/<name>/package.json` | profile manifest | no |
| `~/.dsh/profiles/<name>/node_modules/` | installed plugins | no |

## Adding a new plugin

1. Pick a `<name>` (kebab-case, matches the npm/GitHub name's tail).
2. Write `agents/dsh/plugin/<name>.py` mirroring the ponytail script:
   constants, `_check_dsh`, `_run`, `_plugin_dir`, four `cmd_*` handlers,
   `main` with `argparse` and subparser dispatch.
3. Write `docs/dsh/plugin/<name>.md` with: source, install source,
   restart note, verify commands.
4. Add the plugin to this README under [Plugins](#plugins).
5. Commit both files in one commit.

## Plugins

| Name | Script | Notes | Status |
|---|---|---|---|
| [ponytail](./ponytail.md) | `agents/dsh/plugin/ponytail.py` | lazy-mode coding prompt pack, 6 skills | installed (profile `web`) |

## Why two extension mechanisms, not one

Skills are markdown files; they live in git and travel with the repo via
a symlink. Plugins are Node packages with native deps and build steps;
they cannot be vendored as text. The two share a name and an agent-facing
role (both teach the model what to do), but their install and update
paths are different. Treating them as separate "extension kinds" with
their own source-of-truth layout keeps each one simple.