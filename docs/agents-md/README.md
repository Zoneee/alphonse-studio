# AGENTS.md 映射登记

本表记录每个消费方 repo 与 `agents/agents-md/` 下对应文件的关系。

## 字段

| 字段 | 含义 |
| --- | --- |
| repo | 消费方 repo 名（与目录名一致） |
| md 文件 | `agents/agents-md/` 下对应的文件名 |
| 绝对路径 | 软链接指向的完整路径 |
| 模板偏离度 | `none` = 与模板一致；`light` = 少量覆盖；`heavy` = 大幅重写 |
| 最后核对日期 | 上次人工核对软链接与文件内容的日期（YYYY-MM-DD） |

## 登记条目

| repo | md 文件 | 绝对路径 | 模板偏离度 | 最后核对日期 |
| --- | --- | --- | --- | --- |
| alphonse-studio | `alphonse-studio-agents.md` | `/home/alphonse/projects/alphonse-studio/agents/agents-md/alphonse-studio-agents.md` | light | 2026-09-05 |

`alphonse-studio` 是第一个 consumer —— 即它本身就是 AGENTS.md 模板与 Skills 的源仓库，但仍以 consumer 身份受模板约束；其 `<repo>-agents.md` 末尾的「本 repo 备注」段记录它与通用模板的偏差。

## 新增条目流程

1. 在 `agents/agents-md/` 下创建 `<repo-name>-agents.md`。
2. 在消费方 repo 根目录建软链接：
   - `ln -s /home/alphonse/projects/alphonse-studio/agents/agents-md/<repo-name>-agents.md AGENTS.md`
3. 在本表插入新行，填齐五个字段。
4. 核对日期写当天。
