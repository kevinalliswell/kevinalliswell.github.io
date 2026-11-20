---
title: "GitHub 热点 2026-11-21｜rust-anything：录制原应用行为，逐块校验 Rust 重写，适合增量迁移。"
date: "2026-11-21T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Rust"]
categories: ["日报"]
summary: "今日主推 erkamyaman/rust-anything（近 24h +1,492 Stars），速览 4 个：blender-ai-mcp-addon、floorplan、Ghost-Downloader-3 等。"
---

> 今日主推 erkamyaman/rust-anything（近 24h +1,492 Stars），速览 4 个：blender-ai-mcp-addon、floorplan、Ghost-Downloader-3 等。

## 今日主推：[erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything)

> 录制原应用行为，逐块校验 Rust 重写，适合增量迁移。

⭐ 6,589 · 📈 近 24h +1,492 · 🍴 518 · Rust · MIT · 创建于 2026-11-16

*2026-11-19 推荐过，因发布新版本 v2.1.0再次上榜。*

**为什么是今天**

- 近 24 小时 +1,492 Stars
- 近 3 天 +5,424 Stars
- 创建仅 4 天的新项目
- 近 7 天发布 v2.1.0

**它解决什么问题**

把现有应用逐步重写为 Rust 时，难以证明行为保持一致。它先录制原应用在边界用例、语义陷阱和自定义输入下的返回或异常，再用 diff 回放校验每个 Rust 片段，gate 通过后才继续，最终可 app lift 为纯 Rust。

**和同类相比**

与直接翻译代码或一次性重写不同，它通过 record、bridge、diff、gate、app lift 的流程，用行为录制验证重写，并借助 napi-rs、PyO3、wasm-bindgen 维持原语言调用；但它只能捕获录制覆盖到的行为。

**适合谁**

适合希望把 TypeScript/JavaScript、Python、C、Go、Ruby、Java 或 Kotlin 应用增量迁移到 Rust 的团队；不适合期待完全自动翻译或对未录制行为也要求等价保证的人。

**最短上手**

```bash
README 未说明具体安装/运行命令
提供 crates.io、npm、GitHub Releases 和 Claude Code plugin 入口
```

**采用前留意**

项目较新，流程依赖 coding agent 与行为录制覆盖，README 明确只能捕获录制覆盖到的内容；PHP 和 C# 目前仅支持 record、replay 和 front door。许可证为 MIT，仍需评估多语言绑定与迁移维护成本。

官方描述：Rewrite your whole app in Rust, one piece at a time, checked against the original's recorded behavior at every step. CLIs, HTTP servers and libraries in TypeScript, Python, C, Go, Ruby and Java.

Topics：`agent-skills` `claude-code` `cli` `code-migration` `codex` `ffi` `golang` `java`

链接：[仓库](https://github.com/erkamyaman/rust-anything) · [最新 Release](https://github.com/erkamyaman/rust-anything/releases/tag/v2.1.0) · [Homepage](https://www.npmjs.com/package/rust-anything)

---

## 速览

### 1. bookwjitchieni1986/blender-ai-mcp-addon

Blender AI 助手，内建 MCP server，支持场景操作与多代理工作流。

- 指标：⭐ 1,746 · 📈 日均 +873 · 🍴 3 · Unknown · MIT · 创建于 2026-11-19
- 上榜理由：创建以来日均 +873 Stars；创建仅 1 天的新项目；近 7 天发布 v1.0.0
- 适合谁：适合希望加速迭代的艺术家、自动化重复工作的 technical artist，以及把 AI 工具接入 Blender 的开发者；不适合需要跨平台发布包或严格安全沙箱的用户。
- 留意：MIT 许可证；README 说明发布包仅面向 Windows x64 与 Blender 4.2+，Python 工具校验不是安全沙箱，外部 MCP 客户端需自行管理审批，且当前为 1.0.0 版本，成熟度需自行评估。
- 链接：[仓库](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon) · [最新 Release](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon/releases/tag/v1.0.0)

### 2. haydenschmitty/floorplan

用 Claude/Codex 把代码库绘成可交互 plain-English 地图，便于理解结构

- 指标：⭐ 5,623 · 📈 近 24h +618 · 🍴 487 · JavaScript · MIT · 创建于 2026-10-27
- 上榜理由：近 24 小时 +618 Stars；创建 24 天的新项目；近 7 天发布 floorplan--v0.11.0
- 适合谁：适合用 AI 构建应用但不读代码的 builder、需要快速 onboarding 的团队，不适合只想导出演示图或逐函数研究大型代码库的人。
- 留意：MIT 许可证且 README 标注 Node 18+、零依赖；但版本仅 0.11.0，核心使用依赖 Claude Code 或 Codex，Health check 自述为检查而非审计，不能替代安全审计。
- 链接：[仓库](https://github.com/haydenschmitty/floorplan) · [最新 Release](https://github.com/haydenschmitty/floorplan/releases/tag/floorplan--v0.11.0) · [Homepage](https://haydenschmitty.github.io/floorplan-demo/)

### 3. XiaoYouChR/Ghost-Downloader-3

跨平台多协议下载管理器，集成 HTTP/BT、流媒体与 CLI

- 指标：⭐ 13,662 · 📈 今日 +1,082 · 🍴 837 · Python · GPL-3.0 · 创建于 2023-08-16
- 上榜理由：GitHub Trending 今日 +1,082 Stars；近 7 天发布 v4.5.11
- 适合谁：适合需要跨平台、多协议下载和网页流媒体抓取的个人用户；不适合只想要极简 CLI 下载器，或使用无 AVX CPU、非 arm64-v8a Android 设备的用户。
- 留意：采用前注意 GPL-3.0 许可证、Qt 6.6+ 对无 AVX CPU 的限制，以及 README 路线图中插件 API 尚未公开稳定；Android 仅提供 arm64-v8a。
- 链接：[仓库](https://github.com/XiaoYouChR/Ghost-Downloader-3) · [最新 Release](https://github.com/XiaoYouChR/Ghost-Downloader-3/releases/tag/v4.5.11) · [Homepage](https://gd.xychr.com/)

### 4. zhouxiaoka/autoclip

开源桌面 AI 视频剪辑工具，贴链接一键生成多平台短视频、字幕、封面和文案。

- 指标：⭐ 12,143 · 📈 今日 +983 · 🍴 2,009 · Python · MIT · 创建于 2025-07-08
- 上榜理由：GitHub Trending 今日 +983 Stars
- 适合谁：适合需要将长视频快速拆成多平台短视频的内容创作者、播客或课程运营者；不适合只想用纯在线零配置服务或不愿承担云端模型费用的用户。
- 留意：软件免费但云端模型按量计费，成本需自行评估；项目创建于 2025-07-08，提供的 README 未给出完整安装/运行命令，采用前应先在目标环境验证桌面、CLI 与 MCP 的可用性。
- 链接：[仓库](https://github.com/zhouxiaoka/autoclip) · [最新 Release](https://github.com/zhouxiaoka/autoclip/releases/tag/v1.5.8) · [Homepage](https://zhouxiaoka.github.io/autoclip_intro/)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 14,150 | 今日 +1,660 | 2026-11-19 |
| [stablyai/orca](https://github.com/stablyai/orca) | 130,989 | 近 24h +1,146 | 2026-11-16 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 28,991 | 近 24h +834 | 2026-11-15 |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | 2,691 | 今日 +874 | 2026-11-20 |
| [krisgfx9/Wireless-Device-Battery-Monitor](https://github.com/krisgfx9/Wireless-Device-Battery-Monitor) | 5,261 | 近 24h +624 | 2026-11-18 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
