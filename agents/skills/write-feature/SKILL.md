---
name: write-feature
description: "Write a Feature document from the product perspective: who needs it, why, what success looks like, what's out. The Feature answers 'why this exists' and 'what value unlocks when it's done'."
disable-model-invocation: true
---

The Feature document sits above the Story and below the product strategy. It is the product manager's artifact: framed in user value, scope, and success — not implementation.

## When to use

- A new product capability is being scoped for the first time.
- An existing capability has drifted and needs re-anchoring against its original purpose.
- A cross-team initiative needs a shared product view before any Story is written.

If the user can't articulate the affected user and the observable pain, stop and ask them to. Don't invent a problem statement.

## Inputs

- The problem or opportunity that triggered the Feature (customer signal, metric, strategy bet, or a user-quoted pain).
- The user segments affected. Use existing personas if the repo has them; don't invent new ones.
- Existing Features this one composes with, replaces, or extends.

Domain terms come from the repo's context file(s):

- **Single context** — if a `CONTEXT.md` exists at the repo root and no `CONTEXT-MAP.md`, use its glossary directly.
- **Multi context** — if a `CONTEXT-MAP.md` exists at the repo root, follow its pointers into the relevant sub-`CONTEXT.md` and use that glossary. Do not blend vocabularies across contexts.
- If neither exists, fall back to existing repo terms; surface any new term to the product / glossary owner before publishing.

## Output

Write the Feature doc to `docs/features/<id>-feature-<slug>/<id>-feature-<slug>.md`. Use the default layout in docs/knowledge-layering.md; if the current repo's <repo>-agents.md overrides it, follow that override. `<id>` is a numeric ticket / feature id; `<slug>` is kebab-case. Create the parent directory if it does not exist.

## Body

```markdown
# <Feature name>

## Problem
<2–4 sentences, each verifiable and naming the affected user and the observable pain, written from the user's perspective.>

## Who
<User segments affected, each with the job-to-be-done they are trying to do. Reference existing personas if the repo has them.>

## Value
<What changes for the user when this Feature exists. What metric moves, what becomes possible that wasn't?>

## Success criteria
<3–7 measurable outcomes. Each testable from the user's side: a metric, a threshold, an observable behaviour. Avoid implementation language.>

## Scope
<What this Feature covers. Concrete enough that a Story writer can decide what is in and what is out without re-asking the product side.>

## Out of scope
<Explicit non-goals. Future ideas that look related but are deferred.>

## Open questions
<Anything the product side needs answered before Stories can be written. One sentence per question.>

## Dependencies
<Other Features, platforms, or external systems this Feature requires.>
```

## What not to do

- Don't write implementation decisions. Those belong in the Story.
- Don't write acceptance criteria. Those belong in the Story.
- Don't write code or file paths. The Feature outlives the codebase.
- Don't write tasks or tickets. The Story does that.
- Don't write technical risk. The Story covers that with architecture context.

## After writing

- If a `CONTEXT.md` or glossary exists, verify every term in the Feature appears in it. If a term is new, propose it to the glossary owner before publishing.
- Hand the Feature to the architecture side. The next step is `write-story`.
