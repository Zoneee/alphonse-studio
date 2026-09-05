---
name: high-quality-tests
description: "Reviewer for existing UT and IT. Catches tests that don't actually test behaviour — string-contains checks, weak assertions, mock-the-SUT patterns, false greens. Outputs a ranked list of test smells with file:line and a concrete fix suggestion. Use when a test suite has grown or feels untrustworthy, or after vibe-coding produced tests that pass without proving anything."
---

Reviews an existing test suite for quality, not coverage. Coverage tells you what lines ran; this skill tells you whether running them would catch a real bug.

The trigger is the pattern the user has actually hit: tests that pass while the code is broken. A test that checks "does this static file contain the string `TODO`" passes whether the feature works or not. A test that asserts `result is not None` passes whether `result` is correct or nonsense. This skill finds those and ranks them.

## Inputs

- **Test files** — UT and IT. Path glob the user gives, or `**/*.test.*` / `**/*_test.*` / `**/test_*.py` as a default.
- **Modules under test** — read them so the reviewer can sanity-check the assertions against the real behaviour.
- **Story AC list** (optional) — to verify AC-by-AC coverage at the end.

If no paths are given and the repo has no clear test convention, stop and ask.

## Severity rubric

- **P0 — false green.** Test passes with broken code. Highest priority: these are lies. Examples: `assert mock.called` on a misconfigured mock; `assert result is not None` on a function that always returns an object; string-contains on a file the test itself wrote.
- **P1 — tests implementation, not behaviour.** Test will break on any benign refactor and gives no signal about correctness. Examples: asserting internal field values; asserting call order when order is unspecified; reaching into private state; mocking the system under test.
- **P2 — weak but not broken.** Assertion is too soft to catch a real regression. Examples: `assert x > 0` instead of `assert x == expected`; only happy path; no boundary cases; missing negative cases.

Use these sparingly. If every test is P2, the suite is uniformly weak and the report should say so in the summary rather than list every test.

## Process

### 1. List tests and group by feature

Walk the test files. Group by unit-under-test, not by file path. One summary row per group, then a row per finding.

### 2. Mental-debug each test

For each test, walk the four mental-debug questions. If the answer to any is "no, the test wouldn't catch it", that's a finding.

1. **Remove core logic.** If the main function body were deleted or short-circuited, would this test fail? If no → P0 false green.
2. **Return wrong values.** If the function returned plausible-but-wrong values (off-by-one, swapped fields, wrong constant), would assertions catch it? If no → P2 weak assertion.
3. **Skip validation.** If input validation were removed, would the test feed invalid data and notice? If no → missing negative case.
4. **Break error handling.** If errors were silently swallowed, would the test observe the failure? If no → not testing the failure path.

### 3. Classify the smell

Match the finding to a category:

- **string-contains-on-artifact** — `expect(fs.readFileSync(path)).toContain('foo')`. Reads a file the test itself produced, or a string that could be anywhere. No behaviour is verified.
- **mock-the-SUT** — the system under test is itself mocked, so the test exercises only the mock.
- **existence-only-assertion** — `assert x is not None`, `expect(x).toBeDefined()`, `assert mock.called`. Catches nothing.
- **impl-detail-assertion** — testing private fields, call order, internal logs.
- **always-true-assertion** — `assert True`, tautology, or asserting a value the function just computed without independent verification.
- **no-negative-case** — only happy path. No error / boundary / invalid input.
- **brittle-fixture** — setup reflects no realistic scenario; would never trigger the bug it's meant to catch.
- **snapshot-everything** — `toMatchSnapshot()` covering large blobs; any change trips it; no human ever reads the diff.

### 4. For each finding, propose a concrete fix

Don't just label. Say what the assertion should check, or what test should be added, or what should be deleted.

## Output

```markdown
## <Group name>

**Coverage:** <N tests; happy-path-only | has-negatives | mixed>
**Verdict:** trustworthy | mixed | untrustworthy

### [P0|P1|P2] file:test:line — short title
**Smell:** <category from step 3>
**Impact:** <what bug slips through>
**Fix:** <one-paragraph concrete change — what to assert, what to add, what to delete>
```

End the report with:

```
## Summary
- P0 (false green): N
- P1 (impl-detail): N
- P2 (weak): N
- Verdict: trustworthy | mixed | untrustworthy
- Top fix: <one-line highest-leverage change>
```

If `Story AC` was supplied, append:

```
## AC coverage
- AC-1: covered with evidence | partial | missing
- AC-2: ...
```

## What not to do

- Don't run the tests to "see if they pass". Passing is the false-green trap — many bad tests pass.
- Don't suggest adding more assertions blindly. Add ones that catch a specific class of bug.
- Don't recommend coverage tooling as a fix. Coverage is a lagging indicator; assertion strength is the leading one.
- Don't rewrite the suite. Report and let the human or implementer decide.
- Don't flag stylistic preferences (naming, formatting, fixture organization). That's a separate review.
