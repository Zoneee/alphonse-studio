# ponytail — lazy-mode prompt pack for coding tasks

## What it is

`ponytail` is a prompt pack that makes a DSH coding agent follow a
seven-rung "do less" ladder:

1. Does this need to exist at all? (YAGNI)
2. Already in this codebase? (reuse)
3. Stdlib does it?
4. Native platform feature covers it?
5. Already-installed dependency solves it?
6. Can it be one line?
7. Only then: the minimum code that works.

The DSH adapter ([`MengYuil/dsh-ponytail`](https://github.com/MengYuil/dsh-ponytail))
ports the upstream concept ([`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail))
into DSH's runtime and exposes **6 skills**:

| Skill | Trigger | Role |
|---|---|---|
| `ponytail` | (always-on) | ruleset injected into the system prompt; not user-invocable |
| `ponytail-review` | `/ponytail-review` | one-shot diff review for over-engineering |
| `ponytail-audit` | `/ponytail-audit` | whole-repo over-engineering audit |
| `ponytail-debt` | `/ponytail-debt` | harvest `ponytail:` comment ledger |
| `ponytail-gain` | `/ponytail-gain` | upstream benchmark reference scoreboard |
| `ponytail-help` | `/ponytail-help` | quick-reference card |

## Source

* **npm**: `@mengyuly/dsh-ponytail`
* **GitHub**: `github:MengYuil/dsh-ponytail`
* **Upstream concept**: `github:DietrichGebert/ponytail` (different repo — the original prompt)
* **Author note on adaptation**: the DSH adapter is a separate effort;
  upstream benchmark numbers do not transfer one-to-one.

## Install

The default install source is the GitHub ref, which lets `pnpm` resolve
the latest tagged release:

```bash
python3 agents/dsh/plugin/ponytail.py install
```

For a pinned version, override `--source`:

```bash
python3 agents/dsh/plugin/ponytail.py install --source github:MengYuil/dsh-ponytail#v0.3.2
```

For a non-default profile:

```bash
python3 agents/dsh/plugin/ponytail.py --profile tui install
```

After install, **restart the profile** (`dsh web` / `dsh tui`) so the
cordis runtime picks up the new bundles.

## Verify

Filesystem-only check, no DSH state mutation:

```bash
python3 agents/dsh/plugin/ponytail.py verify
```

This confirms:

* `~/.dsh/profiles/<profile>/node_modules/@mengyuly/dsh-ponytail/` exists.
* Required files present: `lib/index.js`, `lib/invariant.js`, `package.json`, `cordis.patch.yml`.
* The plugin name is declared in the profile's `package.json`.

## Status

```bash
python3 agents/dsh/plugin/ponytail.py status
```

Reports whether the directory and manifest entry exist. Does not change
anything.

## Uninstall

```bash
python3 agents/dsh/plugin/ponytail.py uninstall
```

After uninstall, restart the profile to unload the skills.

## What lands where

| Path | Owned by | Tracked in git? |
|---|---|---|
| `agents/dsh/plugin/ponytail.py` | this repo | yes |
| `~/.dsh/profiles/<p>/package.json` | DSH profile | no |
| `~/.dsh/profiles/<p>/node_modules/@mengyuly/dsh-ponytail/` | DSH profile | no |
| `~/.dsh/profiles/<p>/pnpm-lock.yaml` | DSH profile | no |

The recipe is the only artifact this repo keeps. The plugin itself
flows through DSH's normal `pnpm install` path, identical to any Node
dependency.

## Restart reminders

Installing or uninstalling ponytail **does not** hot-reload DSH. The
new skill set is picked up only after the profile restarts:

* `web` profile → restart `dsh web`
* `tui` profile → restart `dsh tui`

## Known caveats

* The DSH adapter's own README notes the tested DSH commit is `b150a551`
  (a pre-release checkout). Future DSH upgrades may require a new
  adapter release. `verify` catches file presence but not runtime
  compatibility — watch for skill-loading failures on first restart.
* The 6 skills are registered in-process by `ctx.skills.register()`. They
  do **not** appear under `~/.agents/skills/`. Use `verify` and the
  DSH web UI to confirm registration.
* The upstream prompt is authored for any coding agent. The DSH
  adapter's `ponytail-audit` / `ponytail-debt` one-shots are model-
  and tool-dependent; treat them as guidance, not authoritative
  verdicts.