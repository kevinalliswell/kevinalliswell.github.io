---
title: "代码不再是源头：从 Vibe Coding 到 Spec-Driven Development"
date: 2026-04-01T12:00:00+08:00
draft: false
tags: ["AI", "Spec-Driven Development", "Claude Code", "Vibe Coding", "开发范式"]
categories: ["技术"]
author: "Kevin"
description: "当 GitHub 说'意图才是真正的源代码'，当 Karpathy 说'99% 的时间你不再直接写代码'，一场开发范式的历史性转折正在发生。"
---

> 当 GitHub 宣布"我们正在从'代码是真理之源'走向'意图是真理之源'"时，一个新时代的大门已经打开。

---

## 引子：一条推文引发的范式讨论

2025 年 2 月，Andrej Karpathy 在 X 上随手发了一条推文：

> "There's a new kind of coding I call **vibe coding**, where you fully give in to the vibes, embrace exponentials, and forget that the code even exists."
>
> —— Andrej Karpathy, 2025.02

他后来说这只是"洗澡时的随想"。但这条推文像一根火柴扔进了干柴堆——"Vibe Coding"被 Collins 英语词典评为 **2025 年度词汇**，Merriam-Webster 将其列为"slang & trending"。

它之所以引爆，是因为它精准命名了无数开发者已经在经历但说不出口的东西：**我们写代码的方式，正在被根本性地改变。**

但 Vibe Coding 只是开篇。真正的故事，是从"写代码"到"写规则"的范式迁移。

---

## 数据先说话：AI 写了多少代码？

在讨论范式之前，先看几组数据：

| 来源 | 数据 | 时间 |
|------|------|------|
| Satya Nadella（Microsoft CEO） | Microsoft 30-40% 的代码由 AI 生成 | 2025.04 |
| Sundar Pichai（Google CEO） | Google 30%+ 的代码由 AI 辅助生成 | 2025 Q1 |
| Dario Amodei（Anthropic CEO） | "Anthropic 内部有工程师已经不写任何代码了" | 2026 WEF |
| GitHub 官方 | Copilot 用户中 46% 的代码由 AI 生成，Java 开发者达 61% | 2025 |
| DX Q4 2025 报告 | 22% 的合并代码是 AI 编写的 | 2025 Q4 |

> "No one thought that AI will go and make coding easy."
>
> —— Satya Nadella

Fortune 100 企业中 **90%** 已采用 GitHub Copilot，付费订阅用户达 **470 万**。AI 编程工具市场规模在 2025 年达到 **73.7 亿美元**，其中 GitHub Copilot 占 42% 的市场份额。

这些数字指向一个事实：AI 已经不是"辅助写代码"，而是在**接管写代码本身**。

那问题来了——**如果 AI 写代码，人类写什么？**

---

## 答案：写规则

### 从"代码是源头"到"意图是源头"

2025 年，GitHub 开源了 **Spec Kit**，一个结构化的 Spec-Driven Development 工具包。在官方博客中，GitHub 写下了一句极具历史感的话：

> "We're moving from **'code is the source of truth'** to **'intent is the source of truth.'**"
>
> —— GitHub Blog, 2025

这句话值得反复读。它不是在说"AI 帮你写代码更快了"，而是在说——**代码本身不再是最重要的产出物，你的意图、规范和约束才是。**

Spec Kit 把开发流程拆成四个阶段：**Specify → Plan → Tasks → Implement**。它引入了 `constitution.md`——一份不可变的项目宪法，定义了项目的根本原则。

### 每个主流工具都在做同一件事

如果你关注 AI 编程工具的动态，你会发现一个惊人的趋同：**每家都在让你往项目里放一个 Markdown 文件，告诉 AI 该怎么干活。**

| 工具 | 规则文件 | 发布方 |
|------|---------|--------|
| Claude Code | `CLAUDE.md` + `.claude/rules/` | Anthropic |
| Cursor | `.cursorrules` / `.cursor/rules/` | Cursor |
| Windsurf | `.windsurf/rules/` | Codeium |
| GitHub Copilot | `copilot-instructions.md` | GitHub/Microsoft |
| GitHub Spec Kit | `constitution.md` | GitHub |
| AWS Kiro | 内置 spec 工作流 | AWS |

**这不是巧合，这是趋势。** 当所有主流工具不约而同地走向同一个方向，说明这个方向是对的。

---

## 深入案例：两个值得研究的项目

### 案例一：Garry Tan 的 gstack —— 一个人 = 一支工程团队

Y Combinator CEO Garry Tan 在 2026 年 3 月开源了 **gstack**，一个把 Claude Code 变成"虚拟工程团队"的工具集。

