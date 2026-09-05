## 工作流

- **完整链**：`scoped change`（需求已可描述）走 `wayfinder` → `grill-with-docs` → `to-spec` → `to-tickets` → `implement`（内含 `tdd` / `code-review`）。
- **探索模式**：vague / 大任务只走 `wayfinder` → `grill-with-docs`，不出 spec / tickets。
- **直接实施**：单文件 typo / config 调整，跳过 spec / tickets，直接 `implement`。
- 跨阶段不确定用哪个 skill：跑 `ask-matt`。

### 完成定义

- 所有 AC 已勾选（`- [ ]` → `- [x]`）。
- 运行检查全过：UT + IT + lint + type-check + format + build。
- 变更已同步：受影响的文档、测试、计划 commit 到 working tree。
- ADR/assumptions 触发留痕：见 `alphonse-studio/docs/knowledge-layering.md`。
- 证据已记录：每条 AC 的验证摘要 + 关键命令输出写到对应 ticket comment（带 ID）。
- 风险已备注（按 PR 模板 Risk 段分类）。
- 每个 PR 一个目的（feature / fix / chore / refactor 单选）。
- ticket Status 从 `ready-for-agent` → `ready-for-human`。
- PR 已开。

## 代码

### 代码风格
- 命名 / 错误处理 / 抽象层级 / 模块边界等约定由 repo 决定；写入 `<repo>-agents.md` 或 `CONTRIBUTING.md`。
- 中文撰写；命令、路径、接口名、代码标识符保留英文。

### 测试行为
- 业务逻辑改动走 `tdd` skill：red → green → refactor，单 seam 单测试。
- 禁止 anti-patterns：implementation-coupled / tautological / horizontal slicing。
- 测试命名 / fixture / 覆盖目标由 repo 决定；写入 `<repo>-agents.md`。

### Git 行为

#### 分支
- 格式：`<type>/<story-id>-<short-desc>`，例如 `feat/AUTH-123-user-auth`、`fix/BUG-456-null-crash`。`<type>` 限 Conventional Commits 11 类之一；`<story-id>` 用 ticket 系统 ID；`<short-desc>` 用 kebab-case 短语。
- 个人 / 实验分支用 `<user-name>/<short-desc>` 前缀（如 `tony/spike-foo`）。

#### Commit
- 遵循 Conventional Commits 1.0.0。
- scope 可选但鼓励（`feat(auth): ...`）。
- footer 必填 `Refs #<issue>` 或 `Closes #<issue>`。

#### Worktree
- 默认关；多分支并行（紧急修复、对比实验）时启用。
- 位置：仓库同级 `../<repo>-<branch>`。
- 分支合并 / 关闭后立即 `git worktree remove <path>`。

#### PR 模板
- 路径：`.github/pull_request_template.md`（单一模板）。
- 三段：Summary / Test plan / Risk。
- Summary 开头标注 PR Type（feature / fix / chore），可不与分支 type 严格一致。
- Test plan：测试命令 + 结果摘要；UI / 输出类改动附截图。
- Risk：分类列举（安全 / 性能 / 运维 / 兼容性 / 技术债）；无风险写「无」。

## 测试

### 测试分层与 CI
- UT：不命中 real network / DB / fs / subprocess。PR 阶段。
- IT：命中 real DB 或 in-process mock server。PR 阶段。
- E2E / 合约：拉起完整 stack。merge 后 + nightly。
- 流水线：unit → integration → e2e；前一层失败不进入下一层。
- PR 合并门禁：UT + IT 全过。
- IT 设施：若有 `Tiltfile` 则依赖其服务；无则在本 repo 的 agents.md 写明替代设施。
