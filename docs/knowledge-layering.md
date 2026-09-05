# 长期知识分层

适用范围：所有由本仓库（`alphonse-studio`）统一管理 AGENTS.md 的消费方 repo。

## 分层定义

| 层 | 路径 | 写入什么 |
| --- | --- | --- |
| 跨仓库共享规则 | `alphonse-studio/docs/` | 默认工作流、skills 加载机制、知识分层、AGENTS.md 模板本身 |
| 当前 repo 复用经验 | `<repo>/docs/` | 仓库专属的可复用经验、验证结论、已确认约束、实践建议 |
| 当前 feature 工作产物 | `<repo>/.scratch/<feature>/` | 当前进行中的 issue、spec、PR 草稿、review、demo |

## 写入规则

- 改变跨仓库共享事实、接口契约、正式流程、架构边界：必须回写 `alphonse-studio/docs/`，必要时同步回 `<repo>/docs/`。
- 当前 repo 的可复用经验、踩坑教训、验证结论、仓库级操作习惯：写入 `<repo>/docs/`，**不**再使用独立的 `/memories/repo/` 层。
- 当前 feature 进行中的产物（未稳定的）：留在 `<repo>/.scratch/<feature>/`，不要回写 docs。

## 与 AGENTS.md 的关系

AGENTS.md 是一份「每次会话都吃 token」的清单。它只承载「agent 在该 repo 必须遵守的硬规则」。分层规则本身**不在** AGENTS.md 内重复；AGENTS.md 通过一行指针指向本文件。