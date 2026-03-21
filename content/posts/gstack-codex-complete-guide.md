---
title: "gstack + Codex 完全使用指南：把 Codex 变成你的 AI 工程团队"
date: 2026-03-21T14:20:00+08:00
draft: false
tags: ["gstack", "Codex", "AI Agent", "Claude Code", "开发效率", "教程"]
categories: ["技术"]
author: "Kevin"
description: "从零开始安装、配置和使用 gstack，让 Codex 获得更强的产品拆解、代码审查、浏览器 QA 和发版协作能力。"
---

> 适用对象：正在使用 Codex 做编程协作、想把 AI 从“写几段代码”升级为“完整开发流程搭子”的个人开发者。  
> 基于仓库状态：`garrytan/gstack`，截至 2026-03-21 本地分析结果。  
> 难度：⭐⭐⭐  
> 预计阅读时间：20 分钟

---

## 先说结论

**gstack 不是另一个 AI 模型。**

它更像一套装在本地的 **AI 工程工作流系统**：

- 让 AI 在开工前先帮你做产品拆解
- 让 AI 在写完代码后做更像样的 code review
- 让 AI 打开真实浏览器做 QA，而不只是“读代码猜页面”
- 让 AI 在发版前补测试、补文档、补流程

如果你已经在用 Codex 写代码，那么 gstack 带来的提升主要不是“更聪明”，而是：

1. **更会想问题**
2. **更会做检查**
3. **更会走完整流程**
4. **更不容易漏掉关键环节**

一句话理解：

> **Codex 提供模型能力，gstack 提供团队化工作流。**

---

## gstack 到底是什么

官方把它定义成一个 “software factory”。

简单讲，它做了两件事：

### 1. 提供一组角色化技能

比如：

- `/office-hours`：像产品顾问一样，先帮你想清楚需求
- `/plan-eng-review`：像技术负责人一样，收紧架构和测试
- `/review`：像高级工程师一样，审查代码风险
- `/qa`：像 QA 一样，在真实浏览器里点击和验证
- `/ship`：像发布工程师一样，帮你收口、发版、补文档

这不是几个零散 prompt，而是一套有顺序的开发链路：

**Think -> Plan -> Build -> Review -> Test -> Ship**

### 2. 提供真实底层能力

最关键的是它的 `browse`：

- 常驻 Chromium
- 保持登录态、Cookie、标签页状态
- 让 AI 可以持续操作页面
- 支持截图、点击、填表、导入浏览器 Cookie
- 遇到验证码或 MFA 时还能 handoff 给真人接管，再恢复给 AI

所以 gstack 的价值不只是“会说”，而是“能做”。

---

## 它能不能本地部署

**可以，而且默认就是本地部署。**

它不是 SaaS 控制台，也不是你要部署到云上的服务。

你安装之后，核心东西会落在本地：

- 全局技能目录：`~/.codex/skills/gstack`
- 全局 Codex 配置：`~/.codex/AGENTS.md`
- 本地状态目录：`~/.gstack/`
- 项目级技能目录：`.agents/skills/`
- 项目级配置文件：`AGENTS.md`

也就是说，它的运行模型是：

1. 你本机安装 gstack
2. Codex 发现这些技能
3. 在你的代码仓库里调用这些技能
4. 浏览器、配置、日志、缓存大都存在你自己的机器上

对于个人开发者，这个模式有几个明显好处：

- 数据更可控
- 可以接本地项目、localhost、内网页面
- 可以配合你自己的 Git、浏览器、终端环境
- 不需要搭一套额外后端

---

## gstack 能不能增强 Codex 的编程能力

答案是：**能增强工作流能力，不能直接增强模型本体智商。**

这是很多人第一次接触时最容易搞混的地方。

### 它不能做的

- 不能把 Codex 模型直接升级成另一个模型
- 不能让模型“参数更多”
- 不能凭空提高模型的理论推理上限

### 它能做的

它能让 Codex：

1. **在写代码前先做更完整的需求和架构思考**
2. **在写完代码后做更系统的代码审查**
3. **在 Web 项目里直接操作浏览器做 QA**
4. **在发版时把测试、文档、检查流程补全**
5. **在个人开发时模拟一个小型工程团队的协作顺序**

所以如果你平时已经感觉：

- “Codex 会写，但经常方向跑偏”
- “修完 bug 不知道还有没有别的坑”
- “页面逻辑只能靠我自己手点”
- “文档和测试总是最后忘了补”

那 gstack 是能明显帮上忙的。

---

## 全局配置和工作空间配置的区别

这是最重要的一个概念，建议先搞清楚。

### 一、全局配置

放在你家目录下：

```bash
~/.codex/AGENTS.md
~/.codex/skills/
```

适合存放：

- 你个人通用的使用偏好
- 你长期都想启用的技能
- 你在所有项目里都希望 Codex 遵守的规则

比如：

- 优先使用中文解释
- 遇到大改动先做计划
- 默认先 review 再改
- 全局安装 gstack 技能

### 二、工作空间配置

放在具体项目仓库里：

```bash
AGENTS.md
.agents/skills/
```

适合存放：

