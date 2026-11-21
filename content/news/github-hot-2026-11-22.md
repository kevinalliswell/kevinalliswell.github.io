---
title: "GitHub 热点 2026-11-22｜rust-anything：把应用逐块重写成 Rust，并用录制下来的原行为逐例校验等价性。"
date: "2026-11-22T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Rust"]
categories: ["日报"]
summary: "今日主推 erkamyaman/rust-anything（近 24h +793 Stars），速览 4 个：Leonida、SoduWork、neonclipping 等。"
---

> 今日主推 erkamyaman/rust-anything（近 24h +793 Stars），速览 4 个：Leonida、SoduWork、neonclipping 等。

## 今日主推：[erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything)

> 把应用逐块重写成 Rust，并用录制下来的原行为逐例校验等价性。

⭐ 7,382 · 📈 近 24h +793 · 🍴 588 · Rust · MIT · 创建于 2026-11-16

*2026-11-21 推荐过，因发布新版本 v3.1.0再次上榜。*

**为什么是今天**

- 近 24 小时 +793 Stars
- 近 4 天 +6,217 Stars
- 创建仅 5 天的新项目
- 近 7 天发布 v3.1.0

**它解决什么问题**

当团队要把已有的 TypeScript/JavaScript、Python、C、Go、Ruby、Java 或 Kotlin 应用、CLI 或 HTTP server 迁到 Rust 时，最难的是证明重写后行为与原来一致。rust-anything 先录制原应用在生成边界用例、语义陷阱和自定义输入上的返回或抛错，再逐块对照 Rust 实现的重放结果。

**和同类相比**

README 强调它不做代码翻译，核心是 record → bridge → diff → gate → lift 的行为验证流程，调用方通过 bridge 生成的 wrapper 保持原 API；代价是只能覆盖录制到的行为，README 专门列出了 “What it can't catch”。

**适合谁**

适合想把 CLI、HTTP server 或库整体或逐条热路径迁到 Rust 的团队；不适合期望全自动翻译代码，或无法提供有代表性输入的人。

**最短上手**

```bash
README 截断，quick-start 段未给出具体命令
包发布在 crates.io 与 npm（均为 rust-anything）
另提供 Claude Code plugin 与 MCP Registry 入口
```

**采用前留意**

许可证为 MIT，但项目创建于 2026-11-16，仍很新，成熟度需自行评估；跨语言桥接依赖 napi-rs、PyO3 与 wasm-bindgen，且 PHP/C# 目前只有 record、replay 和 front door，unit ports 尚未支持，未录制到的行为也没有等价性保证。

官方描述：Rewrite your whole app in Rust, one piece at a time, checked against the original's recorded behavior at every step. CLIs, HTTP servers and libraries in TypeScript, Python, C, Go, Ruby and Java.

Topics：`agent-skills` `claude-code` `cli` `code-migration` `codex` `ffi` `golang` `java`

