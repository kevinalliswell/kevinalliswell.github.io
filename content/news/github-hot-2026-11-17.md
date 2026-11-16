---
title: "GitHub 热点 2026-11-17｜blender-ai-mcp-addon：把 AI 对话、场景工具和 MCP server 装进 Blender…"
date: "2026-11-17T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报"]
categories: ["日报"]
summary: "今日主推 hitkeeen/blender-ai-mcp-addon（近 24h +1,224 Stars），速览 4 个：kiri、SkillEvaluator、ffmpeg-skill 等。"
---

> 今日主推 hitkeeen/blender-ai-mcp-addon（近 24h +1,224 Stars），速览 4 个：kiri、SkillEvaluator、ffmpeg-skill 等。

## 今日主推：[hitkeeen/blender-ai-mcp-addon](https://github.com/hitkeeen/blender-ai-mcp-addon)

> 把 AI 对话、场景工具和 MCP server 装进 Blender 的插件。

⭐ 2,163 · 📈 近 24h +1,224 · 🍴 53 · Unknown · MIT · 创建于 2026-11-12

**为什么是今天**

- 近 24 小时 +1,224 Stars
- 创建仅 4 天的新项目
- 近 7 天发布 v1.0.0

**它解决什么问题**

它解决在 Blender 内用自然语言检查场景、创建和编辑对象/材质、查找资产与执行多步工作流的问题，减少手动重复操作和工具切换。

**和同类相比**

README 未说明与同类方案的直接对比；其特点是提供可视化 Studio、单助手或 Manager/Worker/Reviewer 团队链，并内置 MCP server。取舍是团队任务顺序执行，评审失败两次会停止流程。

**适合谁**

适合希望加速迭代的艺术家、自动化重复工作的技术美术，以及把 AI 工具接入 Blender 的开发者；不适合需要安全沙箱或依赖非 Windows x64 发布包的用户。

**最短上手**

```bash
下载 mcp-for-blender-pro.zip（Releases）。
Blender → Edit → Preferences → Get Extensions → 菜单 → Install from Disk，选择 ZIP 并启用。
3D Viewport → N → MCP Pro，选择 provider、填写连接信息并选择模型。
在 Blender 中发消息，或点击 Open Studio Window。
```

**采用前留意**

许可证为 MIT，但项目为 1.0.0 版本；发布包面向 Windows x64 与 Blender 4.2+。Python 工具校验并非安全沙箱，外部 MCP 客户端自行管理审批，云模型与资产服务还需各自密钥和许可配置。

官方描述：AI assistant and MCP server for Blender: visual chat, scene tools, multi-agent workflows. Works with ChatGPT/GPT, Claude, Gemini, Ollama, OpenCode. Blender AI addon, copilot for 3D, bpy Python scripting, MCP integration.

Topics：`ai-agents` `ai-assistant` `blender` `blender-addon` `blender-ai` `blender-automation` `blender-mcp` `blender-plugin`

