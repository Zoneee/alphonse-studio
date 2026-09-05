---
name: show-me
description: "Pre-code preview that turns a Story / spec / review context into a clear plan: current state, problem, goal, reason, gap, and a how-to with pseudocode or UML. Solves 'I shipped code I can't vouch for'."
disable-model-invocation: true
---

Pre-code gate that forces explicit answers to five questions that vibe-coding skips:

1. **Current state** — what exists today, in the relevant code area.
2. **Problem** — what's wrong or missing, in concrete terms.
3. **Goal** — what success looks like after this change, in observable behaviour.
4. **Reason** — why this is worth doing now, and what happens if we don't.
5. **Gap** — the delta between current state and goal, narrowed to what this PR fills.

After the five answers, the **how** sketches pseudocode or UML enough to make the implementation direction unambiguous, plus the decision rationale (why this shape and not another).

The five-question gate exists because review-after-the-fact catches too late: by then the wrong shape is cemented in code.

## When to use

Use before starting any non-trivial implementation, when an input (Story, spec, review finding, or free-form problem statement) is concrete enough to plan against.

Don't use for one-line fixes — trivial changes don't need a plan. Don't use to draft code: the show-me is the plan, the implementer writes the code.

## Inputs

Accept any of:

- A Story (preferred — already has AC, seams, decisions).
- A spec or Feature doc.
- The output of `review-what` (when fixing review findings).
- A triage or group output from a parent skill.
- A free-form problem statement (last resort — the show-me will be shallower).

The richer the input, the more concrete the output. If all you have is a problem statement, ask for the Story first; don't fake the depth.

## Output

Write to a single Markdown file at `.scratch/<story-id>/show-me/<story-id>.md`. Use the default layout in docs/knowledge-layering.md; if the current repo's <repo>-agents.md overrides it, follow that override. If `.scratch/<story-id>/` does not exist yet, create it under the current story slug. Structure:

```markdown
# <Story or task name>

## Current state
<What exists today. Cite file:line for the relevant modules / functions / types. If you don't know, write "unexplored" and stop — don't guess.>

## Problem
<What's wrong or missing. In observable behaviour, not "the code is ugly". If the input was a review finding, quote the finding.>

## Goal
<What success looks like. Tied to AC ids when the input has them.>

## Reason
<Why now. What value unlocks, what risk stays if we don't. One short paragraph.>

## Gap
<The delta. Specifically what this PR / change fills, and what it deliberately leaves for follow-ups.>

## How
<Pseudocode or UML. Pick the form that makes the change unambiguous:
- state machine for behaviour changes
- sequence diagram for cross-component flows
- data-flow diagram for transformations
- AST-shaped pseudocode for parser / compiler work
- one or two annotated snippets for surgical fixes
If the implementation is so direct that pseudocode would just be the code, write "no sketch needed — direct implementation" and skip.>

## Decisions
<Each decision: choice + one-paragraph rationale + what was rejected and why. Keep it short. Link the Story's Decisions section if one exists.>

## Risks
<Operational, security, performance, compatibility, tech-debt. Probability × impact. One line each.>

## Out of scope
<What this change does NOT do, even if the Story mentions it.>
```

## Process

### 1. Read the input once end to end

Don't draft on the first sentence. Read the full input, the relevant code, and any linked ADRs before writing.

### 2. Answer the five questions in order

If you can't fill one of them concretely, stop. Either the input is thin (ask the user for more), or the change isn't ready to plan.

### 3. Sketch the how

Pseudocode or UML, not real code. The point is to fix the shape, not the syntax. State machines beat prose for behaviour; sequence diagrams beat prose for cross-component flows; data-flow beats prose for transformations.

### 4. Note the decisions

Each non-obvious choice gets one paragraph. The "what was rejected" half is what makes the decision useful — without it, the next reviewer asks the same question.

### 5. Hand off

After writing the file, print the path and the one-paragraph summary. The implementer reads the file, not the chat. Don't paste the full content into the chat unless the user asks.

## What not to do

- Don't write code in the show-me. The show-me is the plan; the implementer writes the code.
- Don't skip the "what was rejected" half of decisions. A decision without a rejected alternative is just a preference.
- Don't include findings from review-finding without re-checking them. The review may be stale by the time the show-me is written.