核心理念：**流程大于工具。**

gstack 包含 23 个专业技能（Skills），覆盖完整的开发冲刺周期：

```
Think → Plan → Build → Review → Test → Ship → Reflect
```

每个技能对应一个角色：CEO（`/office-hours`）、工程经理（`/plan-eng-review`）、设计师（`/design-consultation`）、QA（`/qa`）、安全官（`/cso`）、发布经理（`/land-and-deploy`）……

**成果数据**：Tan 在 60 天内生成了 **60 万+行代码**（35% 是测试），日均 1-2 万行，同时他还在全职运营 Y Combinator。

他的关键洞察是：

> 没有流程结构，多个 AI Agent 会制造混乱；有了流程结构，它们会倍增生产力。

gstack 的 "Conductor" 并行编排器允许同时运行 **10-15 个独立冲刺**——因为规则和结构（而非人手敲键盘）在维持质量和一致性。

来源：[github.com/garrytan/gstack](https://github.com/garrytan/gstack)

### 案例二：CLAUDE.md 的解剖 —— 你最高杠杆的文件

Daily Dose of Data Science 的一篇文章 [Anatomy of the Claude Folder](https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder) 详细解析了 Claude Code 的配置体系：

**两层架构**：
- **项目级** `./project/.claude/` —— 提交到 Git，团队共享
- **全局级** `~/.claude/` —— 个人偏好，本地生效

**核心组件**：

| 组件 | 作用 |
|------|------|
| `CLAUDE.md` | 项目宪法：编码规范、架构决策、命名约定 |
| `rules/` | 模块化指令，支持按文件路径激活 |
| `commands/` | 自定义斜杠命令 |
| `skills/` | 自触发工作流（满足条件自动激活） |
| `agents/` | 专业子代理（独立人格、模型、工具权限） |
| `settings.json` | 权限控制（允许/拒绝列表） |

文章的核心结论：

> "**CLAUDE.md is your highest-leverage file. Get that right first. Everything else is optimization.**"

翻译过来就是：CLAUDE.md 是你整个项目中杠杆最高的文件。先把它写好，其他都是优化。

这句话本身就是新范式的最佳注脚——**最重要的不是代码文件，而是规则文件。**

---

## 从 Vibe Coding 到 Agentic Engineering

Karpathy 本人也在进化。到 2025 年底 / 2026 年初，他提出了一个更精确的术语：**Agentic Engineering**（代理工程）。

> "Agentic, because the new default is that you are not writing the code directly 99% of the time, you are **orchestrating agents** who do and acting as oversight. Engineering, to emphasize the art, science, and expertise involved."
>
> —— Andrej Karpathy, 2026

他还指出了一个关键时间节点：

> "It is hard to communicate how much programming has changed due to AI in the last 2 months... coding agents basically didn't work before December (2025)."

Simon Willison（Django 联合创作者）在此基础上进一步区分了 **八种** AI 辅助编程模式，强调专业开发与随性的 Vibe Coding 有本质区别。

ThoughtWorks 的刘尚奇则正式定义了 **Spec-Driven Development（SDD）**：

> "一种以精心设计的软件需求规格说明作为 AI 编码代理提示词的开发范式。它将规划与实现分离，要求在代码生成前完成形式化的规格说明。"

**范式演进的时间线**：

```
2025.02  Vibe Coding（Karpathy）—— 随性编程，拥抱直觉
    ↓
2025 中  Spec-Driven Development（GitHub/ThoughtWorks）—— 规格先行，结构化开发
    ↓
2025 末  Agentic Engineering（Karpathy）—— 编排代理，充当监督
    ↓
2026     Rules as Code（gstack/CLAUDE.md 生态）—— 规则即产品，流程即代码
```

---

## AWS Kiro：大厂的回应

如果说 gstack 是个人开发者的极限实验，那么 AWS 的 **Kiro** 则代表了大厂对这一范式的正式回应。

2025 年 7 月，AWS 在 Summit NYC 发布了 Kiro——一个基于 Code OSS 的**全代理 IDE**，原生实现了 Spec-Driven Development。

**Kiro 的工作流**：
1. 开发者用自然语言描述需求
2. Kiro 自动生成用户故事 + 验收标准
3. 生成技术设计文档
4. 拆分任务列表
5. 逐步实现

Kiro 还引入了 **Agent Hooks**——一个事件驱动的自动化框架，监控文件系统变化并触发 AI 动作（安全扫描、代码风格检查、测试套件生成）。

来源：[kiro.dev](https://kiro.dev/)

---

## 冷思考：这条路的风险

任何范式转变都不会一帆风顺。以下是值得警惕的问题：

### 1. 规格漂移与幻觉

ThoughtWorks 的刘尚奇警告：

> "Spec drift and hallucination are inherently difficult to avoid. We still need highly deterministic CI/CD practices to ensure software quality and safeguard our architectures."

规格会漂移，AI 会幻觉。确定性的 CI/CD 实践仍然不可或缺。

### 2. 同一个 Prompt，十种结果

对同一个规格跑十次，可能得到十种不同的实现。AI 会用不同方式填充未指定的细节。**规格越模糊，结果越不可控。**

### 3. 调试瓶颈转移

Vibe Coding 把瓶颈从"创造"转移到了"调试"。当 AI 卡住时，它经常"无意义地循环——添加新的 debug logger 或重构测试运行器作为毫无意义的忙碌工作。"

### 4. 大胆预测的保质期

Daring Fireball 的 John Gruber 把 Amodei"AI 将在 6 个月内写 90% 代码"的预测标记为 **"claim chowder"**（需要回头验证的大胆声明）。Cal Newport 也在文章 *"Why Didn't AI Join the Workforce in 2025?"* 中指出，AI Agent 的实际影响远落后于预期。

### 5. 规格还是代码，谁是最终产物？

一个尚未解决的根本问题：**当规格和代码发生冲突时，以谁为准？** 如果代码是从规格生成的，但运行中发现需要改动代码，改动是否需要回溯到规格？这个工作流还没有成熟的答案。

---

## 对开发者意味着什么？

### 角色转变

| 旧范式 | 新范式 |
|--------|--------|
| 写代码 | 写规格和约束 |
| Debug 代码 | 审查 AI 产出 |
| 学习语法和框架 | 学习如何精确表达意图 |
| 个人编码技巧 | 编排和监督能力 |
| 代码是核心产出 | 规则文件是核心产出 |

### 新的核心技能

1. **规格写作能力** —— 清晰、无歧义地描述你要什么
2. **架构思维** —— AI 能写实现，但架构决策仍需人类
3. **审查能力** —— 快速评估 AI 产出的质量和安全性
4. **流程设计** —— 像 gstack 那样设计 Agent 的工作流程
5. **领域知识** —— AI 无法替代你对业务场景的理解

### 一个类比

如果说传统开发者是**手工匠人**，那新范式下的开发者更像**建筑师 + 质检员**：你画图纸（规格），定标准（规则），监督施工（Agent），验收成果（Review）。

你不需要亲手砌每一块砖，但你需要确保每一块砖都砌在正确的位置。

---

## 总结

回到开头那句话：

> "We're moving from 'code is the source of truth' to 'intent is the source of truth.'"

这不是未来时，是现在进行时。

1. **数据已经说明一切** —— 主流科技公司 30-40% 的代码由 AI 生成，且比例在单调递增
2. **工具已经趋同** —— 从 CLAUDE.md 到 .cursorrules 到 constitution.md，每家都在让你写规则
3. **先行者已经验证** —— Garry Tan 一个人用规则驱动的方式 60 天产出 60 万行代码
4. **但风险也真实存在** —— 规格漂移、幻觉、调试瓶颈、工作流不成熟

**开发的新范式不是"不写代码"，而是"把写代码的权力交给 AI，把定义规则的权力留给自己"。**

---

## 参考资源

- [Andrej Karpathy - Vibe Coding 原推](https://x.com/karpathy/status/1886192184808149383)
- [Andrej Karpathy - 2025 LLM Year in Review](https://karpathy.bearblog.dev/year-in-review-2025/)
- [GitHub Blog - Spec-Driven Development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [GitHub Spec Kit](https://github.com/github/spec-kit)
- [Garry Tan - gstack](https://github.com/garrytan/gstack)
- [Daily Dose of DS - Anatomy of the Claude Folder](https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder)
- [AWS Kiro](https://kiro.dev/)
- [ThoughtWorks - Spec-Driven Development](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
- [Martin Fowler - SDD 工具分析](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)
- [Simon Willison - Not all AI-assisted programming is vibe coding](https://simonwillison.net/2025/Mar/19/vibe-coding/)
- [RedMonk - Vibe Coding vs Spec-Driven](https://redmonk.com/rstephens/2025/07/31/spec-vs-vibes/)
- [Cal Newport - Why Didn't AI Join the Workforce in 2025?](https://calnewport.com/why-didnt-ai-join-the-workforce-in-2025/)

---

> 本文综合整理自官方文档、技术博客和行业分析，引用均已标注来源。观点仅代表个人理解，欢迎讨论。
