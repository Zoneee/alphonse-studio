# Defer `<repo>-agents.md>` placeholder rule

Status: accepted

`agents/agents-md/alphonse-studio-agents.md` 中的两条「写入 `<repo>-agents.md` 或 `CONTRIBUTING.md`」占位符规则被删除——占位符泄漏到本 repo 自身配置时没有具体目标，写下去只会让 agent 去读一个不存在的文件。等本 repo 的约定语言统一后，再用真实文件名把规则填回去（参见 `template-agents.md` 的同段规则，下游 repo 仍按模板走）。
