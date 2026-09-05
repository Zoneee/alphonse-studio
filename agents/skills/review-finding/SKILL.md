---
name: review-finding
description: "Deep review that combines PR + CI + Story + Feature + Code. Asks two questions a code-only review misses: did the Story's acceptance criteria get met, and do they actually achieve the Feature's purpose? Outputs P0/P1/P2 findings, each pinned to file:line and the AC or Feature line it violates. Use when reviewing a branch, PR, or work-in-progress before merge."
---

Deep review that goes beyond "does the code follow standards". It cross-checks the change against the originating Story (acceptance criteria, scope) and the Feature (purpose, value) so it can surface findings a code-only review would miss: an AC silently dropped, a goal half-met, a CI failure on a changed path, a defect that defeats the Feature's purpose.

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

Drop findings that are stylistic-only, theoretical without a plausible failure path, or pre-existing in unchanged code (unless the change routes a new failure path through them).

Confidence tag accompanies severity:

- `high` — direct code evidence and clear failure path from the change.
- `medium` — strong evidence with one reasonable assumption.
- `low` — plausible concern that needs validation; place under `Needs verification`, not in P0/P1/P2.

## Process

### 1. Pin the diff and confirm sources

Capture once: `git diff <fixed-point>...HEAD --stat` and `git log <fixed-point>..HEAD --oneline`. Read the Story's AC list and the Feature's purpose / success criteria / out-of-scope sections. Note the AC ids (AC-1, AC-2, …) and the Feature line numbers so later findings can cite them.

### 2. Three parallel sub-agents

Run three sub-agents in parallel so they don't pollute each other's context. Cap to 3 parallel probes.

**AC-coverage sub-agent.** Inputs: Story AC list with ids, diff, file paths in the repo. Brief: "For each AC, report: (a) met — cite the file:line that proves it; (b) partial — what is missing; (c) not implemented. Do not judge quality, only coverage. Under 500 words."

**Feature-purpose sub-agent.** Inputs: Feature purpose / success criteria / out-of-scope lines, diff, Story. Brief: "Does the diff actually advance the Feature's purpose? Report: (a) gaps — work that leaves the Feature's success criteria unattainable; (b) drift — work that solves a problem the Feature does not have; (c) contradiction — work that pulls against an out-of-scope guardrail. Each finding: cite Feature line + diff hunk. Under 500 words."

**CI + defect sub-agent.** Inputs: CI status output, diff, full relevant files (read them, do not skim). Brief: "Report: (a) CI failures on changed paths and likely cause; (b) defects introduced by the change (security, correctness, reliability, data, breaking regression). Use the P0/P1/P2 rubric above. Each finding: severity + confidence + file:line + concrete impact + causal path. Do not report style. Under 500 words."

### 3. Aggregate

Stack the three sub-reports under `## AC coverage`, `## Feature purpose`, `## CI + defects`. Then merge every finding into a single ranked list:

```
[P0|high] file:line — short title
  Impact: what breaks, or which AC / Feature line is violated
  Evidence: AC-id or Feature-line + file:line
  Causal path: why the change creates this
```

Do not re-rank across sources. AC gaps, Feature drift, and CI / defects are different axes; each axis can carry its own worst finding.

End with a one-line summary:

```
P0: N | P1: N | P2: N | Needs verification: N | Outcome: Blocker | Non-blocking | No actionable findings
```

### What not to report

- Style, formatting, naming, preference-only comments.
- Theoretical defects without a plausible execution path.
- Pre-existing issues in unchanged code, unless the change routes a new failure through them.
- Praise-only notes.
- Findings already enforced by tooling (lint, type-check, formatter).

### Tooling

Do not run lint, type-check, or tests by default. Use targeted verification only when a P0 / P1 defect cannot be confirmed by reading alone.
