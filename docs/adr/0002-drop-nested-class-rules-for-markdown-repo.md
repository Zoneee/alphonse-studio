# Drop "禁止嵌套类 / 禁止一个文件包含多个类" rules for this Markdown-only repo

Status: accepted

`alphonse-studio` 只持有 Markdown（skills / 模板 / docs），不存在承载类的可执行代码。「禁止嵌套类」「禁止一个文件包含多个类」在本 repo 是 dead-on-arrival 的 no-op。规则从 instance（`agents/agents-md/alphonse-studio-agents.md`）删除，但保留在 template（`agents/agents-md/template-agents.md`）供下游有代码上下文的 repo 使用；若本 repo 未来新增代码上下文，再按模板规则补回。
