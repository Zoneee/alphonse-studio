# Grill Findings — UT/IT/E2E、ADR 阈值、docs/ 结构

> Primary-source research for `AGENTS.md` template. Companion to `agents-md-best-practices.md` (which covers testing-layering/CI, AGENTS.md scope, Git defaults). This file covers canonical definitions, ADR triggers, and `docs/` layout.

---

## 1. UT/IT/E2E 边界定义

### 推荐定义（一句话一层）

- **UT**: 程序员为自己的代码片段写的、低延迟可频繁运行的 xUnit 测试；既可以是 **solitary**（依赖全部替成 TestDouble）也可以是 **sociable**（用真实协作者），决定性区分是"low-level + done by programmer + fast"。
- **IT**: 验证"独立开发的模块连接起来之后是否如预期协作"——可以是 **narrow**（只测与外部 service 的交互 + 用 in-process/over-the-wire TestDouble）或 **broad**（拉起真实依赖跑全栈）。
- **E2E / Broad Stack Test**: 拉起"完全集成后的系统"，从外部用户视角（UI driver / over-the-wire REST）驱动，逐条走完关键 user journey。

### 判定细则

- **UT 不可触碰**：real network socket、real DB connection、real filesystem（tmpfs 仍属 I/O）、real subprocess、real clock（应用域里"now"必须可注入）。Vocke (ThoughtWorks) 明示："Test small pieces of your codebase in isolation and **avoid hitting databases, the filesystem or firing HTTP queries** (by using mocks and stubs for these parts) to keep your tests fast."
- **IT 可触碰**：real DB（特别是 in-memory SQLite、H2、testcontainers）、in-process 协议替身（MSW、WireMock、mountebank）、真实 clock 的可控封装；Fowler (2018) 把 narrow integration test 划入"narrow integration tests ... often run very fast, so can run in early stages of a DeploymentPipeline"。
- **临界情形归类**（社区共识而非单一权威）：
  - SQLite in-memory / H2 → IT（真实 SQL，只是进程内）。
  - testcontainers（Docker 启的 Postgres）→ IT，broad 那一端。
  - MSW / WireMock（in-process mock server）→ IT, narrow。
  - 纯进程内 state、零 I/O → 仍可作 UT。
  - **Fowler 2021 提示**：争议大部分是术语分歧，"when anyone starts talking about various testing categories, dig deeper on what they mean by their words, as they probably don't use them the same way as the last person you read did."
- **"Mostly integration" 取舍**：Kent C. Dodds："Write tests. Not too many. Mostly integration. ... **Integration tests strike a great balance on the trade-offs between confidence and speed/expense.**"（前提是 unit test 的定义是 solitary / all-mocked 那种。）

### CI 阶段映射

| 层 | 何时跑 | 时间预算 |
|---|---|---|
| UT（solitary + 大量 sociable） | pre-commit hook + 每次 PR | "compile suite sub-second to a few seconds; commit suite no more than ten minutes" (Kent Beck via Fowler) |
| IT（narrow + 部分 broad，DB/容器） | 每次 PR | 分钟级；"since narrow integration tests are limited in scope, they often run very fast, so can run in early stages of a DeploymentPipeline" (Fowler 2018) |
| E2E（UI driver、REST full-stack） | merge 到 main + nightly | 数十分钟；"End-to-end tests ... require a lot of maintenance and run pretty slowly" (Vocke 2018) |

合并门禁：PR 必须 UT + IT 全绿才能 merge；E2E 在 main 上做持续验证。

### 来源

