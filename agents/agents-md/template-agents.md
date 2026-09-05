# AGENTS.md 模板（基线）

> 读者：AI agent。
> 用途：基线。每接入一个新 repo，复制本文件为 `<repo-name>-agents.md`，按需覆盖或追加。
> 体量目标：实际 AGENTS.md ≤200 行。
> 跨仓库规则（知识分层、Skills 加载机制）：见 `alphonse-studio/docs/knowledge-layering.md`。

## 定位
Agent 优先。人类掌舵、Agent 执行。目标是可靠、可验证、小范围持续交付。

## 工作规则
- 仓库文档优先于对话历史。
- 小步、可逆、可测试。
- 没有验证证据，不得标记完成。
- 改代码同步改文档、测试与计划。
- 反复失败时，先改善系统而非只改实现。
- 中文撰写；命令、路径、接口名、代码标识符保留英文。
- 输出先说目标和理由；下一步收敛在当前 task scope 内。

## 完成定义
- 任务范围满足。
- 必要检查通过；验证证据已记录。
- 受影响文档与测试已同步更新。
- 风险与后续事项已备注。
- 输出符合「目标-理由-步骤」结构。

## 禁止行为
- 大范围混合目的的 PR。
- 未在文档中记录的隐性假设进入业务逻辑。
- 未经验证的外部输入进入业务逻辑。
- 沉默的架构漂移。

## 测试分层与 CI
- **UT**：mock-based 编排检测。PR 阶段跑（秒级）。
- **IT**：真实基础设施验证。PR 阶段跑（分钟级）。如有 `Tiltfile`，依赖 tiltfile 提供的设施。
- **E2E / 合约**：merge 到 main 后 + nightly。
- 流水线顺序：unit → integration → e2e。前一层失败不进入下一层。
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
  story          # 软链到上游 story 文档
  spec.md        # 当前 feature 的 spec
  pr/            # 占位，后续 write-pr skill
  review/        # 评审
    from-<reviewer>.md
    from-<reviewer>-comment.md
  show-me/       # 占位，后续 show-me skill
```

## 跨仓库规则
- 长期知识分层、Skills 加载机制：见 `alphonse-studio/docs/knowledge-layering.md`。
- 当前 repo 的复用经验统一沉淀到 `<repo>/docs/`，不使用独立的 memories 层。