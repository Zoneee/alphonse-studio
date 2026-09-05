## 工作流

- **完整链**：`scoped change`（需求已可描述）走 `wayfinder` → `grill-with-docs` → `to-spec` → `to-tickets` → `implement`（内含 `tdd` / `code-review`）。
- **探索模式**：vague / 大任务只走 `wayfinder` → `grill-with-docs`，不出 spec / tickets。
- **直接实施**：单文件 typo / config 调整，跳过 spec / tickets，直接 `implement`。
- 跨阶段不确定用哪个 skill：跑 `ask-matt`。
- `handoff` 是临时一次性文件：写完一次后冻结，同一会话内不重写、不追加；只有再次调用 `/handoff` 才重写。

### `.scratch/<story-id>/` 布局

```
.scratch/<story-id>/
  issues/        # ticket 文件
  story          # 软链到 docs/features/<id>-feature-<slug>/story/<id>-story-<slug>.md
  spec.md        # 当前 story 的 spec
  pr/            # write-pr skill 的 PR body 草稿
  review/        # review-finding / review-what 产出
    from-<reviewer>.md
    from-<reviewer>-comment.md
  show-me/       # show-me skill 产出
```

## 代码

### 代码风格

- 命名 / 错误处理 / 抽象层级 / 模块边界等约定由 repo 决定；写入 `<repo>-agents.md` 或 `CONTRIBUTING.md`。
- 中文撰写；命令、路径、接口名、代码标识符保留英文。
- Skill 输出的文档、对话内容使用中文（这条规则放 AGENTS.md，不放 skill 里，让 skill 保持语言无关、跨 repo 复用）。
- 禁止嵌套类。
- 禁止一个文件包含多个类。

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
- Message 使用中文。

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

## 本 repo 备注

alphonse-studio 是 AGENTS.md 模板与 Skills 的**中央仓库**，不持有产品代码。本节是与通用模板的偏差：

- **代码风格 > 禁止嵌套类 / 禁止一个文件包含多个类**：本 repo 的「代码」是 Markdown（skill / 模板 / docs），不涉及类的概念。这两条按模板保留，但实际无适用对象。
- **测试分层与 CI**：本 repo 无自动化 UT/IT/E2E。skill / 模板改动通过 agent 加载后跑 dry-run 验证。
- **PR 模板**：本 repo 没有 `.github/pull_request_template.md`；PR body 直接采用模板的三段格式（Summary / Test plan / Risk）。
- **Handoff 输出位置**：本 repo 通用规则仅约束一次性行为；输出到 OS temp dir 的具体约定由 `handoff` skill 自己负责（不在 AGENTS.md 重复）。