链接：[仓库](https://github.com/hitkeeen/blender-ai-mcp-addon) · [最新 Release](https://github.com/hitkeeen/blender-ai-mcp-addon/releases/tag/v1.0.0)

---

## 速览

### 1. libracoder/kiri

Rust 写的轻量容器运行时，兼容 docker CLI 与 Compose

- 指标：⭐ 8,826 · 📈 近 24h +2,592 · 🍴 391 · Rust · Apache-2.0 · 创建于 2026-11-03
- 上榜理由：近 24 小时 +2,592 Stars；创建 14 天的新项目；近 7 天发布 v0.2.1
- 适合谁：适合已用 docker、Compose、buildx、希望桌面运行时更轻更快的 macOS/Windows/Linux 开发者，不适合依赖完整 Docker Desktop 功能或要求成熟稳定构建链的团队。
- 留意：代码为 Apache-2.0，但 guest kernel 属 Linux GPL-2.0，且 “Kiri” 名称与 logo 不在许可证范围内，fork 需改名换标；仓库创建时间很新、README 未说明版本成熟度与长期维护承诺，内置 builder 尚未交付，仓库描述中的 Ngrok 替代功能 README 未说明，采用前需自行验证。
- 链接：[仓库](https://github.com/libracoder/kiri) · [最新 Release](https://github.com/libracoder/kiri/releases/tag/v0.2.1) · [Homepage](https://runkiri.com)

### 2. NVIDIA/SkillEvaluator

NVIDIA 三层 AI agent skill 评估框架：校验、去重、实跑对比

- 指标：⭐ 2,623 · 📈 今日 +953 · 🍴 356 · Python · Apache-2.0 · 创建于 2026-06-24
- 上榜理由：GitHub Trending 今日 +953 Stars；近 7 天发布 v0.9.0
- 适合谁：适合维护 agent skills/plugins、希望在 CI 中加入质量门禁的团队；不适合不愿准备 LLM provider 或 Docker sandbox 来完成完整评估的使用者。
- 留意：License 为 Apache-2.0；仓库创建于 2026-06-24，长期维护与稳定性需自行评估。Tier 1 完整静态覆盖依赖外部 scanner，Tier 3 需要 provider、受支持的 agent 与 sandbox，模型或托管 sandbox 可能产生费用。
- 链接：[仓库](https://github.com/NVIDIA/SkillEvaluator) · [最新 Release](https://github.com/NVIDIA/SkillEvaluator/releases/tag/v0.9.0) · [Homepage](https://docs.nvidia.com/skills/skillevaluator/)

### 3. kajisho5/ffmpeg-skill

给 coding agent 的本地视频编辑器：42 个 FFmpeg 工具，支持 MCP。

- 指标：⭐ 6,629 · 📈 今日 +475 · 🍴 598 · Python · MIT · 创建于 2026-09-03
- 上榜理由：GitHub Trending 今日 +475 Stars；近 2 天 +1,059 Stars；近 7 天发布 v3.10.1
- 适合谁：适合使用 Claude Code、Cursor、Codex 或任意 MCP client、希望本地处理视频的开发者；不适合不通过 agent/CLI 操作视频的用户。
- 留意：许可证为 MIT；运行依赖本机 ffmpeg/ffprobe 与 python3 在 PATH，README 未说明生产成熟度或长期维护承诺。
- 链接：[仓库](https://github.com/kajisho5/ffmpeg-skill) · [最新 Release](https://github.com/kajisho5/ffmpeg-skill/releases/tag/v3.10.1) · [Homepage](https://www.npmjs.com/package/ffmpeg-skill)

### 4. ag-ui-protocol/ag-ui

开源事件协议，标准化 Agent 与任意应用的双向连接，适合前端集成。

- 指标：⭐ 18,911 · 📈 今日 +790 · 🍴 1,961 · TypeScript · MIT · 创建于 2025-05-07
- 上榜理由：GitHub Trending 今日 +790 Stars；近 2 天 +1,577 Stars；近 7 天发布 release/2026-11-13
- 适合谁：适合需要把 LangChain、CrewAI、Mastra、Google ADK 等框架构建的 agent 接入 Web、移动端、terminal 或 Slack 的前端/全栈开发者；不适合只需要简单请求/响应且不愿维护事件流协议的项目。
- 留意：MIT 许可证；README 称 1.0 规范已冻结且双向向后兼容，但仓库创建于 2025-05-07，生产采用仍需评估 SDK/框架集成的持续演进。CLI 模板默认调用 OpenAI，需要 API key 并可能产生费用。
- 链接：[仓库](https://github.com/ag-ui-protocol/ag-ui) · [最新 Release](https://github.com/ag-ui-protocol/ag-ui/releases/tag/release/2026-11-13) · [Homepage](https://ag-ui.com)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [dream-num/univer](https://github.com/dream-num/univer) | 27,739 | 今日 +1,878 | 2026-11-16 |
| [deepseek-ai/chat-demo](https://github.com/deepseek-ai/chat-demo) | 4,042 | 近 24h +1,142 | 2026-11-15 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 24,745 | 近 24h +1,018 | 2026-11-15 |
| [stablyai/orca](https://github.com/stablyai/orca) | 126,737 | 近 24h +1,015 | 2026-11-16 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | 52,899 | 今日 +946 | 2026-11-15 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
