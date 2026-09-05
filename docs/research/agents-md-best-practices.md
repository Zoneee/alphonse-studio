# AGENTS.md 模板设计 — 最佳实践查证

> Primary-source research for an `AGENTS.md` template that will be shared across multiple repos. Three topics: testing-layering/CI, doc-index inside `AGENTS.md`, Git conventions.

## 1. 测试分层与 CI 顺序

### 关键发现

- **没有一个"统一权威形状"**: Martin Fowler 本人在 2021 年的 [On the Diverse And Fantastical Shapes of Testing](https://martinfowler.com/articles/2021-test-shapes.html) 中明确指出，分歧很大程度是因为 "the terms 'unit test' and 'integration test' have always been rather murky" — 测试形状之争更多是术语之争。
- **共识**: 各派都同意底层测试要多、上层测试要少。Fowler 原始 Test Pyramid: "you should have many more low-level UnitTests than high level BroadStackTests running through a GUI"; Vocke (ThoughtWorks) 在 [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) 总结为: "1. Write tests with different granularity. 2. The more high-level you get the fewer tests you should have".
- **当前社区主流**: 综合 Kent C. Dodds 的 Testing Trophy (前端) + Google's Mike Wacker 文章 + Fowler 2021 年的讨论 — **偏向"integration 占大头、unit + e2e 收尾"** 的分层，但前提是 unit test 的定义是"solitary / 全部 mock"那种。Dodds 的金句: "The more your tests resemble the way your software is used, the more confidence they can give you".
- **CI 顺序**: Ham Vocke (ThoughtWorks) 在 [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) 把 build pipeline 描述为多层: "With continuous delivery you use a build pipeline to automatically test your software and deploy it"; 测试在 pipeline 中应按从快到慢、从低到高排序 (unit → integration → e2e)，快层失败直接阻断，慢层在更高阶段运行。Mike Wacker 在 Google Testing Blog 的 [Just Say No to More End-to-End Tests](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html) 中明确推荐: "It's fast. ... It's reliable. ... It isolates failures" 作为 feedback loop 标准 — 这是 unit 层的核心。
- **合并门禁**: GitHub flow ([docs.github.com](https://docs.github.com/en/get-started/using-github/github-flow)) 通过 branch protection 实现: "Branch protection settings may block merging if your pull request does not meet certain requirements. For example, you need a certain number of approving reviews or an approving review from a specific team." — CI 是其中一项 gate。Trunk-Based Development 的官方立场 ([trunkbaseddevelopment.com](https://trunkbaseddevelopment.com/)) 是"short-lived feature branches ... are used for code-review and build checking (CI), but not artifact creation or publication" — 即 PR 上跑完整的 CI (含 IT)，nightly/merge 后跑 e2e 与发布相关层。

### 推荐组合

| 层 | 命名 | 何时跑 | CI 阶段 |
|---|---|---|---|
| UT (单元) | unit | pre-commit hook + 每次 PR | 第 1 阶段 (秒级) |
| IT (集成) | integration | 每次 PR | 第 2 阶段 (分钟级) |
| E2E / 系统 | e2e | merge 到 main + nightly | 第 3 阶段 / 定时任务 |
| 合约 / CDC | contract | 每次 PR + 发布前 | 与 IT 并列 |

合并门禁: PR 必须通过 UT + IT 才能 merge; E2E 在 main 上做持续验证 (post-merge gate)。

### 来源

- [The Test Pyramid (Martin Fowler bliki)](https://martinfowler.com/bliki/TestPyramid.html) — quoted claim: "you should have many more low-level UnitTests than high level BroadStackTests running through a GUI."
- [The Practical Test Pyramid (Ham Vocke, ThoughtWorks)](https://martinfowler.com/articles/practical-test-pyramid.html) — quoted claim: "1. Write tests with different granularity. 2. The more high-level you get the fewer tests you should have."; 描述 build pipeline 多层结构。
- [On the Diverse And Fantastical Shapes of Testing (Martin Fowler, 2021)](https://martinfowler.com/articles/2021-test-shapes.html) — quoted claim: "the pyramid argues that you should have most testing done as unit tests, the honeycomb and trophy instead say you should have a relatively small amount of unit tests and focus mostly on integration tests"; 解释分歧源自术语不一致。
- [The Testing Trophy and Testing Classifications (Kent C. Dodds, 2021)](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications) — quoted claim: "The more your tests resemble the way your software is used, the more confidence they can give you."; 区分 unit (mocked) vs integration (真实协作)。
- [Just Say No to More End-to-End Tests (Mike Wacker, Google Testing Blog, 2015)](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html) — quoted claim: "It's fast. ... It's reliable. ... It isolates failures." — 这是 unit-level feedback loop 的核心特性；用 nightly E2E 跑全栈并展示端到端测试反馈循环慢、flaky、难定位的根本问题。
- [Trunk-Based Development (Paul Hammant)](https://trunkbaseddevelopment.com/) — quoted claim: "short-lived feature branches ... are used for code-review and build checking (CI), but not artifact creation or publication, to happen before commits land in the trunk for other developers to depend on."
- [GitHub flow (GitHub Docs)](https://docs.github.com/en/get-started/using-github/github-flow) — quoted claim: "Branch protection settings may block merging if your pull request does not meet certain requirements."

---

## 2. AGENTS.md 是否应包含文档索引

### 关键发现

- **官方 agents.md 规范 (agents.md)** 明确说 AGENTS.md 是"extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren't relevant to human contributors" — 它的定位是**给 agent 的额外上下文**，不是文档目录。
- **嵌套优于索引**: agents.md 官方推荐用嵌套 AGENTS.md: "Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree, so the closest one takes precedence and every subproject can ship tailored instructions." — 索引的替代方案是"放在离它描述的内容最近的地方"。
- **Claude Code 的官方指引 (code.claude.com/docs/en/memory)**:
  - "target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence." — 索引会让文件膨胀，违反这条。
  - "CLAUDE.md files can import additional files using `@path/to/import` syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them." — Claude Code 提供 `@path/to/import` 机制按需引入。
  - "imported files still load and enter the context window at launch" — 但 import 仍消耗 context (只是分散在文件里)，并不能解决"内容太多"的问题；这只是组织手段。
- **Claude Code 明确支持 AGENTS.md**: 它直接读取 `AGENTS.md` 作为 `CLAUDE.md` 的等价物 ([code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory) 有 AGENTS.md 小节)。`CLAUDE.md` 的所有规则同样适用。
- **OpenAI Codex 官方 AGENTS.md 示例** ([openai/codex/AGENTS.md](https://github.com/openai/codex/blob/main/AGENTS.md)) 没有文档索引 — 而是直接的指令、规则、命令。其结构是按"代码风格 / 测试 / 模块组织 / 命令"分组的内联规则，不是文档索引。
- **指引应放在 AGENTS.md，文档应放在 docs/**: `AGENTS.md` 是一份"在每次会话里都吃 token 的清单"。索引每一份 docs 路径，等于每次启动都把目录结构注入 context — 既偏离主题又增加 context load。更便宜的做法是描述"如何找到 docs"(`docs/architecture/`、`docs/runbooks/`)以及"哪些 docs 在哪些场景下需要读"。

### 推荐

- `AGENTS.md` **不要**做"全文档目录" — 它只列"agent 在做某类任务时必须读的几份关键文档"的指针，每条带一行的读取触发条件。
- 详细架构/runbook 留在 `docs/`，用嵌套 `AGENTS.md` 或 `.scratch/<feature>/AGENTS.md` 在那个子目录里补充上下文。
- 对 Claude Code / Cursor 这类支持 `@path` 的 agent，可以用 `@docs/architecture/X.md` 形式按需拉入相关章节；不要把整份索引原文塞进 `AGENTS.md`。

### 来源

- [agents.md — 官方规范](https://agents.md/) — quoted claim: "AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren't relevant to human contributors."; "Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree."
- [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory) — quoted claim: "Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."; "CLAUDE.md files can import additional files using `@path/to/import` syntax."; "imported files still load and enter the context window at launch."
- [Claude Code — Give Claude context: CLAUDE.md and better prompts](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts) — Anthropic 官方对 CLAUDE.md 的内容指引 (聚焦 build/test / 项目结构)。
- [OpenAI Codex AGENTS.md 示例](https://github.com/openai/codex/blob/main/AGENTS.md) — 一线 OpenAI 项目 AGENTS.md 内容示例 (无文档索引，按"风格/测试/模块/命令"组织)。
- [awesome-agents-md (danielrosehill)](https://github.com/danielrosehill/awesome-agents-md) — 社区 curated 真实 AGENTS.md 列表；其 templates/minimal.md 与 examples/nextjs-shop.md 也都不做文档目录，而是直接是命令与禁止项。

---

## 3. Git 开发规范默认值

### 分支命名

推荐：**`<type>/<short-kebab-case-desc>`** (例如 `feat/user-auth`, `fix/null-pointer-crash`, `chore/bump-deps`)。理由：与 Conventional Commits 类型保持一致，便于从分支名一眼识别意图，且和大多数 GitHub/GitLab 工具链的默认 branch protection 规则兼容。

来源: [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) — quoted claim: "A short, descriptive branch name enables your collaborators to see ongoing work at a glance. For example, `increase-test-timeout` or `add-code-of-conduct`."; [Vincent Driessen git-flow](https://nvie.com/posts/a-successful-git-branching-model/) — 命名规范 `feature-*`、`release-*`、`hotfix-*` 的事实标准。

### Commit 信息格式

推荐：**Conventional Commits 1.0.0** (`<type>[optional scope]: <description>` + 可选 body + 可选 footer)。理由：与 SemVer 自动对齐，CHANGELOG 可自动生成，是 de-facto 标准。

来源: [Conventional Commits 1.0.0 规范](https://www.conventionalcommits.org/en/v1.0.0/) — quoted claim: "Commits MUST be prefixed with a type, which consists of a noun, `feat`, `fix`, etc., followed by the OPTIONAL scope, OPTIONAL `!`, and REQUIRED terminal colon and space."; "fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning). feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning)."

### Worktree

推荐：**默认不用；需要并行多个分支（紧急修复、对比实验、并行 PR）时用**。理由：`git worktree` 是 Git 官方机制解决"半成品 branch 不能 checkout 别的 branch"的问题；当一个 worktree 的状态太乱、无法 stash 但又必须切到别处工作时，价值最大。平时不必要。

来源: [git-worktree Documentation (git-scm.com)](https://git-scm.com/docs/git-worktree) — quoted claim: "You are in the middle of a refactoring session and your boss comes in and demands that you fix something immediately. You might typically use git-stash to store your changes away temporarily, however, your working tree is in such a state of disarray (with new, moved, and removed files, and other bits and pieces strewn around) that you don't want to risk disturbing any of it. Instead, you create a temporary linked worktree to make the emergency fix, remove it when done, and then resume your earlier refactoring session." Claude Code 官方文档 [memory docs](https://code.claude.com/docs/en/memory) 也明确以 worktree 作为多 worktree 个人指令分发场景: "If you work across multiple git worktrees of the same repository..."

### PR 模板

推荐：**`.github/pull_request_template.md` 含固定三段 (Summary / Test plan / Risk)**。理由：是 GitHub 官方约定的路径；让 agent 在生成 PR 时有结构化输出。

来源: [GitHub flow (docs.github.com)](https://docs.github.com/en/get-started/using-github/github-flow) — quoted claim: "When you create a pull request, include a summary of the changes and what problem they solve."; "If your pull request addresses an issue, link the issue so that issue stakeholders are aware of the pull request and vice versa." (描述了 PR 模板的标准章节)

---

## 4. 综合建议（给模板用的）

1. **测试分层**: UT + IT 必须在 PR 阶段跑过才能 merge；E2E 与发布相关层放在 merge 后 (nightly + main 触发)；合约/CDC 测试作为 IT 的子层。三段命名建议 `unit / integration / e2e`，明确 CI 的阶段映射写在 AGENTS.md。
2. **AGENTS.md 定位**: 不当文档目录。**它**描述的是"agent 必须遵守的硬规则、必跑的测试命令、必填的 PR 章节、必查的链接"。**docs/** 才是放详情的；`AGENTS.md` 用指针加触发条件按需 `@import`。
3. **AGENTS.md 体量**: 严守 ~200 行上限 (Claude Code 官方建议)。超出部分，要么用嵌套 AGENTS.md (子目录专属)，要么用 `@import`。
4. **Git 默认**: Conventional Commits + `<type>/<short-desc>` 分支 + `.github/pull_request_template.md` 三段 (Summary / Test plan / Risk) + worktree 按需启用。
5. **来源一致性提示**: 用户问题中提到 "Source: Martin Fowler, Kent C. Dodds, Google testing blog, Microsoft / ThoughtWorks" — 其中 **Microsoft 没有测试金字塔的官方一手文章**，我们用的是 ThoughtWorks (Vocke 在 ThoughtWorks 写、Fowler 站点发布)。修正后的权威一手来源清单见各小节"来源"部分。