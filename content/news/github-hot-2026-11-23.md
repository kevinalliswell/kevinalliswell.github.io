---
title: "GitHub 热点 2026-11-23｜fast-anything：把慢的5%函数用 coding agent 移植到 Rust，并用真实调…"
date: "2026-11-23T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Rust"]
categories: ["日报"]
summary: "今日主推 EL4CTEO/fast-anything（日均 +912 Stars），速览 4 个：Xbox2Windows、stitch-skills、inference-optimisation-skill 等。"
---

> 今日主推 EL4CTEO/fast-anything（日均 +912 Stars），速览 4 个：Xbox2Windows、stitch-skills、inference-optimisation-skill 等。

## 今日主推：[EL4CTEO/fast-anything](https://github.com/EL4CTEO/fast-anything)

> 把慢的5%函数用 coding agent 移植到 Rust，并用真实调用验证。

⭐ 1,824 · 📈 日均 +912 · 🍴 107 · Rust · MIT · 创建于 2026-11-21

**为什么是今天**

- 创建以来日均 +912 Stars
- 创建仅 1 天的新项目
- 近 7 天发布 v0.7.0

**它解决什么问题**

解决全量重写 Rust 成本高，而运行时往往集中在少数热点函数的问题。它 profile 应用、移植热点函数，并在行为一致后按函数启用。

**和同类相比**

与整体重写不同，它只移植可移植的外层热点循环，每个 port 是单函数 crate，可逆且通过录制调用和派生边界用例验证。取舍是仅支持确定性的纯数据函数，跨语言调用成本过高时不会启用。

**适合谁**

适合已有 Python、Node/TypeScript、Ruby、Java、Kotlin、Go、PHP、C/C++、C# 应用并愿意引入 Rust 工具链来低风险优化热点的人；不适合需要移植非确定性或非纯数据函数、或不愿引入 Rust/FFI 的项目。

**最短上手**

```bash
npm i -g @el4cteo/fast-anything
fast-anything go --agent claude -- python app.py
```

**采用前留意**

项目较新，README 未说明生产成熟度与长期维护计划；采用前需确认 Rust 工具链及各语言 FFI/绑定依赖，例如 PHP 需 FFI 扩展、Go 需 cgo。

官方描述：Don't rewrite it in Rust. Rewrite the 5% that's slow: profile Python, Node or Ruby apps, port the hot functions with your coding agent, prove they behave the same.

Topics：`agent-skills` `ai-agents` `claude-code` `claude-code-plugin` `codex` `developer-tools` `ffi` `mcp`

链接：[仓库](https://github.com/EL4CTEO/fast-anything) · [最新 Release](https://github.com/EL4CTEO/fast-anything/releases/tag/v0.7.0) · [Homepage](https://www.npmjs.com/package/@el4cteo/fast-anything)

---

## 速览

### 1. R0Y00/Xbox2Windows

Xbox 到 Windows 静态重编译研究，含 CPU/shader 实验。

- 指标：⭐ 1,292 · 📈 近 24h +418 · 🍴 125 · Python · MIT · 创建于 2026-11-21
- 上榜理由：近 24 小时 +418 Stars；创建仅 2 天的新项目；近 7 天发布 gpu-check-v0.1.0
- 适合谁：适合研究静态重编译、D3D12/DXIL shader 翻译和 Windows 运行时兼容的开发者；不适合想直接运行完整 GTA VI 的普通玩家。
- 留意：许可证为 MIT，但项目成熟度有限：完整游戏启动、该游戏标题的 CPU 代码执行和帧率未验证，主可执行文件在检查的包中缺失；构建还依赖 x64 Windows、Python 3.11+ 与指定 Windows SDK/DXC。
- 链接：[仓库](https://github.com/R0Y00/Xbox2Windows) · [最新 Release](https://github.com/R0Y00/Xbox2Windows/releases/tag/gpu-check-v0.1.0)

### 2. google-labs-code/stitch-skills

面向 Stitch MCP 的 Agent Skills 集合，覆盖设计到代码生成。

- 指标：⭐ 11,898 · 📈 今日 +516 · 🍴 1,473 · TypeScript · Apache-2.0 · 创建于 2026-01-17
- 上榜理由：GitHub Trending 今日 +516 Stars；近 7 天 +2,636 Stars
- 适合谁：适合已配置 Stitch MCP、使用 Codex/Claude Code/Cursor/OpenCode 等编码 Agent 并希望把 Stitch 设计流程接入开发工作流的人；不适合未使用 Stitch MCP 或不需要 Agent Skills 插件的人。
- 留意：采用前需先配置 Stitch MCP 服务器、环境变量和凭据；README 未说明项目成熟度与版本策略，选择性安装时还需处理技能间依赖。
- 链接：[仓库](https://github.com/google-labs-code/stitch-skills) · [最新 Release](https://github.com/google-labs-code/stitch-skills/releases/tag/v1.0) · [Homepage](https://stitch.withgoogle.com/docs/mcp/setup)

### 3. sybil-solutions/inference-optimisation-skill

本地 LLM 服务提速的 agent skill：先算理论上限，再做交错基准与稳定性门禁。

- 指标：⭐ 1,949 · 📈 近 24h +357 · 🍴 181 · Python · MIT · 创建于 2026-11-17
- 上榜理由：近 24 小时 +357 Stars；近 5 天 +1,050 Stars；创建仅 6 天的新项目
- 适合谁：适合使用 Claude Code 或兼容 SKILL.md 的 agent、并愿意自行做基准测量的开发者；不适合需要开箱即用托管服务或不愿投入测量成本的人。
- 留意：MIT 许可证；主要风险是 README 的加速数据绑定具体硬件、模型和引擎，不能直接外推，且流程要求反复基准测试与长上下文门禁，时间和算力成本不低。脚本面向 OpenAI-compatible server，其他栈需自行适配。
- 链接：[仓库](https://github.com/sybil-solutions/inference-optimisation-skill)

### 4. headroomlabs-ai/headroom

本地压缩 Agent 日志、JSON、代码和 RAG 内容，降低 LLM token 消耗。

- 指标：⭐ 80,496 · 📈 近 24h +239 · 🍴 6,303 · Python · Apache-2.0 · 创建于 2026-01-08
- 上榜理由：近 24 小时 +239 Stars；近 7 天 +754 Stars；近 7 天发布 v0.45.0
- 适合谁：适合希望降低 coding agent/RAG token 成本并接受本地压缩层的团队；不适合只想压缩普通散文或不愿引入额外代理/依赖的场景。
- 留意：License 为 Apache-2.0；项目创建于 2026-01-07，成熟度和长期维护 README 未说明。TypeScript SDK 需额外运行 proxy，且 README 明确散文压缩收益较小。
- 链接：[仓库](https://github.com/headroomlabs-ai/headroom) · [最新 Release](https://github.com/headroomlabs-ai/headroom/releases/tag/v0.45.0) · [Homepage](https://docs.headroomlabs.ai/docs)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [ItsNotRexed/Leonida](https://github.com/ItsNotRexed/Leonida) | 14,539 | 近 24h +9,983 | 2026-11-22 |
| [bookwjitchieni1986/blender-ai-mcp-addon](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon) | 2,746 | 近 24h +424 | 2026-11-21 |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 17,689 | 今日 +1,721 | 2026-11-19 |
| [erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything) | 7,967 | 近 24h +585 | 2026-11-22 |
| [stablyai/orca](https://github.com/stablyai/orca) | 132,930 | 近 24h +993 | 2026-11-16 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
