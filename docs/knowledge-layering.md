# 长期知识分层与 docs/ 布局

适用范围：所有由本仓库（`alphonse-studio`）统一管理 AGENTS.md 的消费方 repo。

## 三层定义

| 层 | 路径 | 写入什么 |
| --- | --- | --- |
| 跨仓库共享规则 | `alphonse-studio/docs/` | 默认工作流、Skills 加载机制、知识分层、AGENTS.md 模板本身 |
| 当前 repo 长期产物 | `<repo>/docs/` | 仓库专属的 Story、ADR、架构、运行手册、领域词汇、未验证前提 |
| 当前 feature 工作产物 | `<repo>/.scratch/<feature>/` | 当前进行中的 issue、spec、PR 草稿、评审、demo |

## `<repo>/docs/` 子目录布局（6 个固定）

```
docs/
  README.md                  # 一页入口，链到各子目录
  stories/<id>.md            # user story + workflow + AC + context + 带 ID 的 Comment
  adr/NNNN-<title>.md        # 架构决策记录（四位序号 + kebab-case）
  architecture/              # 当下系统描述（可重写）
    overview.md
    components.md
    data-model.md
  runbooks/<scenario>.md     # 运维手册（imperative + step-by-step）
  domain/                    # 稳定事实
    glossary.md
    facts.md
  assumptions/<id>.md        # 未验证前提（会过期；验证后迁到 domain/ 或删除）
```

子目录清单是受控产物。新增顶层 `docs/` 子目录必须先改本文件 + 对应 `<repo>-agents.md`。

## 写入规则

- 改变跨仓库共享事实、接口契约、正式流程、架构边界：必须回写 `alphonse-studio/docs/`，必要时同步回 `<repo>/docs/`。
- 决策影响 structure / 关键质量属性 / 难逆转：写 `<repo>/docs/adr/NNNN-<title>.md`（Nygard 五字段：Title / Context / Decision / Status / Consequences）。
- 当前 repo 的可复用经验、踩坑教训、验证结论、仓库级操作习惯：写入 `<repo>/docs/` 对应子目录。
- 未验证前提：写入 `<repo>/docs/assumptions/<id>.md`；验证通过后迁到 `domain/facts.md`，未通过则删除。
- 当前 feature 进行中的产物（未稳定的）：留在 `<repo>/.scratch/<feature>/`，不回写 docs。
- 当前 feature 的 story 软链：`<repo>/.scratch/<feature>/story` → `<repo>/docs/stories/<id>.md`。

## ADR 状态机

- `Proposed` → `Accepted` →（可）`Deprecated` / `Superseded`。
- ADR 文件 append-only。supersede 时保留旧文件，在 Status 字段加新 ADR 链接。

## 与 AGENTS.md 的关系

AGENTS.md 是「每次会话都吃 token」的清单。它只承载「agent 在该 repo 必须遵守的硬规则」。分层规则与 docs/ 布局本身**不在** AGENTS.md 内重复；AGENTS.md 通过一行指针指向本文件。