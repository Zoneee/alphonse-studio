# AGENTS.md

## 定位
本仓库面向 Agent 优先的软件开发方式。
人类负责舵，Agent 负责执行。
目标是可靠、可验证、小范围的持续交付。

## 工作规则
1. 不以对话历史作为唯一信息来源。
2. 以仓库文档作为共享事实与正式规则的首要知识来源；对开发者个人或仓库长期有价值的经验按 `capture-memory` skill 沉淀。
3. 优先做小步、可逆、可测试的改动。
4. 没有验证证据，不得标记工作已完成。
5. 改动代码时，同步更新受影响的文档与测试。
6. 所有产物文档必须使用中文撰写，仅保留命令、路径、接口名、代码标识符等必要英文原文。
7. 每次输出必须在前几行说清目标和理由。若给出下一步，必须收敛在当前 task scope 内，不得主动扩散到无关领域。

## 默认阅读顺序
1. 先读取根目录 `AGENTS.md`，建立通用规则、完成定义与工作流。
2. 读取 `CONTEXT.md` 建立领域术语；按任务主题进入 `docs/` 对应主题目录（架构、标准、运行手册等）。
3. 若任务涉及当前进行中的变更，进入 `.scratch/` 查看对应 feature 的 issue 与 spec。
4. 仅在任务需要时读取对应 Skills，具体规则见下文。
5. 开始实现前确认范围、验证方式与证据来源已经明确。

## 工作流
本仓库使用 Matt Pocock 工程链驱动 scoped change，两条平行路径：

### 探索与规划（任务模糊或过大，一次会话装不下）
用 `wayfinder` 画地图 → 拆成决策票逐张推进 → 路线清晰后交接给实施。

### 标准 scoped change（需求已可描述）
1. `grill-with-docs`：收敛需求，同步更新 `CONTEXT.md` 与 ADR。
2. `to-spec`：产出 spec，发布到 `.scratch/<feature>/`。
3. `to-tickets`：拆成 tracer-bullet tickets，标注阻塞关系。
4. `implement`：按票实施，内部驱动 `tdd` 与 `code-review`。
5. 关闭 issue，更新地图与相关文档。

### 任何时刻
不知道用哪个 skill 时，运行 `ask-matt`。

### 经验沉淀
任务形成可复用稳定经验时，进入 `capture-memory` skill 沉淀（分层规则见该 skill）。

## Skills 使用与加载规则
1. 完成任务所需的上下文构建后，Agent 必须主动读取与任务相关的 Skills 文件，不能把是否读取 Skills 的责任完全留给用户在对话中额外提醒。
2. 若用户显式指定某个 Skills 文件，Agent 必须优先采用该 Skills，并在不冲突时继续遵守 `AGENTS.md` 中的其余通用约束。
3. 若用户请求与当前自动选择的 Skills 不一致，Agent 必须明确说明最终采用了哪些 Skills，以及哪些是因为用户显式指定而被优先采用。
4. 在输出计划、开始实现或给出结论前，Agent 应先自检本次任务所需读取的 Skills 是否已经覆盖；不得在未读取相关 Skills 的情况下直接开始高风险或高歧义工作。

## 长期知识分层
长期经验按 `capture-memory` skill 分层沉淀（`/memories/` 个人 + 仓库 docs 共享规则），详见 `.agents/skills/capture-memory/SKILL.md`。

## 完成定义
满足以下全部条件，工作才算完成：
- 任务范围已满足
- 必要检查通过，且验证证据已记录
- 受影响文档与测试已按工作规则更新；若产出了可复用的长期经验，已按 `capture-memory` skill 沉淀
- 风险与后续事项已备注
- 输出符合工作规则第 7 条：目标与理由在前几行说清、步骤可直接执行

## 禁止行为
- 大范围混合目的的 PR
- 未在仓库文档中记录的隐性假设
- 未经验证的外部输入直接进入业务逻辑
- 沉默的架构漂移

## Agent skills

### Issue tracker

Issues and specs live as markdown files in `.scratch/<feature>/.` See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-label vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout — one `CONTEXT.md` at the repo root. See `docs/agents/domain.md`.
