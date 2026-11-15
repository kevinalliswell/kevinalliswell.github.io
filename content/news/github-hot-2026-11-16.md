---
title: "GitHub 热点 2026-11-16｜plannotator：用于 AI agent 的本地浏览器审阅台，标注计划、HTML 与 di…"
date: "2026-11-16T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "TypeScript"]
categories: ["日报"]
summary: "今日主推 backnotprop/plannotator（今日 +860 Stars），速览 4 个：univer、misterdownloadmanager、orca 等。"
---

> 今日主推 backnotprop/plannotator（今日 +860 Stars），速览 4 个：univer、misterdownloadmanager、orca 等。

## 今日主推：[backnotprop/plannotator](https://github.com/backnotprop/plannotator)

> 用于 AI agent 的本地浏览器审阅台，标注计划、HTML 与 diff 并一键回传反馈。

⭐ 11,799 · 📈 今日 +860 · 🍴 1,082 · TypeScript · Apache-2.0 · 创建于 2025-12-28

**为什么是今天**

- GitHub Trending 今日 +860 Stars
- 近 2 天 +1,243 Stars
- 近 7 天发布 v0.28.65

**它解决什么问题**

解决 AI coding agent 的计划、文档、HTML artifact 和代码 diff 缺少集中审阅与反馈通道的问题；用户在本地浏览器标注后，可把意见直接发回对应 agent。

**和同类相比**

README 未说明与同类方案的直接对比；特点是本地浏览器审阅 surface，通过 plugins、hooks 和 commands 接入多种 coding agent，并把标注反馈回传原会话。

**适合谁**

适合使用 Claude Code、Codex、Copilot CLI 等 coding agent 并需要审阅计划、HTML 或 diff 的开发者；不适合不愿在本地运行浏览器审阅界面或不使用这些 agent 的用户。

**最短上手**

```bash
plannotator inbox
/plannotator-annotate README.md
/plannotator-review
```

**采用前留意**

项目创建于 2025-12-28，成熟度与长期维护需观察；README 可见部分未完整说明本体安装步骤、系统要求和各 agent 插件配置，采用前需核对官方文档。

官方描述：The workspace to stay in the loop and on top of agents - shape, decide, plan, annotate, review code, share with team, and send all feedback to agents with one click.

Topics：`agents` `claude-code` `code-review` `codex` `obsidian` `opencode` `pi-mono` `plan-mode`

链接：[仓库](https://github.com/backnotprop/plannotator) · [最新 Release](https://github.com/backnotprop/plannotator/releases/tag/v0.28.65) · [Homepage](https://plannotator.ai)

---

## 速览

### 1. dream-num/univer

可扩展的开源Office SDK，支持Sheets/Docs编辑与公式计算

- 指标：⭐ 25,567 · 📈 今日 +1,041 · 🍴 2,333 · TypeScript · Apache-2.0 · 创建于 2022-09-29
- 上榜理由：GitHub Trending 今日 +1,041 Stars；近 7 天发布 v1.5.0
- 适合谁：适合需要在自有产品中嵌入可扩展Sheets/Docs编辑与计算能力的开发团队；不适合期望开箱即用完整Office套件或不愿接入商业Server/AI扩展许可的团队。
- 留意：Apache-2.0许可，但开源范围限于Web SDK核心；商业Web SDK插件、Server SDK和商业AI SDK扩展需单独许可，采用前需确认功能边界与商业成本，README未说明具体依赖和成本细节。
- 链接：[仓库](https://github.com/dream-num/univer) · [最新 Release](https://github.com/dream-num/univer/releases/tag/v1.5.0) · [Homepage](https://univer.ai)

### 2. anefzaoui/misterdownloadmanager

纯 Rust 跨平台开源下载管理器，支持 BT 和浏览器扩展且免费无广告。

- 指标：⭐ 10,317 · 📈 近 24h +767 · 🍴 849 · Rust · GPL-3.0 · 创建于 2026-10-29
- 上榜理由：近 24 小时 +767 Stars；近 2 天 +1,213 Stars；创建 17 天的新项目；近 7 天发布 v0.5.2
- 适合谁：适合需要免费开源、跨平台且带浏览器集成/BT 下载的用户；不适合必须使用成熟稳定 macOS 版或不能接受 GPL-3.0 的用户。
- 留意：采用前需确认 GPL-3.0 对分发和修改的约束，并注意 README 将 macOS 标为实验性；项目成熟度、依赖与安全审计情况 README 未说明。
- 链接：[仓库](https://github.com/anefzaoui/misterdownloadmanager) · [最新 Release](https://github.com/anefzaoui/misterdownloadmanager/releases/tag/v0.5.2) · [Homepage](https://misterdownloadmanager.com)

### 3. stablyai/orca

编排多个 coding agent，支持独立 worktree 和移动端。

- 指标：⭐ 125,722 · 📈 近 24h +695 · 🍴 7,968 · TypeScript · MIT · 创建于 2026-03-17
- 上榜理由：近 24 小时 +695 Stars；近 2 天 +1,224 Stars；近 7 天发布 v1.4.259
- 适合谁：适合需要并行运行 Claude Code、Codex 等 coding agent 并远程跟进的人；不适合只需要轻量本地终端、无需编排与远程协作的人。
- 留意：项目创建于 2026-03-17，较新，成熟度与长期维护需观察；远程服务器、云 VM 和自有 agent 订阅可能带来额外成本，README 未说明具体定价。
- 链接：[仓库](https://github.com/stablyai/orca) · [最新 Release](https://github.com/stablyai/orca/releases/tag/v1.4.259) · [Homepage](https://orca.dev)

### 4. milind-soni/OpenMausBot

开源版 Grok Bot：聊天应用里管理一队本地 AI agent

- 指标：⭐ 23,333 · 📈 近 24h +585 · 🍴 3,239 · TypeScript · Apache-2.0 · 创建于 2026-08-12
- 上榜理由：近 24 小时 +585 Stars；近 7 天发布 v0.1.161
- 适合谁：适合已有 Claude/Codex/Grok CLI 订阅、希望自托管多 agent 的开发者；不适合想要纯云端托管、零配置开箱即用的用户。
- 留意：采用 Apache-2.0 许可；仓库创建于 2026-08-11，README 未说明测试与版本稳定性，成熟度需自行验证。功能依赖本机的 claude/codex/grok CLI、Docker 类隔离环境与 Composio，宿主控制存在平台限制。
- 链接：[仓库](https://github.com/milind-soni/OpenMausBot) · [最新 Release](https://github.com/milind-soni/OpenMausBot/releases/tag/v0.1.161) · [Homepage](https://www.mausbot.com/)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [deepseek-ai/chat-demo](https://github.com/deepseek-ai/chat-demo) | 2,900 | 近 24h +1,179 | 2026-11-15 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 23,727 | 近 24h +1,025 | 2026-11-15 |
| [JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video) | 9,155 | 近 24h +600 | 2026-11-15 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 148,397 | 近 24h +651 | 2026-11-15 |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 33,681 | 近 24h +959 | 2026-11-14 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