链接：[仓库](https://github.com/erkamyaman/rust-anything) · [最新 Release](https://github.com/erkamyaman/rust-anything/releases/tag/v3.1.0) · [Homepage](https://www.npmjs.com/package/rust-anything)

---

## 速览

### 1. ItsNotRexed/Leonida

自有 Xbox 版 GTA VI 的 PC 静态重编译早期项目，值得关注。

- 指标：⭐ 4,556 · 📈 日均 +4,556 · 🍴 312 · Python · GPL-3.0 · 创建于 2026-11-21
- 上榜理由：创建以来日均 +4,556 Stars；创建仅 1 天的新项目
- 适合谁：适合能自备指定版本游戏副本、熟悉 Python/.NET/Vulkan/LLVM 工具链并关注主机游戏重编译的开发者；不适合想直接开玩的普通玩家。
- 留意：项目处于早期，README 明确游戏尚不能启动，PE loader、Xbox D3D12→Vulkan 等关键部分仅为骨架或进行中；构建需要自备 Xbox Series 1.0.2.1 副本、约 350 GB 工作空间及多项 SDK/工具链。GPL-3.0 许可，生成的资产与运行时文件不应分享。
- 链接：[仓库](https://github.com/ItsNotRexed/Leonida)

### 2. mdiri-ai/SoduWork

面向团队与 Agent 的自托管 AI 工作引擎，强调多 harness 与人工验收。

- 指标：⭐ 6,437 · 📈 近 24h +484 · 🍴 507 · JavaScript · MIT · 创建于 2026-10-29
- 上榜理由：近 24 小时 +484 Stars；创建 23 天的新项目；近 7 天发布 v1.13.19
- 适合谁：适合需要自托管、多 Agent 协作和人工签收的团队；不适合只需要单轮聊天或不愿承担自托管部署维护的人。
- 留意：README 明确项目处于 public beta，建议生产使用前先评估；自托管需准备 Python 3.12.x/Node.js 22.x（或 Docker）并配置模型服务，首次连接探测成功也不保证推理可用。
- 链接：[仓库](https://github.com/mdiri-ai/SoduWork) · [最新 Release](https://github.com/mdiri-ai/SoduWork/releases/tag/v1.13.19) · [Homepage](https://www.soduwork.ai)

### 3. iamajmeena/neonclipping

本地开源、零 API 成本的链接转 9:16 字幕切片工具，约 2 分钟出片。

- 指标：⭐ 1,730 · 📈 近 24h +493 · 🍴 84 · Python · MIT · 创建于 2026-11-19
- 上榜理由：近 24 小时 +493 Stars；创建仅 2 天的新项目；近 7 天发布 v1.1.0
- 适合谁：适合注重隐私、想零 API 成本制作短视频切片的创作者和开发者；不适合不愿配置本地依赖/本地 LLM 或本地算力不足的用户。
- 留意：仓库较新（信息显示创建于 2026-11-19），最低硬件要求 README 未说明；依赖 FFmpeg、Whisper/YouTube captions、Ollama 本地 LLM 等，实际速度与质量受本机算力和网络影响。README 提到 52 种字幕语言，但完整限制说明被截断，采用前需核对。
- 链接：[仓库](https://github.com/iamajmeena/neonclipping) · [最新 Release](https://github.com/iamajmeena/neonclipping/releases/tag/v1.1.0)

### 4. Minireel/HGhub

插件化接入内容源的通用视频播放器，统一浏览、播放与片库管理。

- 指标：⭐ 11,015 · 📈 近 24h +569 · 🍴 8,934 · Rust · 创建于 2026-11-03
- 上榜理由：近 24 小时 +569 Stars；近 7 天 +2,164 Stars；创建 18 天的新项目；近 7 天发布 v0.0.4
- 适合谁：适合愿意自行寻找并导入插件、在 Windows 或 Android 上使用通用播放器的用户；不适合需要开箱即用内容源、商业使用或依赖其他平台稳定支持的用户。
- 留意：仓库元数据未声明 License，README 则写明采用 PolyForm Noncommercial 1.0.0 并禁止商业用途；采用前需确认合规边界。项目处于早期开发，当前重点支持 Windows 与 Android，其他平台仍在适配验证，且第三方插件与内容源的可用性不由项目保证。
- 链接：[仓库](https://github.com/Minireel/HGhub) · [最新 Release](https://github.com/Minireel/HGhub/releases/tag/v0.0.4) · [Homepage](https://minireel.github.io/HGhub/)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [bookwjitchieni1986/blender-ai-mcp-addon](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon) | 2,322 | 近 24h +576 | 2026-11-21 |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 15,954 | 今日 +1,794 | 2026-11-19 |
| [stablyai/orca](https://github.com/stablyai/orca) | 131,937 | 近 24h +948 | 2026-11-16 |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | 3,361 | 今日 +724 | 2026-11-20 |
| [anefzaoui/misterdownloadmanager](https://github.com/anefzaoui/misterdownloadmanager) | 15,491 | 近 24h +1,201 | 2026-11-16 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
