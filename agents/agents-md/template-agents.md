# AGENTS.md 模板（基线）

> 读者：AI agent。
> 用途：基线。每接入一个新 repo，复制本文件为 `<repo-name>-agents.md`，按需覆盖或追加。
> 体量目标：实际 AGENTS.md ≤200 行。
> 跨仓库规则（知识分层、Skills 加载机制、docs/ 布局）：见 `alphonse-studio/docs/knowledge-layering.md`。

## 定位
Agent 优先。人类掌舵、Agent 执行。目标是可靠、可验证、小范围持续交付。

## 工作规则
- 仓库文档优先于对话历史。
- 小步、可逆、可测试。
- 没有验证证据，不得标记完成。
- 改代码同步改文档、测试与计划。
- 反复失败时，先改善系统而非只改实现。
- 假设先在 `docs/assumptions/<id>.md` 显式记录再使用；被验证后从 `assumptions/` 移除或迁到 `domain/`。
- 外部输入在使用前完成验证（schema / 边界 / 类型）。
- 架构决策影响 structure / 关键质量属性 / 难逆转时，先写 `docs/adr/NNNN-<title>.md`（四位序号 + kebab-case）；小范围架构变更在 `docs/architecture/` 留痕即可。
- 跳过默认工作流环节时，输出开头声明跳过了哪一步。
- 中文撰写；命令、路径、接口名、代码标识符保留英文。
- 输出先说目标和理由；下一步收敛在当前 task scope 内。

## 完成定义

ticket 完成 = agent 自检通过 + human 验收通过。两段各自独立负责。

### Agent 自检（agent 工作流止点）
- 所有 AC 已勾选（`- [ ]` → `- [x]`）。
- 运行检查全过：UT + IT + lint + type-check + format + build。
- 变更已同步：受影响的文档、测试、计划 commit 到 working tree。
- ADR 触发已留痕：若命中 ADR 阈值，对应 `docs/adr/NNNN-<title>.md` 已 commit。
- 证据已记录：每条 AC 的验证摘要 + 关键命令输出写到对应 ticket comment（带 ID）。
- 风险已备注：自由文本（安全 / 性能 / 运维 / 兼容性 / 技术债），PR 模板 Risk 段 + ticket comment 末尾各写一份。
- ticket Status 从 `ready-for-agent` → `ready-for-human`。
- PR 已开。

### Human 验收（PR merge 前提）
- reviewer 走完 PR review。
- 核对 agent 的 evidence + AC 勾选 + 风险备注一致。
- 决定 merge（ticket 关闭）或 reject（Status 回 `ready-for-agent`）。

## 禁止行为
- 大范围混合目的的 PR。
- 架构决策触发 ADR 阈值但未留 ADR 就 merge。
- 未在文档中记录的隐性假设进入业务逻辑。
- 未经验证的外部输入进入业务逻辑。

## 测试分层与 CI
- **UT**：不命中 real network / real DB / real filesystem / real subprocess 的测试；可用 TestDouble 替身。PR 阶段（秒级）。
- **IT**：命中 real DB（含 in-memory SQL）/ in-process mock server（MSW、WireMock）/ testcontainers 的测试。PR 阶段（分钟级）。若有 `Tiltfile`，依赖其服务；无 `Tiltfile` 的 repo 在 `<repo>-agents.md` 写明替代设施。
- **E2E / 合约**：拉起完整 stack，UI 或 over-the-wire REST 驱动；merge 后 + nightly。
- 流水线：unit → integration → e2e；前一层失败不进入下一层。
- PR 合并门禁：UT + IT 全过。

## 开发规范

### 分支
- 格式：`<type>/<story-id>-<short-desc>`，例如 `feat/AUTH-123-user-auth`、`fix/BUG-456-null-crash`。
- type 限 Conventional Commits 11 类：feat / fix / docs / style / refactor / perf / test / build / ci / chore / revert。
- 个人 / 实验分支用 `<user-name>/<short-desc>` 前缀（如 `tony/spike-foo`）。

### Commit
- 遵循 Conventional Commits 1.0.0。
- scope 可选但鼓励（`feat(auth): ...`）。
- footer 必填 `Refs #<issue>` 或 `Closes #<issue>`。

### Worktree
- 默认关；多分支并行（紧急修复、对比实验）时启用。
- 位置：仓库同级 `../<repo>-<branch>`。
- 分支合并 / 关闭后立即 `git worktree remove <path>`。

### PR 模板
- 路径：`.github/pull_request_template.md`（单一模板）。
- 三段：Summary / Test plan / Risk。
- Summary 开头标注 PR Type（feature / fix / chore），可不与分支 type 严格一致。
- Test plan：测试命令 + 结果摘要；UI / 输出类改动附截图。
- Risk：分类列举（安全 / 性能 / 运维 / 兼容性 / 技术债）；无风险写「无」。

## Skills 加载规则

### 默认工作流
- **完整链**：`scoped change`（需求已可描述）走 `wayfinder` → `grill-with-docs` → `to-spec` → `to-tickets` → `implement`（内含 `tdd` / `code-review`）。
- **探索模式**：vague / 大任务只走 `wayfinder` → `grill-with-docs`，不出 spec / tickets。
- **直接实施**：单文件 typo / config 调整，跳过 spec / tickets，直接 `implement`。
- 跨阶段不确定用哪个 skill：跑 `ask-matt`。

### 各链步产物路径
- skill 自身规定路径 → 走 skill。
- skill 未规定 → AGENTS.md 设默认路径：
  - `wayfinder` → `.scratch/<feature>/map.md`
  - `to-spec` → `.scratch/<feature>/spec.md`
  - `to-tickets` → `.scratch/<feature>/issues/<NN>-<slug>.md`（per `to-tickets` skill 既有约定）
  - `implement` → 代码 + 测试
- `grill-with-docs`：产物落 `docs/`（按 `docs/` 子目录布局）。

## .scratch/<feature>/ 布局

```
.scratch/<feature>/
  issues/        # ticket 文件
  story          # 软链到 docs/stories/<id>.md
  spec.md        # 当前 feature 的 spec
  pr/            # 占位，后续 write-pr skill
  review/        # 评审
    from-<reviewer>.md
    from-<reviewer>-comment.md
  show-me/       # 占位，后续 show-me skill
```