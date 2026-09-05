---
name: review-what
description: "Triage the output of review-finding. For each finding, decide fix-here / fix-next / skip (with reason) / needs-human. Justify each verdict with the violated AC, Feature line, or contradicting code line. Use after review-finding, before opening fix branches."
---

Triages the ranked finding list from `review-finding` (or any review source). Goal: a defensible verdict per finding — what gets fixed in this PR, what gets deferred, what gets rejected, and why.

The skill exists because raw review output mixes real defects with noise, and shipping every finding as a must-fix bloats the PR until nobody can review it. The agent's job here is to separate signal from load.

## Inputs

- **Finding list** — P0 / P1 / P2 with `file:line`, evidence, causal path.
- **Story AC** — so verdicts can cite AC ids when a finding is real.
- **Feature purpose / out-of-scope** — so verdicts can cite Feature lines when a finding is out of scope.
- **Scope boundary** — what this PR is and is not trying to do. If unclear, ask before triaging.

## Verdict vocabulary

For each finding, exactly one of:

- **fix-here** — fix in the current PR. Justify by citing the violated AC, the Feature line, or a safety boundary (security, data integrity, CI red).
- **fix-next** — same defect, but out of current PR scope. Open a follow-up ticket seed; reference the AC or Feature line so the next PR inherits the context.
- **skip-false-positive** — the reviewer's causal path doesn't hold. Quote the contradicting `file:line` so the rejection is checkable.
- **skip-out-of-scope** — the change was never meant to address this. Cite the Feature's out-of-scope guardrail or the Story's scope statement.
- **skip-over-design** — the proposed fix adds complexity the Feature doesn't need. Show the YAGNI argument or cite an ADR that says the simpler shape is the right one.
- **needs-human** — verdict requires a product / architecture call the agent can't make. Phrase the question so the human can answer in one sentence.

Avoid vague verdicts. Every row carries an evidence-backed reason. "Looks fine" is not a verdict.

## Output

Write the triage report to a Markdown file. Default path: `.scratch/<story-id>/review/from-<reviewer>-comment.md` (per the shared `.scratch/<story-id>/` layout in AGENTS.md). `<reviewer>` matches the matching `review-finding` output's reviewer slug. If the repo's `<repo>-agents.md` overrides the layout, follow the override.

## Process

### 1. Read the finding list end to end

Before triaging row by row, read every finding. Some P2s collapse into one fix; some P1s dissolve under cross-evidence. Don't verdict in isolation.

### 2. Walk the decision tree per finding

For each finding, in order:

1. Does the cited AC / Feature line apply to this PR? — If no → `skip-out-of-scope` with the line.
2. Does the cited `file:line` actually behave the way the reviewer claims? — Read it. If the causal path fails → `skip-false-positive` with the contradicting line.
3. If both hold: is the fix within current PR scope? — Yes → `fix-here`. No → `fix-next` with a one-line ticket seed.
4. If the fix requires new design choices the spec doesn't make → `needs-human`. Phrase the question precisely.
5. If the finding is real but the proposed fix adds an abstraction or parameter the spec doesn't ask for → `skip-over-design` and propose inlining or deferring.

### 3. Cross-check scope

After verdicts, walk the `fix-here` list once. If together they push the PR past its scope (more than ~30% size delta, or they pull in a new module or migration), promote the lowest-priority ones to `fix-next`. Scope discipline beats completeness in a single PR.

### 4. Output

A list per finding:

```
[verdict] [P?] file:line — short title
  Reason: AC-id-or-Feature-line / contradicting file:line / scope note
  Action: commit-message seed, ticket seed, or one-sentence question for human
```

End the report with:

- Counts: `fix-here: N | fix-next: N | skip: N | needs-human: N`.
- If `needs-human > 0`: the exact questions, one sentence each, ready to paste to the human.
- If `fix-here` is empty and there are no `needs-human`: state `No changes required from review-finding`.
- A `Ticket seeds` block with one bullet per `fix-next` finding, each a single sentence ready to become a ticket title.

### What not to do

- Don't reopen the review. If a finding's evidence is wrong, mark `skip-false-positive` and move on; don't try to repair the reviewer's argument.
- Don't argue with `needs-human`. Surface the question and wait.
- Don't merge multiple `fix-here` items into one commit unless they share a module and a root cause; mixed-cause commits are harder to revert.
