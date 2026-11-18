---
title: "GitHub 热点 2026-11-19｜rust-anything：以录制回放校验逐步迁移到 Rust 的迁移工具，降低重写风险。"
date: "2026-11-19T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Rust"]
categories: ["日报"]
summary: "今日主推 erkamyaman/rust-anything（近 24h +2,120 Stars），速览 4 个：Claude-BugHunter、paper-orchestra、ECC 等。"
---

> 今日主推 erkamyaman/rust-anything（近 24h +2,120 Stars），速览 4 个：Claude-BugHunter、paper-orchestra、ECC 等。

## 今日主推：[erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything)

> 以录制回放校验逐步迁移到 Rust 的迁移工具，降低重写风险。

⭐ 3,285 · 📈 近 24h +2,120 · 🍴 257 · Rust · MIT · 创建于 2026-11-16

**为什么是今天**

- 近 24 小时 +2,120 Stars
- 创建仅 2 天的新项目
- 近 7 天发布 v1.5.1

**它解决什么问题**

它解决把已有 TypeScript、Python、C、Go、Ruby、Java 的 CLI、HTTP server 或库逐步重写为 Rust 时，如何持续验证新实现与原实现行为一致的问题。

**和同类相比**

特点是先录制原应用行为，再生成 Rust crate 与 wrapper，并通过 diff 回放和 gate 检查后才继续迁移，调用方可保留原 API；README 未说明与具体同类方案的直接对比。

**适合谁**

适合已有上述语言项目、需要按模块或 hot path 迁移到 Rust 并用行为回放证明一致的团队；不适合无法在隔离副本中运行原代码或只想要全自动重写的人。

**最短上手**

```bash
cargo install rust-anything
rust-anything setup
```

**采用前留意**

MIT 许可证。主要风险在于 record/app record 会真实执行原代码，可能写文件、访问数据库或网络，需在项目副本、测试数据库且无生产凭据的环境中运行；diff/gate 只能校验录制覆盖到的行为，项目创建于 2026-11-16，成熟度需自行评估。

官方描述：Rewrite your whole app in Rust, one piece at a time, checked against the original's recorded behavior at every step. CLIs, HTTP servers and libraries in TypeScript, Python, C, Go, Ruby and Java.

Topics：`agent-skills` `claude-code` `cli` `code-migration` `codex` `ffi` `golang` `java`

链接：[仓库](https://github.com/erkamyaman/rust-anything) · [最新 Release](https://github.com/erkamyaman/rust-anything/releases/tag/v1.5.1) · [Homepage](https://www.npmjs.com/package/rust-anything)

---

## 速览

### 1. elementalsouls/Claude-BugHunter

Claude Code 的漏洞挖掘技能包，含 83 个技能与报告模式。

- 指标：⭐ 11,291 · 📈 今日 +2,322 · 🍴 1,505 · Python · MIT · 创建于 2026-05-05
- 上榜理由：GitHub Trending 今日 +2,322 Stars；近 3 天 +4,921 Stars
- 适合谁：适合做授权渗透测试、漏洞赏金和外部红队的安全人员，不适合未授权测试者或只需要通用编程辅助的人。
- 留意：这是攻击性安全工具，只能用于授权范围；README 与仓库描述的技能数不一致（83 vs 82），且 681 条报告模式中仅 433 条标注逐条引用可审计，采用前需自行核验。
- 链接：[仓库](https://github.com/elementalsouls/Claude-BugHunter) · [最新 Release](https://github.com/elementalsouls/Claude-BugHunter/releases/tag/v2.1) · [Homepage](https://elementalsouls.github.io/Claude-BugHunter)

### 2. google-research/paper-orchestra

多智能体自动写 AI 论文并生成 LaTeX 稿，适合看端到端流程。

- 指标：⭐ 4,225 · 📈 今日 +1,529 · 🍴 529 · Python · Apache-2.0 · 创建于 2026-05-02
- 上榜理由：GitHub Trending 今日 +1,529 Stars；近 2 天 +2,795 Stars
- 适合谁：适合需要快速生成论文初稿或 LaTeX 草稿的 AI 研究者；不适合期待开箱即用数据集或正式产品支持的用户。
- 留意：需自行配置 Semantic Scholar、OpenAI/Gemini/Vertex AI 等 API key，可能产生调用成本；生成论文的准确性与引用可靠性需人工核验，且 README 明确数据集未随仓库提供、项目非 Google 官方支持产品。许可证为 Apache-2.0。
- 链接：[仓库](https://github.com/google-research/paper-orchestra) · [Homepage](https://yiwen-song.github.io/paper_orchestra/)

### 3. affaan-m/ECC

多 agent harness 性能优化系统，含技能、记忆与安全。

- 指标：⭐ 306,449 · 📈 今日 +1,109 · 🍴 45,115 · JavaScript · MIT · 创建于 2026-01-18
- 上榜理由：GitHub Trending 今日 +1,109 Stars；近 5 天 +3,901 Stars
- 适合谁：适合同时使用多种 AI coding agent、希望统一增强技能/记忆/安全与研究流程的开发者；不适合只需要单一轻量插件或排斥托管/付费服务的用户。
- 留意：采用前注意只从 README 列出的官方渠道安装，第三方镜像可能含恶意软件；Pro 私有仓库能力为付费服务（$19/seat/mo 起），且 README 未说明具体依赖与兼容版本。
- 链接：[仓库](https://github.com/affaan-m/ECC) · [最新 Release](https://github.com/affaan-m/ECC/releases/tag/v2.2.3) · [Homepage](https://ecc.tools)

### 4. Immortal-Protocols/lastbook

离线生存知识库，把手册、视频、地图与本地 AI 问答装进一台电脑

- 指标：⭐ 2,150 · 📈 近 24h +435 · 🍴 279 · Python · MIT · 创建于 2026-11-13
- 上榜理由：近 24 小时 +435 Stars；创建仅 5 天的新项目；近 7 天发布 v1.1.11
- 适合谁：适合需要在断网环境查阅资料、且使用 macOS 14+、Windows 10+ 或 Ubuntu 24.04/26.04 x86_64 的用户；不适合需要全球详细地图或非美国地址离线搜索的用户。
- 留意：项目创建于 2026-11、版本仍在 1.1.x，Linux 版仅在 WSL2 的 Ubuntu 24.04.5 上验证过安装、播放与 AI，原生 GPU 性能和其他发行版未验证；下载依赖 downloads.lastbook.org 与 Hugging Face，且只信任内置的 11 个根证书，另外资料包内容的授权情况 README 未说明。
- 链接：[仓库](https://github.com/Immortal-Protocols/lastbook) · [最新 Release](https://github.com/Immortal-Protocols/lastbook/releases/tag/v1.1.11) · [Homepage](lastbook.org)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [krisgfx9/Wireless-Device-Battery-Monitor](https://github.com/krisgfx9/Wireless-Device-Battery-Monitor) | 3,911 | 近 24h +1,350 | 2026-11-18 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 27,149 | 近 24h +1,178 | 2026-11-15 |
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 36,949 | 近 24h +1,270 | 2026-11-14 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 69,945 | 今日 +1,062 | 2026-11-18 |
| [stablyai/orca](https://github.com/stablyai/orca) | 128,839 | 近 24h +1,042 | 2026-11-16 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
