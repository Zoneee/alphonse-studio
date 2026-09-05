---
name: write-pr
description: "Open and ship a pull request after review-what is settled: push the branch, fill the body from the change + Story + review findings, post the PR comment, and stop before merge."
disable-model-invocation: true
---

Ships a PR once the implementation is finished, `review-what` has triaged findings, and all `fix-here` items are committed. Drafts and executes. Does not author code.

## When to use

Use after `review-what` has produced a verdict list and all `fix-here` items are committed on the implementation branch.

Don't use before `review-what` has run — opening a PR against un-triaged findings invites drive-by comments that re-litigate the triage. Don't use to author code; that's `implement` / `tdd`.

## Pre-flight

Before opening the PR, verify all five. If any fails, stop and tell the user; do not auto-fix.

1. Working tree is clean (`git status --porcelain` is empty).
2. **Branch convention read** — read the current repo's `AGENTS.md` (or `<repo>-agents.md` symlink target) for the branch naming convention. If the file does not exist, or exists but does not name a branch convention, stop and ask the user instead of guessing.
3. Current branch is the implementation branch for the Story (matches the convention read in step 2).
4. **Base branch fetch** — `git fetch origin <base>` succeeds and `git rev-parse origin/<base>` resolves to a commit. **Done when**: `git rev-parse origin/<base>` returns a commit SHA; if fetch fails or the remote ref is missing, stop and surface the failure, do not proceed to PR creation on an unresolved base.
5. `.github/pull_request_template.md` (or the repo's equivalent) exists. If not, fall back to the body shape below.

## Inputs

- **Story** — ticket id, title, AC list. Source: the ticket system or the Story doc.
- **Commits** — `git log <base>..HEAD --oneline`.
- **Diff stat** — `git diff <base>...HEAD --stat` for the summary.
- **Test plan results** — what was run (UT, IT, lint, type-check, build) and the one-line outcome for each.
- **Risk notes** — anything that fits the Risk section of the repo's PR template.
- **Reviewer handles** — from CODEOWNERS if it exists, otherwise leave to the user.
- **`review-what` output** — so unresolved `needs-human` items can be surfaced on the PR thread.

## Output

The final artifact is the PR on the host (e.g. GitHub). Before pushing, also stage a Markdown draft. 按 `docs/knowledge-layering.md` 默认布局写入 `.scratch/<story-id>/pr/draft.md`；若当前 repo 的 `<repo>-agents.md` 覆盖了布局，则遵循覆盖。so the body is reviewable in the working tree.

## Body shape

### If a template exists

Fill every required section of `.github/pull_request_template.md`. Do not skip required sections. If a required field doesn't apply, write `N/A` with a one-line reason — don't omit the section.

### If no template exists

Use this shape:

```
## Summary
<One paragraph. What this PR does, why, and which AC it closes. Reference the Story id. Lead with the user-visible change, not the implementation.>

## Test plan
- [ ] <command> — <result>
- [ ] <command> — <result>

## Risk
- <category>: <one line>. Categories: security / performance / operations / compatibility / tech-debt. If none, write "None".

## Review findings
- <N> `fix-here` items addressed; see commits.
- <N> `fix-next` items deferred; see linked tickets.
- <N> `needs-human` items; see comments below.
```

UI / output changes: attach a screenshot or before/after. If the PR template doesn't have a screenshot slot, add one in the Summary.

## Title

Follow the repo's commit-title convention. If recent merged PR titles use Conventional Commits (`feat(auth): …`), use that. If they don't, mirror the dominant local pattern. The title format:

```
<type>(<scope>): <imperative summary> (#<story-id>)
```

`<scope>` is optional but encouraged.

## Execution

```bash
# 1. Push the branch
git push -u origin <branch>

# 2. Write the body to a temp file (avoid shell-escape pain)
cat > /tmp/pr-body.md <<'EOF'
...body here...
EOF

# 3. Create the PR
gh pr create \
  --base <base> \
  --head <branch> \
  --title "<title>" \
  --body-file /tmp/pr-body.md \
  --reviewer <handle1>,<handle2> \
  --label <labels>
```

If `gh` is not authenticated, stop and tell the user to run `gh auth login`. Don't try to authenticate on their behalf.

## After opening

- Print the PR URL.
- If `review-what` had any `needs-human` items, post them as a single PR comment so the human sees them on the thread.
- Do not auto-merge. The human owns the merge.

## What not to do

- Don't open a PR before `review-what` has been run. A PR opened against un-triaged findings will gather drive-by comments that re-litigate the triage.
- Don't include unrelated changes in the same PR. If `git status` shows stray edits, stop and ask.
- Don't add reviewers the user hasn't approved. If CODEOWNERS resolves to a long list, list them all but flag it for the user.
- Don't invent a branch naming convention when the repo's `AGENTS.md` is silent — stop and ask.