- **Martin Fowler, [UnitTest (bliki)](https://martinfowler.com/bliki/UnitTest.html)** — "unit tests are low-level, focusing on a small part of the software system. Secondly unit tests are usually written these days by the programmers themselves ... Thirdly unit tests are expected to be significantly faster than other kinds of tests."; 定义 solitary vs sociable。
- **Martin Fowler, [IntegrationTest (bliki)](https://martinfowler.com/bliki/IntegrationTest.html)** — "narrow integration tests ... exercise only that portion of the code in my service that talks to a separate service ... uses test doubles ... often no larger in scope than a unit test"; "broad integration tests require live versions of all services"。
- **Ham Vocke (ThoughtWorks), [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)** — "avoid hitting databases, the filesystem or firing HTTP queries (by using mocks and stubs for these parts) to keep your tests fast"; "End-to-end tests ... require a lot of maintenance and run pretty slowly"; "Write lots of small and fast unit tests. Write some more coarse-grained tests and very few high-level tests"。
- **Kent C. Dodds, [Write tests. Not too many. Mostly integration.](https://kentcdodds.com/blog/write-tests)** — "Write tests. Not too many. Mostly integration."; "Integration tests strike a great balance on the trade-offs between confidence and speed/expense."
- **Kent C. Dodds, [Static vs Unit vs Integration vs E2E Testing](https://kentcdodds.com/blog/static-vs-unit-vs-integration-vs-e2e-tests)** — 测试金字塔四类: E2E / Integration / Unit / Static 的明确描述; "**The more your tests resemble the way your software is used, the more confidence they can give you.**"
- **Martin Fowler, [On the Diverse And Fantastical Shapes of Testing (2021)](https://martinfowler.com/articles/2021-test-shapes.html)** — "the terms 'unit test' and 'integration test' have always been rather murky"; 解释 honeycomb / trophy / pyramid 分歧源自对 unit 的定义不一致 (solitary vs sociable)。
- **Google Testing Blog, [Test Sizes (Mike Wacker, 2010)](https://testing.googleblog.com/2010/12/test-sizes.html)** — Google 的 small/medium/large 三档分类（页面 fetch 失败未能取得原文；URL 作为权威引用保留）。
- **xUnit Test Patterns (Gerard Meszaros)** — [官网](http://xunitpatterns.com) 当前 404；[O'Reilly 章节](https://www.oreilly.com/library/view/xunit-test-patterns/9780131495050/ch11.html) 需付费访问，无法直接引述原文；本主题建议直接信 Fowler/Vocke 的总结。

---

## 2. ADR 触发阈值

### 推荐判定准则（什么必须写 ADR）

Nygard (2011) 给出的"**architecturally significant**" 判定是核心 trigger：那些影响"structure, non-functional characteristics, dependencies, interfaces, or construction techniques"的决策。落到具体清单：

| 必须写 | 触发理由（Nygard / Microsoft / AWS 共识） |
|---|---|
| 引入新的外部依赖（lib、service、framework） | "dependencies" 是 Nygard 明列；MS Well-Architected: "Only include choices that affect the system's structure, key quality attributes, or are difficult to reverse." |
| 框架/语言 swap | "construction techniques" |
| 公共 API/合约破坏性变更 | "interfaces"；MS: "difficult to reverse" |
| 持久层 schema/引擎变更 | "non-functional characteristics" + "structure" |
| 认证/授权/安全模型变更 | "non-functional characteristics" |
| 跨服务契约引入或变更 | Nygard: "interfaces"; 单独提一条因为影响多个团队 |
| 部署拓扑/可观测性栈变更 | "non-functional characteristics" |

Microsoft Azure Well-Architected 直接说: "Only include choices that affect the system's **structure, key quality attributes, or are difficult to reverse.**"——任何"难逆转"或"碰质量属性"的决策都触发 ADR。

### 不必写（写到 `docs/architecture/` 或代码注释即可）

- 同模块内的命名/重构、行为不变 (refactor-with-no-behavior-change)。
- 单文件 bug fix、错误信息文案调整。
- 测试增补、fixture 调整（除非引入新的测试栈）。
- 现有模块内新增一个 service/handler/file。
- 文档 typo。

### 完全不写

- 单行 typo、注释修正。
- CI 配置调参（timeout、retry count）——除非反映新的部署策略。
- 依赖版本 patch bump（minor 行为不变）。

### 推荐目录

- **首选 `docs/adr/NNNN-title.md`**（四位序号 + kebab-case 标题）。Nygard 原话："We will keep ADRs in the project repository under `doc/arch/adr-NNN.md`. ... ADRs will be numbered sequentially and monotonically. Numbers will not be reused."——但 **adr.github.io / MADR** 生态的事实标准是 `docs/decisions/NNNN-title.md`（MADR README: "Copy it into `docs/decisions`. For each ADR, copy the template to `nnnn-title.md` and adapt."）。
- 与本仓库结构（已有 `docs/`）对齐，**推荐 `docs/adr/NNNN-title.md`**——比 `docs/decisions/` 更精准命名（"decision" 太宽，ADR 是 arch decision），比 Nygard 的 `doc/arch/` 更靠近 `docs/` 既有约定。
- 反向链：superseded 时保留旧文件、加 status + 新 ADR 链接。Nygard: "If a decision is reversed, we will keep the old one around, but mark it as superseded."

### 来源

- **Michael Nygard, [Documenting Architecture Decisions (Cognitect blog, 2011)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html)** — "We will keep a collection of records for 'architecturally significant' decisions: those that affect the **structure, non-functional characteristics, dependencies, interfaces, or construction techniques.**"; "We will keep ADRs in the project repository under doc/arch/adr-NNN.md"; "If a decision is reversed, we will keep the old one around, but mark it as superseded."; ADR 模板字段: Title / Context / Decision / Status / Consequences。
- **[adr.github.io](https://adr.github.io/)** — "An Architectural Decision (AD) is a justified design choice that addresses a functional or non-functional requirement that is **architecturally significant**."; "An Architectural Decision Record (ADR) captures a single AD and its rationale"; ADR 工具与模板的官方索引。
- **[MADR (Markdown ADR) README](https://github.com/adr/madr)** — "Copy it into `docs/decisions`. For each ADR, copy the template to `nnnn-title.md` and adapt."; Y-statement 格式与可选项 (Decision Drivers / Considered Options / Pros and Cons / Confirmation)。
- **AWS, [Architectural Decision Records Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/introduction.html)** — "Three major anti-patterns often emerge when making architectural decisions: No decision is made ... A decision is made without any justification ... The decision isn't captured in an architectural decision repository"; ADR 的业务目标是 "align current and future team members; set a strategic direction; avoid decision anti-patterns"。
- **Microsoft, [Maintain an architecture decision record — Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)** — "Only include choices that affect the system's **structure, key quality attributes, or are difficult to reverse.**"; "The ADR serves as an append-only log. Don't go back and edit accepted records."; 每条需含: Problem statement / Options / Decision outcome (含 tradeoff 与 confidence) / Status。
- **ThoughtWorks Technology Radar** — 检索未发现把 ADR 作为单条 blip 收录（ADR 已在 mainstream，未列为 "new/assess"）；MADR 与 adr.github.io 在 Radar 多期被引。

---

## 3. docs/ 子目录结构

### 推荐布局

```
docs/
  README.md                       # 一页入口，链到各子目录
  stories/<id>.md                 # 用户故事 + AC + Comment；轻量 spec
  adr/NNNN-<title>.md             # 架构决策记录
  architecture/                   # 高层架构图、系统概览
    overview.md
    components.md
    data-model.md
  runbooks/                       # 运维手册：incident、deploy、rollback
    <scenario>.md
  domain/                         # 词汇表 + 关键事实（Diátaxis: reference）
    glossary.md
    facts.md
  assumptions/                    # AssumptionRecord：未验证前提 + 失效信号
    <id>.md
```

**取舍说明**：
- `stories/` 是 spec-driven 的入口（替代 Jira），与 `adr/` 平行——故事改"做什么"，ADR 改"怎么做"。
- `architecture/` vs `adr/`: ADR 是**带时序的决策日志**（为什么选 X 不选 Y），architecture 是**当下系统的描述**（"现在长啥样"）。前者 append-only，后者可被 refactor 重写。
- `assumptions/` 与 `domain/` 分离：assumption 会过期、需要被验证/推翻；domain 是稳定事实。
- Runbooks 单列：与 architecture 在写作语气上完全不同（imperative, step-by-step vs declarative）。

### Diátaxis 映射

| Diátaxis 模式 | 定义（Procida） | 我们用在哪 |
|---|---|---|
| **Tutorials**（"informs action, acquisition of skill"） | "A lesson ... takes a student by the hand through a learning experience." | 新成员 onboarding 的 step-by-step（暂不进 docs/，放在 `docs/architecture/` 或独立 `docs/tutorials/`；MVP 不必建） |
| **How-to guides**（"informs action, application of skill"） | "Addresses a real-world goal or problem, by providing practical directions to help the user who is in that situation." | `runbooks/`（incident response、deploy procedure、rollback） |
| **Reference**（"informs cognition, application of skill"） | "Contains the technical description ... facts ... accurate, complete, reliable information, free of distraction and interpretation." | `domain/glossary.md`、`domain/facts.md`、`architecture/` 的事实性章节（接口表、配置项） |
| **Explanation**（"informs cognition, acquisition of skill"） | "Provide context and background. ... answer the question why?" | `adr/` 全部（每个 ADR 的 Context/Consequences）、`assumptions/`（解释前提的理由） |

Diátaxis compass 的判别公式: "**action or cognition? acquisition or application?**"——`runbooks/` 是 action+application，stories 是 action+acquisition（学员读故事学业务），ADR 是 cognition+acquisition（理解系统为什么这样），domain 是 cognition+application（查事实）。

### docs-as-code 通用约定

- 子目录用名词复数（`runbooks/`、`stories/`、`adr/`），不用动词。
- 文件名 kebab-case：`on-call-handoff.md`，不混用大小写。
- README 作为入口：`docs/README.md` 提供 4–8 行 overview + 链到每个子目录。
- 命名一致性比"漂亮"重要：`docs/decisions/` vs `docs/adr/` vs `docs/architecture/decisions/` 都能工作——一旦选定不改。

### 来源

- **Daniele Procida, [Diátaxis](https://diataxis.fr/)** — 四模式定义: "Diátaxis identifies four distinct needs, and four corresponding forms of documentation - tutorials, how-to guides, technical reference and explanation."
- **Diátaxis [Compass](https://diataxis.fr/compass/)** — 判别表: "If the content … informs action … acquisition of skill → a tutorial"; "informs action … application of skill → a how-to guide"; "informs cognition … application of skill → reference"; "informs cognition … acquisition of skill → explanation".
- **Diátaxis [Start here](https://diataxis.fr/start-here/)** — "Tutorials ... serves acquisition of skill"; "How-to guides ... serves application of skill"; "Reference ... serves the user who is at work, and it's up to the user to be sufficiently competent to interpret and use it correctly"; "Explanation ... serves the user's study"。
- **adr.github.io / MADR** — `docs/decisions/` 路径与文件命名惯例（见 §2 来源）。
- **Nygard (2011)** — `doc/arch/adr-NNN.md`（最早的 ADR 路径范式，见 §2 来源）。

---

## 4. 综合建议（落到 AGENTS.md 的具体规则）

1. **测试分层定义写入 AGENTS.md**（用一句话锁住各层）：
   - UT = "测试运行时**不命中** real network / real DB / real filesystem / real subprocess 的 test"，写代码时可挂 TestDouble。
   - IT = "测试运行时命中 real DB (含 in-memory SQL) / in-process mock server (MSW、WireMock) / testcontainers 的 test"。
   - E2E = "在 staging 或本地 compose 中拉起完整 stack，从 UI 或 over-the-wire REST 驱动的 test"。
   - 把这条加进 AGENTS.md 的"Tests" 段，agent 写新测试时按定义自检。
2. **ADR trigger 写成 checklist**（agent 在 PR description 里勾选；命中任一项就要求 PR 链一份 `docs/adr/NNNN-*.md`）：
   - [ ] 新增/替换外部依赖、框架、运行时？
   - [ ] 持久层/认证/部署拓扑变更？
   - [ ] 公共 API 破坏性变更？
   - [ ] 跨服务契约引入/变更？
   - [ ] 决策"难逆转"或"碰质量属性"？
3. **`docs/` 布局作为不可变约定**：
   - 6 个固定子目录（`stories/`、`adr/`、`architecture/`、`runbooks/`、`domain/`、`assumptions/`）+ `README.md`。
   - AGENTS.md 里只放一句 "Doc layout is fixed; do not create new top-level dirs under `docs/` without updating AGENTS.md"——把 docs/ 拓扑本身当作受控产物。
4. **Diátaxis 用作 review 工具**：agent 写到 `runbooks/` 必须 imperative + step-by-step；写到 `domain/` 必须中性、只列事实；写到 `adr/` 必须含 Nygard 五字段（Title/Context/Decision/Status/Consequences）。在 AGENTS.md 里贴一句 Diátaxis compass 的判别口诀，agent 自查。
5. **来源一致性提示**：Google Testing Blog 的 "Test Sizes" 文章 (2010) 在官方 blogspot 上 fetch 不稳定，引用 URL 但未引述原文；xUnit Patterns (Meszaros) 官网 404、O'Reilly 章节付费墙，本主题以 Fowler/Vocke/Dodds/Nygard/Microsoft/AWS/Diátaxis 为主权威。

---

## 摘要（给上游 AGENTS.md 模板用的三句话）

1. **测试分层定义**：UT 不可触碰 real network/DB/fs/subprocess（命中即降级为 IT）；IT 可命中 in-memory DB、in-process mock server、testcontainers；E2E 必须拉起完整 stack、UI 或 over-the-wire REST 驱动（来源：Fowler bliki、Vocke ThoughtWorks 文章）。
2. **ADR trigger**：决策满足"影响 structure / 关键质量属性 / 难逆转"任一即触发；Nygard 明列 dependencies / interfaces / non-functional / construction techniques 为判断轴。
3. **docs/ 布局**：`docs/{stories,adr,architecture,runbooks,domain,assumptions}/` 六目录固定，新增顶层目录必须先改 AGENTS.md；ADR 用 `NNNN-title.md` 四位序号 + kebab-case，写入 `docs/adr/`，supersede 时保留旧文件加状态。
