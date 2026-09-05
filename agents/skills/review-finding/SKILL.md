---
name: review-finding
description: "Deep review that combines PR + CI + Story + Feature + Code: checks whether the Story's AC are met and whether they actually achieve the Feature's purpose. Outputs P0/P1/P2 findings pinned to file:line and the violated AC or Feature line."
disable-model-invocation: true
---

Deep review that goes beyond "does the code follow standards". It cross-checks the change against the originating Story (acceptance criteria, scope) and the Feature (purpose, value) so it can surface findings a code-only review would miss: an AC silently dropped, a goal half-met, a CI failure on a changed path, a defect that defeats the Feature's purpose.

## When to use

Use when reviewing an unmerged change before merge: the change should already have a Story and (preferably) a Feature pointing at it.

Don't use when there is no Story or Feature to check against — a code-only review is `code-review`, not this skill. Don't use for post-merge archaeology or for live debugging — that's `diagnosing-bugs`.

## Inputs

The skill needs four things. If any is missing, ask the user to point to it; do not invent.

1. **Diff** — a fixed point (branch, commit, tag, merge-base). Use `git diff <fixed-point>...HEAD` (three-dot, against the merge-base). Confirm `git rev-parse <fixed-point>` resolves and the diff is non-empty before spawning sub-agents.
2. **Story** — the ticket / spec with the acceptance criteria list and scope statement.
3. **Feature** — the product-level document describing purpose, success criteria, and out-of-scope.
4. **CI results** — pipeline output already produced (passed / failed / skipped suites). Do not re-run CI.

Fallbacks: if the Feature is missing but a Story exists, run in Story-only mode and note the gap in the report. If both are missing, stop and ask.

## Severity rubric (P0 / P1 / P2)

Use the lowest level that still blocks the change's purpose.

- **P0 — must fix before merge.** Security vulnerability, data corruption or irreversible loss, crash / outage in a reachable path, AC violation that defeats the Feature's purpose, CI failure on a changed path.
- **P1 — should fix before merge.** User-visible defect in a common path, missing or wrong error handling causing request / job failure, concurrency or state bug with realistic reachability, partial AC coverage that leaves a Feature goal half-met, incomplete migration or contract change likely to break a consumer.
- **P2 — nice to have.** Edge-case correctness bug with narrow reachability, type or validation gap likely to fail at runtime, performance regression with concrete user or system impact, low-severity maintainability risk introduced by the change.

Confidence tag accompanies severity as an **independent** label, written as two brackets side by side:

- `[P0][high]` — direct code evidence and clear failure path from the change.
- `[P0][medium]` — strong evidence with one reasonable assumption.
- `[P0][low]` — plausible concern that needs validation; place under `Needs verification`, not in P0/P1/P2.

The `[severity]` and `[confidence]` tags are independent: severity says how badly the change is broken, confidence says how sure the reviewer is. Use this dual-tag form everywhere (in-line, in axes, in the summary count), so downstream tools can filter on either axis.

## Output

Write the report to a Markdown file at `.scratch/<story-id>/review/from-<reviewer>.md`. Use the default layout in docs/knowledge-layering.md; if the current repo's <repo>-agents.md overrides it, follow that override. Replace `<reviewer>` with the agent or human producing the review.

## Process

### 1. Pin the diff and confirm sources

Capture once: `git diff <fixed-point>...HEAD --stat` and `git log <fixed-point>..HEAD --oneline`. Read the Story's AC list and the Feature's purpose / success criteria / out-of-scope sections. Note the AC ids (AC-1, AC-2, …) and the Feature line numbers so later findings can cite them.

**Done when**: the fixed point resolves (`git rev-parse <fixed-point>` succeeds), the diff is non-empty, and three sub-agent tasks have been dispatched in step 2.

### 2. Three parallel sub-agents

Run three sub-agents in parallel so they don't pollute each other's context. Each sub-agent reports into exactly one axis and never crosses axes.

**AC-coverage sub-agent.** Inputs: Story AC list with ids, diff, file paths in the repo. Brief: "For each AC, report: (a) met — cite the file:line that proves it; (b) partial — what is missing; (c) not implemented. Do not judge quality, only coverage. Under 500 words." Reports into the `## AC coverage` axis.

**Feature-purpose sub-agent.** Inputs: Feature purpose / success criteria / out-of-scope lines, diff, Story. Brief: "Does the diff actually advance the Feature's purpose? Report: (a) gaps — work that leaves the Feature's success criteria unattainable; (b) drift — work that solves a problem the Feature does not have; (c) contradiction — work that pulls against an out-of-scope guardrail. Each finding: cite Feature line + diff hunk. Under 500 words." Reports into the `## Feature purpose` axis.

**CI + defect sub-agent.** Inputs: CI status output, diff, full relevant files (read them, do not skim). Brief: "Report: (a) CI failures on changed paths and likely cause; (b) defects introduced by the change (security, correctness, reliability, data, breaking regression). Use the P0/P1/P2 rubric above. Each finding: severity + confidence + file:line + concrete impact + causal path. Do not report style. Under 500 words." Reports into the `## CI + defects` axis.

If CI status is **missing or still running**, do not force the CI sub-agent to wait — skip its dispatch and mark the axis as `CI-pending` (see Aggregate below). If a sub-agent fails, returns an empty report, or exceeds the word budget, treat that axis as `Needs verification` rather than silently clean.

**Done when**: all three reports are present at the expected length, or the missing/running ones are explicitly marked `CI-pending` / `Needs verification` with the reason recorded.

### 3. Aggregate

Produce exactly three axis sections — `## AC coverage`, `## Feature purpose`, `## CI + defects` — and rank findings **within each axis only**. Do not re-rank across axes: an AC-coverage P0 is not "worse than" a CI P0; each axis carries its own worst finding.

Each axis section follows the same shape:

```
## <Axis name>
- [P0][high] file:line — short title
    Impact: what breaks, or which AC / Feature line is violated
    Evidence: AC-id or Feature-line + file:line
    Causal path: why the change creates this
- [P1][medium] file:line — short title
    ...
```

When a sub-agent failed, returned an empty report, or blew the word budget, lift any partial finding it produced out of the axis and into a `## Needs verification` section at the end of the report. A missing sub-agent report is never "no findings" — it is "findings unknown until the source is re-run".

When CI status is missing or still running, replace the `## CI + defects` axis with:

```
## CI + defects
CI-pending: <reason — e.g. "pipeline id 12345 still running", "no CI configured for this branch">
No CI findings can be reported. Re-run review-finding after CI settles.
```

and place that whole axis block under `## Needs verification`. Do not infer "CI is green because it is quiet"; quiet is `CI-pending`, not pass.

End with a one-line summary:

```
P0: N | P1: N | P2: N | Needs verification: N | Outcome: Blocker | Non-blocking | No actionable findings
```

**Done when**: the three axis sections `## AC coverage`, `## Feature purpose`, `## CI + defects` are written with within-axis ranking, any sub-agent failure or missing report has been lifted into `## Needs verification`, any `CI-pending` axis sits under `## Needs verification`, and the one-line summary is the last line of the report.

### What not to report

- Style, formatting, naming, preference-only comments.
- Theoretical defects without a plausible execution path.
- Pre-existing issues in unchanged code, unless the change routes a new failure through them.
- Praise-only notes.
- Findings already enforced by tooling (lint, type-check, formatter).

### Tooling

Do not run lint, type-check, or tests by default. Use targeted verification only when a P0 / P1 defect cannot be confirmed by reading alone.
