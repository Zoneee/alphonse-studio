---
name: write-story
description: "Write a Story document from the architecture perspective: how the system delivers the Feature, with AC, seams, and decisions. The Story is the contract between product and engineering."
disable-model-invocation: true
---

The Story document sits below the Feature and above the tickets. It is the architect's artifact: takes a slice of Feature value and describes how the system will deliver it — with enough precision that engineers can implement and test without re-asking, but without committing to code that will be outdated in a week.

Two voice boundaries this skill enforces; do not blur them:

- **Story** (capitalised) is the engineering-side contract this skill produces: architecture, seams, AC, decisions. It is read by implementers and reviewers.
- **user-story** (lowercase, hyphenated) is the product-side voice used in Features and ticket seeds: "As a <user>, I want <capability>, so that <value>". It belongs in the Feature; it does **not** belong in this document.

The two never substitute for each other: a `Story` AC must be testable from the outside (input → observable behaviour → outcome), and a `user-story` voice never carries the seam or decision detail that the engineering side needs.

## When to use

- A Feature (or a slice of one) is ready to enter engineering.
- A Story is large enough to span multiple tickets or PRs but small enough to be one Feature unit.
- An existing Story needs to be reshaped because the architecture has shifted.

If the Feature doesn't exist, stop and ask the user to run `write-feature` first. Don't invent scope.

## Inputs

- The Feature doc (Scope + Success criteria at minimum).
- Existing architecture: relevant ADRs, the module map, the seam conventions of this repo.
- Tech constraints (platforms, languages, runtime versions, infra boundaries).

Domain terms come from the repo's context file(s):

- **Single context** — if a `CONTEXT.md` exists at the repo root and no `CONTEXT-MAP.md`, use its glossary directly.
- **Multi context** — if a `CONTEXT-MAP.md` exists at the repo root, follow its pointers into the relevant sub-`CONTEXT.md` and use that glossary. Do not blend vocabularies across contexts.
- If neither exists, fall back to existing repo terms; surface any new term to the product / glossary owner before publishing.

If an ADR exists for the area, respect it; if the Story needs to break an ADR, surface that explicitly and link to the proposed new ADR.

## Output

Write the Story doc to `docs/features/<id>-feature-<slug>/story/<id>-story-<slug>.md`. Use the default layout in docs/knowledge-layering.md; if the current repo's <repo>-agents.md overrides it, follow that override. The parent Feature directory must already exist (run `write-feature` first if it doesn't). After writing, create or refresh the symlink `.scratch/<story-id>/story` → `docs/features/<id>-feature-<slug>/story/<id>-story-<slug>.md`.

## Body

```markdown
# <Story name>

## Origin
<One paragraph. Which Feature this Story serves and what slice of Feature value it delivers.>

## Acceptance criteria
<Numbered list. Each AC is testable from the outside: input → observable behaviour → outcome. Each AC has an id (AC-1, AC-2, …) so later review can cite it.>

## Seams
<Where the Story meets the rest of the system. Existing seams first; new ones only if the existing seam can't carry the new behaviour. For each seam: the boundary, the contract, and a one-line rationale.>

## Decisions
<Architecture decisions this Story makes or that bound it. Each: decision + one-paragraph rationale. Reference ADRs by id where they exist. Inline a small snippet (state machine, schema, type shape) only when prose can't carry the precision; trim to the decision-rich parts.>

## Risks
<What could go wrong. Operational, security, performance, compatibility, tech-debt. For each: probability (low / med / high) and impact (low / med / high).>

## Testing approach
<What kinds of tests apply: UT seams, IT paths, E2E journeys. What behaviour is too expensive to test in this Story and is deferred.>

## Out of scope
<What this Story deliberately does not cover, even if it sits inside the Feature scope.>

## Open questions
<Architectural questions still open. One sentence each.>
```

## What not to do

- Don't write implementation tasks or ticket bodies. Those come from `to-tickets`.
- Don't write code beyond the small decision-snippets justified above.
- Don't invent seams. If a new seam is needed, say so and explain why the existing one fails.
- Don't relitigate Feature scope. If the Story needs to expand or shrink scope, surface that to the product side first.

## After writing

- Each AC must be independently testable. If two ACs only make sense together, merge them.
- Hand the Story to engineering. The next step is `to-tickets`.
