## Agent skills

### Issue tracker

GitHub Issues（`gh` CLI；remote `git@github.com:Zoneee/alphonse-studio.git`）。详见 `docs/agents/issue-tracker.md`。

### Triage labels

5 个 canonical role：`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`。详见 `docs/agents/triage-labels.md`。

### Domain docs

单 context：`CONTEXT.md`（如存在）+ `docs/adr/`。详见 `docs/agents/domain.md`。

## 工作流

- turn by turn 使用中文。
- **完整链**：`scoped change` 走 `wayfinder` → `grill-with-docs` → `to-spec` → `to-tickets` → `implement`（内含 `tdd` / `code-review`）。
- **探索模式**：vague / 大任务只走 `wayfinder` → `grill-with-docs`，不出 spec / tickets。
- **直接实施**：单文件 typo / config 调整，跳过 spec / tickets，直接 `implement`。
- 跨阶段不确定用哪个 skill：跑 `ask-matt`。
- `handoff` 是临时一次性文件：写完一次后冻结，同一会话内不重写、不追加；只有再次调用 `/handoff` 才重写。

### `.scratch/<story-id>/` 布局

详见 `docs/agents/scratch-layout.md`。

## 代码

### 代码风格

- 中文撰写；命令、路径、接口名、代码标识符保留英文。

### 测试行为

- 业务逻辑改动走 `tdd` skill：red → green → refactor，单 seam 单测试。
- 禁止 anti-patterns：implementation-coupled / tautological / horizontal slicing。

### Git 行为

#### 分支

- 格式：`<type>/<story-id>-<short-desc>`，例如 `feat/#3-skill-contract`、`fix/#7-write-skills`。`<type>` 限 Conventional Commits 11 类之一；`<story-id>` 用 GitHub Issues 数字 ID（`#<n>`）；`<short-desc>` 用 kebab-case 短语。
- 个人 / 实验分支用 `<user-name>/<short-desc>` 前缀（如 `tony/spike-foo`）。

#### Commit

- 遵循 Conventional Commits 1.0.0。
- scope 可选但鼓励（`feat(auth): ...`）。
- footer 必填 `Refs #<issue>` 或 `Closes #<issue>`。
- Message 使用中文。

#### Worktree

- 默认关；多分支并行（紧急修复、对比实验）时启用。
- 位置：仓库同级 `../<repo>-<branch>`。
- 分支合并 / 关闭后立即 `git worktree remove <path>`。

## 测试

### 测试分层与 CI

- UT：不命中 real network / DB / fs / subprocess。PR 阶段。
- IT：命中 real DB 或 in-process mock server。PR 阶段。
- E2E / 合约：拉起完整 stack。merge 后 + nightly。
- 流水线：unit → integration → e2e；前一层失败不进入下一层。
- PR 合并门禁：UT + IT 全过。
- IT 设施：若有 `Tiltfile` 则依赖其服务；无则在本 repo 的 agents.md 写明替代设施。

## 本 repo 备注

alphonse-studio 是 AGENTS.md 模板与 Skills 的**中央仓库**，不持有产品代码。本节是与通用模板的偏差：

- **测试分层与 CI**：本 repo 无自动化 UT/IT/E2E。skill / 模板改动通过 agent 加载后跑 dry-run 验证。
- **Handoff 输出位置**：本 repo 通用规则仅约束一次性行为；输出到 OS temp dir 的具体约定由 `handoff` skill自己负责（不在 AGENTS.md 重复）。
