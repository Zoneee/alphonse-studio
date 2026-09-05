---
name: review-what
description: "Triage the output of review-finding. For each finding, assigns one verdict (fix-here / fix-next / skip-* / needs-human), each backed by the violated AC, Feature line, or contradicting code line."
disable-model-invocation: true
---

Triages the ranked finding list from `review-finding` (or any review source). Goal: a defensible verdict per finding — what gets fixed in this PR, what gets deferred, what gets rejected, and why.

The skill exists because raw review output mixes real defects with noise, and shipping every finding as a must-fix bloats the PR until nobody can review it. The agent's job here is to separate signal from load.

## When to use

Use after `review-finding` produces a ranked list, before opening any fix branch.

Don't use to redo the review — if a finding's evidence is wrong, the right verdict is `skip-false-positive`, not a new investigation. Don't use before `review-finding` has run; triage without a finding list is just guessing.

## Inputs

- **Finding list** — P0 / P1 / P2 with `file:line`, evidence, causal path.
- **Story AC** — so verdicts can cite AC ids when a finding is real.
- **Feature purpose / out-of-scope** — so verdicts can cite Feature lines when a finding is out of scope.
- **Scope boundary** — what this PR is and is not trying to do. If unclear, ask before triaging.

## Verdict vocabulary

For each finding, exactly one of:

- **fix-here** — fix in the current PR. Justify by citing the violated AC, the Feature line, or a safety boundary (security, data integrity, CI red).
- **fix-next** — same defect, but out of current PR scope. Seed a follow-up ticket in the `Ticket seeds` block of the output; reference the AC or Feature line so the next PR inherits the context.
- **skip-false-positive** — the reviewer's causal path doesn't hold. Quote the contradicting `file:line` so the rejection is checkable.
- **skip-out-of-scope** — the change was never meant to address this. Cite the Feature's out-of-scope guardrail or the Story's scope statement.
- **skip-over-design** — the proposed fix adds complexity the Feature doesn't need. Show the YAGNI argument or cite an ADR that says the simpler shape is the right one.
- **needs-human** — verdict requires a product / architecture call the agent can't make. Phrase the question so the human can answer in one sentence.

Avoid vague verdicts. Every row carries an evidence-backed reason. "Looks fine" is not a verdict.

## Output

Write the triage report to a Markdown file. 按 `docs/knowledge-layering.md` 默认布局写入 `.scratch/<story-id>/review/from-<reviewer>-comment.md`；若当前 repo 的 `<repo>-agents.md` 覆盖了布局，则遵循覆盖。`<reviewer>` matches the matching `review-finding` output's reviewer slug.

## Process

### 1. Read the finding list end to end

Before triaging row by row, read every finding. Some P2s collapse into one fix; some P1s dissolve under cross-evidence. Don't verdict in isolation.

Before any per-finding verdict, run a pass that produces a merge / dissolution list:

- **Merge candidates** — findings that share a root cause or sit in the same module and would be fixed by a single commit. Group them; one verdict covers the group.
- **Dissolution candidates** — findings whose premise is invalidated by another finding or by code evidence in the repo. A P1 that is fully covered by a high-confidence P0 from the same review drops; cite the covering finding.

The merge / dissolution list is a precondition for step 2, not a side product of it: verdicts must reference a stable reading of the whole list, not a row-by-row improvisation that misses bulk-handling opportunities.

**Done when**: every finding has been classified into one of {merge candidate, dissolved, neither}, the merge groups and the dissolution pairs are written down, and that classification is referenced before the first verdict is assigned.

### 2. Walk the decision tree per finding

For each finding, in order:

1. Does the cited AC / Feature line apply to this PR? — If no → `skip-out-of-scope` with the line.
2. Does the cited `file:line` actually behave the way the reviewer claims? — Read it. If the causal path fails → `skip-false-positive` with the contradicting line.
3. If both hold: is the fix within current PR scope? — Yes → `fix-here`. No → `fix-next` with a one-line ticket seed.
4. If the fix requires new design choices the spec doesn't make → `needs-human`. Phrase the question precisely.
5. If the finding is real but the proposed fix adds an abstraction or parameter the spec doesn't ask for → `skip-over-design` and propose inlining or deferring.

Apply the merge / dissolution list from step 1 before assigning a verdict to a row that was grouped or covered. Verdict vocabulary stays the same set as above; no new verdict words.

### 3. Cross-check scope

After verdicts, walk the `fix-here` list once. If together they push the PR past its scope (more than ~30% size delta, or they pull in a new module or migration), promote the lowest-priority ones to `fix-next`. Scope discipline beats completeness in a single PR.

### 4. Output

A list per finding:

```
[verdict] [P?][confidence] file:line — short title
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
