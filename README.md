# alphonse-studio

中央仓库：管理所有消费方 repo 共享的 `AGENTS.md` 模板与 Skills。

---

## Skill 与 AGENTS.md 的边界

**Skill** 是集中管理、跨 repo 复用的工作流定义。语言中性（默认英文），承载稳定的步骤、规则与判定准则；改动一处，所有 consumer repo 同步生效。

**AGENTS.md** 是每个 repo 的 per-repo 文件（位于 `agents/agents-md/<repo-name>-agents.md`），承载该 repo 独有的命名 / 错误处理 / 测试约定，以及对 skill 默认行为的少量覆盖（输出目录、输出语言、scratch 布局等）。

### 修改原则

- **改 Skill**：当规则跨 repo 通用。改完所有 consumer repo 跟随。
- **改 `<repo>-agents.md`**：当规则只适用于当前 repo，或仅需覆盖某个 skill 的默认行为。

### Skill 默认值与 per-repo AGENTS.md 的覆盖关系

每个 skill 在其 `## Output`（或类似段落）声明默认输出路径与默认输出语言。这些是 share-friendly 的默认。

`<repo>-agents.md` 可以覆盖这些默认——例如：

- 重写 `<repo>/.scratch/<story-id>/` 布局
- 指定 skill 输出用其他语言（如英文）
- 把 skill 产物落到不同路径

冲突时：`<repo>-agents.md` 优先。

### 内容语言规则

Skill 自身可用英文写（稳定、跨 repo 复用、不易过时）。Skill **输出的文档、对话内容**使用中文 —— 这条规则统一放 AGENTS.md（不在 skill 里），以便个别 repo 需要英文时直接在 per-repo 文件里覆盖。

### commit / comment 的中文

`AGENTS.md` 模板的 Commit 段要求 `Message 使用中文`，避免阅读 commit log 时来回切语言。

---

## 仓库结构

```
alphonse-studio/
  agents/
    agents-md/
      template-agents.md                # AGENTS.md 模板
      alphonse-studio-agents.md         # 本仓库自己的 AGENTS.md（per-repo）
    skills/                              # 所有共享 skill 的源
  docs/
    knowledge-layering.md               # 三层知识定义 + docs/ + .scratch/ 布局
    agents-md/README.md                 # consumer repo 注册表
    research/                            # 历次研究产出
```

---

## Consumer repo 接入流程

1. 复制 `agents/agents-md/template-agents.md` → `agents/agents-md/<repo-name>-agents.md`。
2. 按该 repo 实际状况改 `<repo-name>-agents.md`（命名约定 / 错误处理 / 测试命令等）。
3. 在消费方 repo 根目录建软链接：
   ```bash
   ln -s /home/alphonse/projects/alphonse-studio/agents/agents-md/<repo-name>-agents.md AGENTS.md
   ```
4. 在 `docs/agents-md/README.md` 表里加一行，登记这个 repo。

详见 `docs/agents-md/README.md`。
