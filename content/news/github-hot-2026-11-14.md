---
title: "GitHub 热点 2026-11-14｜codex-security：Codex Security CLI/SDK，用于查找、验证和修复代码漏…"
date: "2026-11-14T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "TypeScript"]
categories: ["日报"]
summary: "今日主推 openai/codex-security（今日 +751 Stars），速览 4 个：craft-anything、GestaltX、modern-web-guidance-src 等。"
---

> 今日主推 openai/codex-security（今日 +751 Stars），速览 4 个：craft-anything、GestaltX、modern-web-guidance-src 等。

## 今日主推：[openai/codex-security](https://github.com/openai/codex-security)

> Codex Security CLI/SDK，用于查找、验证和修复代码漏洞。

⭐ 13,248 · 📈 今日 +751 · 🍴 1,027 · TypeScript · Apache-2.0 · 创建于 2026-07-14

**为什么是今天**

- GitHub Trending 今日 +751 Stars
- 近 7 天发布 npm-v0.10.0
- 来自重点官方组织

**它解决什么问题**

它帮助开发者定位、调查并修复代码中的安全漏洞，并可通过 CLI、SDK、Codex 工作流或 CI 自动化扫描仓库、指定路径与 Git 变更。

**和同类相比**

它将扫描、候选发现验证、补丁生成与修复验证串成工作流，还覆盖 SECURITY.md、威胁模型、第三方扫描导入与工单/导出；README 未说明与同类方案的具体对比。

**适合谁**

适合需要在终端、Codex 工作流或 CI 中扫描并跟进漏洞的团队；不适合不愿配置登录/API Key 及 Node.js、Python 依赖的使用者。

**最短上手**

```bash
npm install --global @openai/codex-security
cs login
cs scan .
```

**采用前留意**

采用前需确认 Node.js 22.13+（22.x）/24/26 与 Python 3.10+ 依赖、登录或 CI 的 API Key 要求，以及扫描成本限制；项目创建于 2026-07-13，成熟度需自行评估，许可证为 Apache-2.0。

官方描述：OpenAI's Codex Security CLI and TypeScript SDK for finding, validating, and fixing security vulnerabilities. npm: https://www.npmjs.com/package/@openai/codex-security

Topics：`ai-security` `application-security` `cli` `code-scanning` `codex` `codex-security` `cybersecurity` `devsecops`

链接：[仓库](https://github.com/openai/codex-security) · [最新 Release](https://github.com/openai/codex-security/releases/tag/npm-v0.10.0) · [Homepage](https://developers.openai.com/codex/security)

---

## 速览

### 1. storytold/craft-anything

开源 Rust 引擎：检查网站、应用或游戏并让 AI 复刻

- 指标：⭐ 31,665 · 📈 日均 +2,262 · 🍴 6,488 · Rust · Apache-2.0 · 创建于 2026-10-31
- 上榜理由：创建以来日均 +2,262 Stars；创建 13 天的新项目；近 7 天发布 v0.6.1
- 适合谁：适合想研究网站、应用或游戏并快速生成可对照原型的开发者与创作者；不适合期待成熟稳定版或需要操作系统级隔离的人。
- 留意：README 标注 early alpha，且 Clean room 并非操作系统 sandbox，coding agent 仍以你的权限行动；许可证徽章写 MIT OR Apache-2.0，但仓库信息为 Apache-2.0，采用前需核对。
- 链接：[仓库](https://github.com/storytold/craft-anything) · [最新 Release](https://github.com/storytold/craft-anything/releases/tag/v0.6.1)

### 2. huamidev/GestaltX

iOS 27 MobileGestalt 编辑器，可实验区域码预设并备份

- 指标：⭐ 7,409 · 📈 日均 +1,482 · 🍴 2,606 · Swift · GPL-3.0 · 创建于 2026-11-09
- 上榜理由：创建以来日均 +1,482 Stars；创建仅 4 天的新项目；近 7 天发布 v1.1.1
- 适合谁：适合需要在 iOS/iPadOS 27.x 上实验 MobileGestalt 预设、能自行签名并承担设备风险的用户；不适合要求稳定生产、无备份恢复能力或使用不受支持系统的用户。
- 留意：采用前注意 GPL-3.0 许可证；仅支持 iOS/iPadOS 27.x，26.x 不支持；签名需证书和描述文件含可用 App Group，并同时签名 share extension。预设为实验性 flags，效果依赖设备和 OS，硬件身份恢复也仅支持 README 列出的部分 iPhone。
- 链接：[仓库](https://github.com/huamidev/GestaltX) · [最新 Release](https://github.com/huamidev/GestaltX/releases/tag/v1.1.1)

### 3. GoogleChrome/modern-web-guidance-src

帮 coding agent 避开旧模式的现代 Web 指南源仓库。

- 指标：⭐ 5,055 · 📈 今日 +1,925 · 🍴 277 · TypeScript · Apache-2.0 · 创建于 2026-01-28
- 上榜理由：GitHub Trending 今日 +1,925 Stars
- 适合谁：适合使用 coding agents 并希望其生成现代 Web 平台代码的 Web 开发者/团队；不适合不使用 coding agents 或只需手工查阅文档的人。
- 留意：采用前注意这是源仓库，README 未说明发布稳定性和兼容范围；许可证为 Apache-2.0，安装/试用依赖 npx 与网络，效果取决于 coding agent 集成。
- 链接：[仓库](https://github.com/GoogleChrome/modern-web-guidance-src) · [Homepage](https://goo.gle/modern-web-guidance)

### 4. Gathin23/cleanyourtv

ADB 停用 Android/Google TV 广告预装，装可恢复的干净启动器。

- 指标：⭐ 57,508 · 📈 日均 +2,054 · 🍴 7,440 · Python · 创建于 2026-10-17
- 上榜理由：创建以来日均 +2,054 Stars；创建 27 天的新项目
- 适合谁：适合愿意开启开发者选项、用电脑或编码助手折腾的 Android TV/Google TV 用户；不适合 Samsung、LG、Roku、Vizio、Hisense VIDAA 等非 Android 电视或不想改系统设置的人。
- 留意：License 未声明，复用或商用前需确认授权；运行依赖 Python 3、JDK 17–22、Android SDK platform 34/build-tools 34，且只适用于 Android TV/Google TV。禁用系统组件可能影响更新、语音或 Chromecast，README 称会先备份并可用一行恢复，但仍建议逐项确认。
- 链接：[仓库](https://github.com/Gathin23/cleanyourtv) · [最新 Release](https://github.com/Gathin23/cleanyourtv/releases/tag/v3.4.0) · [Homepage](https://cleanyour.tv)

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
