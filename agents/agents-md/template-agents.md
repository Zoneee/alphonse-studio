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
- 任务范围满足。
- 必要检查通过；验证证据已记录。
- 受影响文档与测试已同步更新。
- 风险与后续事项已备注。

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
- 分支：`<type>/<short-desc>`，例如 `feat/user-auth`、`fix/null-crash`。
- Commit：Conventional Commits 1.0.0。
- Worktree：默认关；多分支并行（紧急修复、对比实验）时启用。
- PR 模板：`.github/pull_request_template.md` 三段（Summary / Test plan / Risk）。

## Skills 加载规则
- 默认工作流（scoped change）：`wayfinder` → `grill-with-docs` → `to-spec` → `to-tickets` → `implement`（内含 `tdd` / `code-review`）。
- 用户显式指定 skill 时优先采用；与默认选择冲突时显式列出所采用的 skills 与原因。
- 输出计划或结论前，自检本次任务的 skills 覆盖是否足够。

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