- 这个项目特有的约束
- 测试命令
- 项目目录结构说明
- 是否必须跑某些检查
- 团队共享的工作规范

### 最佳实践

我建议这样分层：

- **全局 AGENTS**：写你的个人习惯
- **项目 AGENTS**：写项目规则
- **全局安装 gstack**：让所有项目可用
- **需要团队共享时，再把 gstack 放进项目 `.agents/skills`**

简单讲：

> 个人偏好放全局，项目规则放仓库。

---

## 安装前准备

在 Codex 环境里使用 gstack，建议你先确认下面几件事。

### 1. 安装 Bun

如果你的机器还没有 `bun`，先安装：

```bash
curl -fsSL https://bun.sh/install | bash
```

安装后重开终端，确认：

```bash
bun --version
```

### 2. 确认 Git 可用

```bash
git --version
```

### 3. 确认 Codex 已安装

```bash
codex --help
```

### 4. 预留 Playwright/Chromium 安装时间

首次 `setup` 时，gstack 会检查并安装浏览器依赖。

---

## 最推荐的安装方式：全局安装给 Codex 用

这是最适合个人开发者的方案。

### 第一步：克隆到全局技能目录

```bash
git clone https://github.com/garrytan/gstack.git ~/.codex/skills/gstack
```

### 第二步：运行安装脚本

```bash
cd ~/.codex/skills/gstack
./setup --host codex
```

这个命令会做几件事：

1. 检查 `bun`
2. 构建 `browse` 二进制
3. 检查或安装 Playwright Chromium
4. 把 Codex 版技能链接到 `~/.codex/skills`
5. 准备好运行时依赖

### 第三步：确认技能目录

你应该能看到类似目录：

```bash
~/.codex/skills/gstack
~/.codex/skills/gstack-review
~/.codex/skills/gstack-qa
~/.codex/skills/gstack-office-hours
...
```

---

## 项目级安装什么时候需要

如果只是你自己一个人用，**全局安装就够了**。

只有在下面场景下，才建议做项目级安装：

- 你想把 gstack 跟着仓库一起提交
- 你希望团队成员 clone 项目后也能直接使用
- 你要为这个项目定制一套更强的工作流

项目级安装思路是把技能放进：

```bash
.agents/skills/
```

这样它会随着仓库一起走。

---

## 给 Codex 配 AGENTS：最小可用版本

### 全局 `~/.codex/AGENTS.md` 推荐内容

下面是一版适合个人开发者的最小配置思路：

```md
## gstack

Use gstack skills when they fit the task.

- For new ideas or features, prefer `/office-hours` first.
- For implementation planning, prefer `/plan-eng-review`.
- For code changes before merge, prefer `/review`.
- For web app validation, prefer `/qa`.
- For bug root-cause analysis, prefer `/investigate`.

When a task is substantial, think in this order:
idea -> plan -> implement -> review -> test
```

这段配置的目的不是“强制每次都跑全流程”，而是让 Codex 在合适的时候优先想到这些技能。

### 项目里的 `AGENTS.md` 应该写什么

更建议写这些项目信息：

- 技术栈
- 启动命令
- 测试命令
- 构建命令
- 哪些目录是核心目录
- 哪些操作必须先 review

比如：

```md
## Testing

- Backend tests: `pytest`
- Frontend tests: `pnpm test`
- Build: `pnpm build`

## Project Rules

- Always update docs when public behavior changes.
- Run review before final delivery.
- For UI changes, run QA against local or staging URL.
```

---

## 建议你先启用的 4 个技能

如果你是个人开发者，不要一上来全用。

我最推荐先掌握下面 4 个：

### 1. `/office-hours`

适合：

- 新想法
- 新功能
- 不确定值不值得做
- 方向有点散的时候

它最大的价值是：

**帮你先想清楚“真正要解决的问题是什么”。**

很多时候你以为你要做的是一个功能，实际上你要做的是一个更大的用户结果。

### 2. `/plan-eng-review`

适合：

- 开工前把架构和边界想明白
- 列出测试点
- 提前暴露风险

它最大的价值是：

**帮你在写代码前，减少返工。**

### 3. `/review`

适合：

- 做完一轮开发之后
- 准备合并前
- 想查查有没有生产风险

它最大的价值是：

**给你一个更像“高级工程师审 diff”的视角。**

### 4. `/qa`

适合：

- Web 项目
- 表单流程
- 登录流程
- 页面交互验证
- 真实浏览器回归测试

它最大的价值是：

**让 AI 真正去点页面，而不是只看代码猜测页面行为。**

---

## 个人开发者最推荐的工作流

下面是我最推荐的轻量链路。

## 场景一：做一个新功能

```text
/office-hours
-> /plan-eng-review
-> 实现功能
-> /review
-> /qa
```

### 什么时候用

- 你要加一个完整功能
- 改动会跨多个文件
- 涉及产品体验、页面流程、接口设计

### 为什么这样排

因为个人开发最怕两件事：

1. 一开始方向错
2. 做完后没人替你兜底检查

这个链路正好补这两个坑。

---

## 场景二：修一个 bug

