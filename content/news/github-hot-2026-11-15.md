---
title: "GitHub 热点 2026-11-15｜open-code-review：阿里开源 AI 代码审查 CLI，确定性流水线结合 Agent，行级定位…"
date: "2026-11-15T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Go"]
categories: ["日报"]
summary: "今日主推 alibaba/open-code-review（今日 +897 Stars），速览 4 个：dsh-Go、rea-video、chat-demo 等。"
---

> 今日主推 alibaba/open-code-review（今日 +897 Stars），速览 4 个：dsh-Go、rea-video、chat-demo 等。

## 今日主推：[alibaba/open-code-review](https://github.com/alibaba/open-code-review)

> 阿里开源 AI 代码审查 CLI，确定性流水线结合 Agent，行级定位精准。

⭐ 51,388 · 📈 今日 +897 · 🍴 3,905 · Go · Apache-2.0 · 创建于 2026-05-18

**为什么是今天**

- GitHub Trending 今日 +897 Stars
- 近 7 天发布 v1.13.9

**它解决什么问题**

解决通用 Agent 审查较大变更集时覆盖不全、评论位置漂移、审查质量不稳定的问题。

**和同类相比**

用确定性工程约束文件选择、规则匹配和评论定位，Agent 负责动态检索与判断；取舍是精度优先，Recall 低于通用 Agent。

**适合谁**

适合在本地或 CI 中做代码审查、重视低误报的团队；不适合追求最高召回或不愿配置模型端点的人。

**最短上手**

```bash
README 未说明安装/运行命令
仅说明配置模型端点即可开始使用 CLI
```

**采用前留意**

Apache-2.0 许可证；需自备 OpenAI 或 Anthropic 兼容模型端点，会产生 token 成本并涉及代码外发。README 未给出完整安装命令，且其 Recall 低于通用 Agent。

官方描述：Secure, fast, efficient, battle-tested at Alibaba's scale. Hybrid architecture code review tool: deterministic pipelines + LLM Agent, precise line-level comments, built-in multi-language ruleset (NPE, thread-safety, XSS, SQL injection), OpenAI & Anthropic compatible.

Topics：`agent` `agent-skills` `code-review` `code-review-assistant` `harness` `repository-level-context`

链接：[仓库](https://github.com/alibaba/open-code-review) · [最新 Release](https://github.com/alibaba/open-code-review/releases/tag/v1.13.9) · [Homepage](https://open-codereview.ai)

---

## 速览

### 1. ccch1mneyyy/dsh-Go

手机端 DeepSeek Harness：本机运行或远程控制电脑。

- 指标：⭐ 22,702 · 📈 近 24h +662 · 🍴 1,060 · Dart · AGPL-3.0 · 创建于 2026-10-25
- 上榜理由：近 24 小时 +662 Stars；创建 20 天的新项目；近 7 天发布 v1.0.16
- 适合谁：适合需要在 Android 手机上用 DSH 或远程操控电脑 DSH 的用户；不适合依赖 iOS/鸿蒙、32 位 ARM 或完整远程插件管理的人。
- 留意：AGPL-3.0 采用前需评估源码披露等合规义务；项目为第三方客户端，功能依赖 DeepSeek Harness 和所配置的模型提供方。远程连接存在附件、插件管理和导出限制；覆盖安装不同签名测试包会清空对话、Linux 环境和设置。
- 链接：[仓库](https://github.com/ccch1mneyyy/dsh-Go) · [最新 Release](https://github.com/ccch1mneyyy/dsh-Go/releases/tag/v1.0.16)

### 2. JuneYaooo/rea-video

用 Agent 逐镜头逆向视频来源并输出开放 VIDEO.md，便于复刻。

- 指标：⭐ 8,555 · 📈 近 24h +459 · 🍴 1,260 · Python · Apache-2.0 · 创建于 2026-10-30
- 上榜理由：近 24 小时 +459 Stars；创建 16 天的新项目；近 7 天发布 v0.1.0
- 适合谁：适合需要拆解短视频、广告、AI 视频或混合素材并复刻的创作者和开发者；不适合无法使用 Agent 与 ffmpeg 的用户。
- 留意：采用前需准备 ffmpeg、Python 3.10+ 和可执行命令的 Agent，接入 Gemini/Doubao 等视频模型要提供 endpoint/key，可能增加成本；项目创建时间较新，长期维护情况 README 未说明。README 也提示压缩样片或无视觉模型时结果会不同，许可证为 Apache-2.0。
- 链接：[仓库](https://github.com/JuneYaooo/rea-video) · [最新 Release](https://github.com/JuneYaooo/rea-video/releases/tag/v0.1.0) · [Homepage](https://www.reavideo.ai/)

### 3. deepseek-ai/chat-demo

基于 DeepSeek API 的纯前端聊天 Demo，无需应用后端即可对话。

- 指标：⭐ 1,721 · 📈 近 24h +617 · 🍴 288 · TypeScript · MIT · 创建于 2026-11-12
- 上榜理由：近 24 小时 +617 Stars；创建仅 2 天的新项目；近 7 天发布 v0.1.1
- 适合谁：适合想体验 DeepSeek API 聊天能力或做前端二次开发的开发者；不适合需要服务端密钥托管和多用户后端的场景。
- 留意：API key 存于浏览器 localStorage，消息和附件会发送到配置的 API 服务；通过 file:// 打开或部署静态站点时，还依赖浏览器存储与目标 API 的 CORS/能力支持。导入历史会覆盖本地全部会话和附件，导出不包含 API key、设置及原始非图片附件；MIT 许可，第三方依赖需分别核查，README 未说明项目成熟度与安全审计情况。
- 链接：[仓库](https://github.com/deepseek-ai/chat-demo) · [最新 Release](https://github.com/deepseek-ai/chat-demo/releases/tag/v0.1.1) · [Homepage](https://deepseek-ai.github.io/chat-demo/)

### 4. Graphify-Labs/graphify

用 /graphify 把代码库解析成本地知识图谱，替代 grep 式查找

- 指标：⭐ 147,746 · 📈 近 24h +374 · 🍴 14,160 · Python · Apache-2.0 · 创建于 2026-04-03
- 上榜理由：近 24 小时 +374 Stars；近 7 天发布 v0.9.109
- 适合谁：适合使用 Claude Code、Cursor、Codex、Gemini CLI 等助手、希望在较大代码库中按图查询与追踪路径的开发者；不适合要求全类型文件纯离线处理或需要成熟稳定产品的团队。
- 留意：仓库创建于 2026-04-03，属新项目，README 未说明版本稳定性与长期维护计划；PyPI 包名为 graphifyy（与仓库名不同），且文档/PDF 等语义解析会消耗助手模型或 API key 额度，具体成本 README 未说明。许可证为 Apache-2.0。
- 链接：[仓库](https://github.com/Graphify-Labs/graphify) · [最新 Release](https://github.com/Graphify-Labs/graphify/releases/tag/v0.9.109) · [Homepage](https://www.graphify.com)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [storytold/craft-anything](https://github.com/storytold/craft-anything) | 32,722 | 近 24h +1,057 | 2026-11-14 |
| [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | 5,959 | 今日 +1,225 | 2026-11-14 |
| [openai/codex-security](https://github.com/openai/codex-security) | 13,529 | 近 24h +281 | 2026-11-14 |
| [Gathin23/cleanyourtv](https://github.com/Gathin23/cleanyourtv) | 57,857 | 近 24h +349 | 2026-11-14 |
| [anthropics/claude-code](https://github.com/anthropics/claude-code) | 155,685 | 近 24h +89 | 2026-11-13 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
