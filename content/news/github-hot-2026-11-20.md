---
title: "GitHub 热点 2026-11-20｜superpowers：用可组合 skills 让 coding agent 按规格、计划与 T…"
date: "2026-11-20T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Shell"]
categories: ["日报"]
summary: "今日主推 obra/superpowers（今日 +2,029 Stars），速览 4 个：app-store-compliance、firecrawl、hermes-agent 等。"
---

> 今日主推 obra/superpowers（今日 +2,029 Stars），速览 4 个：app-store-compliance、firecrawl、hermes-agent 等。

## 今日主推：[obra/superpowers](https://github.com/obra/superpowers)

> 用可组合 skills 让 coding agent 按规格、计划与 TDD 流程开发。

⭐ 322,037 · 📈 今日 +2,029 · 🍴 28,626 · Shell · MIT · 创建于 2025-10-10

**为什么是今天**

- GitHub Trending 今日 +2,029 Stars
- 近 2 天 +2,747 Stars

**它解决什么问题**

它解决 coding agent 容易直接写代码、缺少规格与计划的问题；README 描述其通过 skills 和初始指令引导需求澄清、设计审阅、实施计划与 subagent 执行。

**和同类相比**

特点是把软件开发方法论拆成可组合且自动触发的 skills，并用 subagent-driven-development 逐任务审查；README 未说明与同类方案的具体对比。

**适合谁**

适合使用受支持 coding agent、希望用结构化流程约束 agent 的开发者或团队；不适合不需要该流程或使用未支持 harness 的人。

**最短上手**

```bash
/plugin install superpowers@claude-plugins-official
```

**采用前留意**

License 为 MIT；仓库创建于 2025-10-09，README 未说明稳定版本与发布周期，且需按 harness 分别安装。README 目录提到 Visual companion telemetry，但截断内容未说明具体范围。

官方描述：An agentic skills framework & software development methodology that works.

Topics：`ai` `brainstorming` `coding` `obra` `sdlc` `skills` `subagent-driven-development` `superpowers`

链接：[仓库](https://github.com/obra/superpowers) · [最新 Release](https://github.com/obra/superpowers/releases/tag/v7.0.2)

---

## 速览

### 1. mjmirza/app-store-compliance

开源商店拒审手册与预提交扫描，提前拦截 iOS/Android 风险。

- 指标：⭐ 1,790 · 📈 今日 +542 · 🍴 124 · Shell · 创建于 2026-06-06
- 上榜理由：GitHub Trending 今日 +542 Stars；近 7 天发布 v2.4.0
- 适合谁：适合准备提交 iOS/Android 应用的开发者、非开发合规人员以及使用 AI coding agent 的团队；不适合需要成熟商业合规审计或不涉及应用商店提交的团队。
- 留意：仓库信息标注许可证未声明，README 显示 OpenRoots ORA 2.3 徽章，商用前需核对授权条款；项目创建时间较新，规则与截止日期应回到 Apple/Google 官方来源复核。
- 链接：[仓库](https://github.com/mjmirza/app-store-compliance) · [最新 Release](https://github.com/mjmirza/app-store-compliance/releases/tag/v2.4.0) · [Homepage](https://mjmirza.github.io/app-store-compliance/)

### 2. firecrawl/firecrawl

为 AI agent 提供网页抓取、爬取与映射能力的开源知识基础设施，本地可跑。

- 指标：⭐ 204,143 · 📈 今日 +795 · 🍴 10,696 · TypeScript · AGPL-3.0 · 创建于 2024-04-16
- 上榜理由：GitHub Trending 今日 +795 Stars；近 3 天 +1,798 Stars
- 适合谁：适合需要给 AI agent 接入网页抓取/MCP、并希望本地运行或自托管的开发者；不适合只想零运维使用全部云端功能或无法接受 AGPL-3.0 的团队。
- 留意：AGPL-3.0 对分发和网络服务使用有约束；Local 默认会把本地加载失败的单页抓取回退到 Firecrawl Cloud（可用 FIRECRAWL_CLOUD=off 关闭），JS 渲染依赖本机 Chrome/Chromium、MCP 依赖 Node.js 22+，完整 self-hosting 还需维护队列、worker 和数据库。
- 链接：[仓库](https://github.com/firecrawl/firecrawl) · [最新 Release](https://github.com/firecrawl/firecrawl/releases/tag/v2.11.0) · [Homepage](https://firecrawl.dev)

### 3. NousResearch/hermes-agent

自改进的开源 AI agent，内置学习闭环，可常驻云端并跨消息平台对话

- 指标：⭐ 264,744 · 📈 近 24h +258 · 🍴 59,798 · Python · MIT · 创建于 2025-07-23
- 上榜理由：近 24 小时 +258 Stars；近 6 天 +1,486 Stars；近 7 天发布 v0.23.2
- 适合谁：适合希望长期常驻、跨 Telegram/Slack 等平台使用并愿意自托管云环境或沙箱的开发者与研究者；不适合只需本地一次性脚本调用或不接受维护云资源的用户。
- 留意：MIT 许可，但仓库创建于 2025-07，项目非常年轻，README 未说明版本稳定性与兼容性承诺；使用需承担模型 API 费用及 VPS/沙箱成本，安装脚本会自带并管理 Python 3.14、Node.js、uv 等依赖。
- 链接：[仓库](https://github.com/NousResearch/hermes-agent) · [最新 Release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.23.2) · [Homepage](https://hermes-agent.nousresearch.com)

### 4. cheaper-inference/OmniRoute

免费 MIT AI gateway，一个 endpoint 聚合多 provider 并支持自动回退

- 指标：⭐ 88,931 · 📈 近 24h +254 · 🍴 13,739 · TypeScript · MIT · 创建于 2026-02-13
- 上榜理由：近 24 小时 +254 Stars；近 6 天 +1,706 Stars；近 7 天发布 v3.8.54
- 适合谁：适合已有多家 provider 账号、想在 Claude Code/Cursor/Cline 等工具中统一接入并利用免费额度的开发者；不适合要求稳定 SLA、或不愿处理第三方账号与条款的人。
- 留意：免费额度来自第三方 provider，配额、可用性和条款由各 provider 控制，README 也说明数字会上下变动；项目创建于 2026-02-13、迭代较快，稳定性需自行验证，许可证为 MIT。
- 链接：[仓库](https://github.com/cheaper-inference/OmniRoute) · [最新 Release](https://github.com/cheaper-inference/OmniRoute/releases/tag/v3.8.54) · [Homepage](https://omniroute.online)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything) | 5,097 | 近 24h +1,812 | 2026-11-19 |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 38,419 | 近 24h +1,470 | 2026-11-14 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 28,157 | 近 24h +1,008 | 2026-11-15 |
| [stablyai/orca](https://github.com/stablyai/orca) | 129,843 | 近 24h +1,004 | 2026-11-16 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 70,762 | 今日 +952 | 2026-11-18 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