```text
/investigate
-> 修复
-> /review
-> 如果是 Web 问题再 /qa
```

### 为什么先 investigate

因为很多 bug 的第一反应是“先改一把试试”，但这很容易把问题越修越乱。

`/investigate` 的价值是：

- 先找根因
- 先验证猜想
- 降低误修

---

## 场景三：纯后端或脚本项目

如果你不怎么做前端页面，建议主用：

```text
/office-hours
-> /plan-eng-review
-> 实现
-> /review
```

这时 `/qa` 的优先级就没那么高，`/investigate` 会更实用。

---

## `browse` 为什么是 gstack 的核心能力

很多 AI 工具都能“说自己会 QA”，但 gstack 的区别在于它有持续浏览器状态。

这意味着：

- 不是每一步都重新启动浏览器
- 登录后能保持登录态
- 标签页不会丢
- Cookie 不会丢
- 多步交互可以持续推进

### 实际能做什么

比如让 AI：

- 打开你的本地站点
- 登录后台
- 点击某个按钮
- 填表并提交
- 截图
- 检查报错
- 对比修改前后行为

这比“只让 AI 读代码再猜页面表现”强太多了。

---

## 首次使用时我建议你这样练手

不要直接拿它做最复杂的项目，先做一次小型演练。

### 演练 1：审查一个已有改动

在有改动的仓库里对 Codex 说：

```text
请使用 /review 检查我当前分支的改动，重点关注生产风险、边界情况和遗漏的测试。
```

### 演练 2：检查一个本地页面

先把项目跑起来，比如：

```bash
pnpm dev
```

然后对 Codex 说：

```text
请使用 /qa 测试 http://localhost:3000 ，优先检查首页、主导航、登录流程和主要表单。
```

### 演练 3：开一个新功能前先做需求拆解

```text
我想做一个日报自动生成工具，请使用 /office-hours 帮我先拆清楚到底应该做什么。
```

这样你会非常快地感受到它和裸 prompt 的差异。

---

## 它和普通 Prompt 使用方式的区别

很多人刚装好 gstack，会继续像以前一样说：

```text
帮我加个功能
```

这样当然也能用，但价值没有完全发挥出来。

gstack 更适合这种说法：

```text
先用 /office-hours 帮我把这个想法收敛清楚。
```

或者：

```text
我已经实现完了，请用 /review 做一次正式审查。
```

或者：

```text
请用 /qa 在真实浏览器里帮我验证这个页面流程。
```

也就是说，**你要学会“调角色”而不是只“下需求”。**

---

## 常见问题

## 1. 为什么我在 Codex 里看不到 `/codex` 技能

这是正常的。

`/codex` 这个技能本来是给 Claude 去调用 Codex CLI 做第二意见的。

如果你已经在 Codex 里运行 gstack，再暴露 `/codex` 就会出现递归语义，所以 Codex 版输出会把它排除。

简单理解：

- 在 Claude 里，`/codex` 是“找 OpenAI Codex 来做第二审查”
- 在 Codex 里，你自己已经在 Codex 里面了，所以这个技能没必要继续套娃

## 2. 它适不适合所有项目

不适合。

最适合的是：

- Web 应用
- SaaS
- 全栈个人项目
- 有明确 review / QA / 发版过程的项目

不太适合的是：

- 一次性小脚本
- 极轻量 demo
- 几分钟就能写完的 throwaway code

## 3. 会不会太重

会，如果你每个小改动都跑完整流程。

正确姿势是：

- 大功能：全流程
- 小修复：`/investigate` + `/review`
- 页面验证：只跑 `/qa`

按任务大小来选技能，不要机械全跑。

## 4. 安装失败怎么办

优先检查：

1. `bun` 是否安装成功
2. `codex` 是否在 PATH 中
3. `./setup --host codex` 是否报浏览器依赖错误
4. Playwright Chromium 是否下载完成

常用检查命令：

```bash
bun --version
codex --help
cd ~/.codex/skills/gstack && ./setup --host codex
```

---

## 个人开发者的最终推荐配置

如果你只想要一个够用、不过重的版本，我建议这样：

### 全局安装

```bash
git clone https://github.com/garrytan/gstack.git ~/.codex/skills/gstack
cd ~/.codex/skills/gstack
./setup --host codex
```

### 全局 AGENTS 放最小偏好

- 新功能优先 `/office-hours`
- 开工前优先 `/plan-eng-review`
- 代码完成后优先 `/review`
- Web 改动优先 `/qa`

### 日常只记住三条

1. **新功能别急着写，先拆**
2. **写完别急着交，先 review**
3. **页面别只靠眼睛看，先 QA**

这三条执行好，gstack 对个人开发的价值就已经很高了。

---

## 一句话总结

如果说 Codex 是一个很强的 AI 工程师，

那么 gstack 做的事情就是：

**给这个工程师补上产品经理、技术负责人、QA 和发布工程师的工作流。**

它不会神奇地把模型变成另一个模型，
但它会让你和模型的协作方式，从“想到什么问什么”，升级到“按团队流程稳定产出”。

对个人开发者来说，这种提升往往比单纯多一点代码生成速度更有价值。
