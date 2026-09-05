---
name: write-common
description: "Write developer-facing documents from the implementation perspective: how to use, run, debug, extend, or integrate the system. The Common layer is the engineer's reference that lives at the code, not the architecture. Use when an API, module, or workflow needs a doc that ages with the code, not above it."
---

The Common document is the developer's reference. It sits beside the code: API references, integration guides, troubleshooting recipes, internal how-tos, runbooks. Where the Feature answers "why" and the Story answers "what", the Common answers "how".

## When to use

- A public API or module needs a developer-facing reference.
- A non-obvious workflow needs a runbook (debug, recovery, deployment).
- A cross-cutting convention (logging, errors, config, retry) needs a single source of truth.
- A new contributor needs a path through the repo's setup.

If the doc is about a decision or trade-off, that belongs in an ADR via `domain-modeling`, not here. If the doc is about user value or scope, that belongs in the Feature. If the doc is about how a Story will be built, that belongs in the Story.

## Inputs

- The code, module, or workflow being documented. Read it before writing. Don't write from imagination.
- The audience: external integrators, new contributors, on-call engineers, future-self.
- Existing conventions: where do READMEs live? What format do API refs use? Is there a `docs/` index?

If `CONTEXT.md` exists, use its glossary. If `CONTEXT-MAP.md` exists and points to multiple CONTEXTs, follow the one that covers this area.

## Output

Default placement, by doc shape:

- **API / module reference** → `<module>/README.md` if the module has a directory, else `docs/<area>/<module>.md`.
- **Runbook** → `docs/runbooks/<scenario>.md` (matches the shared `<repo>/docs/runbooks/` slot in `alphonse-studio/docs/knowledge-layering.md`).
- **Internal how-to / convention** → `docs/<area>/<topic>.md`.

Follow the repo's existing placement convention if it differs. If the repo's `<repo>-agents.md` overrides the layout, follow the override.

## Body shapes

Pick the shape that matches the audience. Don't force every doc into one template.

### API / module reference

```markdown
# <Module or API name>

## Purpose
<One paragraph. What this is for, who uses it, when not to use it.>

## Quick start
<Minimal copy-pasteable example. End-to-end: import, call, observe result.>

## Reference
<Signature, parameters, return shape. Each param: type, required, default, meaning.>

## Behaviour
<Side effects, ordering guarantees, error shapes, idempotency, thread-safety.>

## Failure modes
<What goes wrong, what the caller sees, how to recover.>

## Examples
<One per common usage pattern.>
```

### Runbook

```markdown
# <Runbook name>

## When to use this
<Symptom or trigger that brought you here.>

## Pre-flight
<What to confirm before acting.>

## Steps
<Numbered. Each step: command, expected output, what to do if output differs.>

## Rollback
<How to undo.>

## Escalation
<Whom to page, what context to hand off.>
```

### Internal how-to / convention

```markdown
# <Topic>

## Why this exists
<One paragraph. The problem this convention solves.>

## The rule
<The single rule, stated plainly.>

## Examples
<Good vs bad, with code.>

## Exceptions
<When the rule doesn't apply and what to do instead.>
```

## What not to do

- Don't duplicate the Story or Feature. Link to them; don't restate.
- Don't write prose that ages out fast — line numbers, exact file paths to internal modules, screenshots of UI that will move. Reference symbols and module names instead.
- Don't write tutorial-style "first we'll, then we'll" walkthroughs unless the audience is genuinely new. Walkthroughs rot faster than reference docs.
- Don't document private internals. If it's not part of the module's contract, it doesn't belong in the Common layer.

## After writing

- Verify every code snippet compiles / runs in isolation.
- Place the doc where the repo expects it (often `<module>/README.md`, `docs/<area>/`, or the repo root for top-level guides).
