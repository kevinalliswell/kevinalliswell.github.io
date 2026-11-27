---
title: "GitHub 热点 2026-11-28｜VIctory-NVIDIA：把 Xbox Series 游戏跑在 Windows 上、专为 NVID…"
date: "2026-11-28T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Rust"]
categories: ["日报"]
summary: "今日主推 trustno1-coder/VIctory-NVIDIA（日均 +1,470 Stars），速览 4 个：magpie、windows-titlebar-blur-customizer、KuroCat 等。"
---

> 今日主推 trustno1-coder/VIctory-NVIDIA（日均 +1,470 Stars），速览 4 个：magpie、windows-titlebar-blur-customizer、KuroCat 等。

## 今日主推：[trustno1-coder/VIctory-NVIDIA](https://github.com/trustno1-coder/VIctory-NVIDIA)

> 把 Xbox Series 游戏跑在 Windows 上、专为 NVIDIA RTX 调优的兼容层

⭐ 2,940 · 📈 日均 +1,470 · 🍴 1,009 · Rust · GPL-3.0 · 创建于 2026-11-26

**为什么是今天**

- 创建以来日均 +1,470 Stars
- 创建仅 1 天的新项目
- 近 7 天发布 v2026.11.27.7

**它解决什么问题**

让玩家用自己 dump 的 Xbox Series 版游戏文件在 Windows 上原生运行，并针对 NVIDIA RTX 显卡配置 DLSS 超分、帧生成与 2560x1440 画质/帧率。

**和同类相比**

是 Marvisak/VIctory 的 fork，把多个上游项目合并后逐项实测再选定基线，只面向 NVIDIA RTX 调优，并提供 F1 设置菜单与 F3 统计面板；代价是需要自备游戏 dump，且不含任何游戏或 NVIDIA/AMD 文件，首次启动还要额外下载依赖。

**适合谁**

适合持有该游戏合法副本、有 RTX 显卡且愿意折腾 dump、驱动与 Runtime 的 Windows 用户；不适合想要开箱即用、使用非 NVIDIA 显卡或没有游戏文件的用户。

**最短上手**

```bash
从 latest release 下载 victory.exe
放入自己 dump 的 Xbox Series 构建 v1.0.2.1 文件夹，与 game_scarlett_master.exe 同目录
双击 victory.exe（未签名，需 More info → Run anyway）
首次启动按提示确认下载 NVIDIA DLSS/帧生成文件（约 70 MB）
```

**采用前留意**

许可证为 GPL-3.0 的 fork，仓库不含游戏文件，需自行合法获取；项目创建时间很新、README 明确只在 RTX 50 上实测，Windows 10 还需另下 D3D12 Agility SDK，且每个新版本首次启动会以约 14 fps 运行并自动重启一次。

官方描述：VIctory (Xbox Series compatibility layer) tuned for NVIDIA RTX cards: Series X at 2560x1440 with DLSS, about 26-30 fps on an RTX 5070, DLSS frame generation 2x-6x, an F1 settings menu and F3 stats panel, open water without dark blocks. Built on many repos combined into one. No game files or NVIDIA files included.

Topics：`compatibility-layer` `directx-12` `dlss` `frame-generation` `nvidia` `rust`

链接：[仓库](https://github.com/trustno1-coder/VIctory-NVIDIA) · [最新 Release](https://github.com/trustno1-coder/VIctory-NVIDIA/releases/tag/v2026.11.27.7)

---

## 速览

### 1. yetone/magpie

把多个 AI 订阅账户汇总为一个本地池，供任意 agent 使用

- 指标：⭐ 42,515 · 📈 近 24h +506 · 🍴 3,909 · Go · MIT · 创建于 2026-09-24
- 上榜理由：近 24 小时 +506 Stars；近 7 天发布 v0.1.4985
- 适合谁：适合同时使用多个 agent、多个 provider 或多个账号的人；只用单一 agent 且其原生订阅足够的人不需要。
- 留意：License 为 MIT，但仓库创建于 2026-09-23，成熟度与长期维护情况 README 未说明；默认会读取 Claude Code、Codex 的登录文件及 Keychain 来发现订阅账号，可在 Settings → Privacy 或通过 `magpie accounts discovery off` 关闭；安装方式为 `curl | sh`，脚本还会调用包管理器并改动 agent 配置，建议先审阅脚本。
- 链接：[仓库](https://github.com/yetone/magpie) · [最新 Release](https://github.com/yetone/magpie/releases/tag/v0.1.4985) · [Homepage](https://usemagpie.ai)

### 2. Pixel679-cmyk/windows-titlebar-blur-customizer

开源 Windows 标题栏模糊定制工具，支持 Aero、Acrylic、Mica。

- 指标：⭐ 1,505 · 📈 日均 +1,505 · 🍴 0 · C++ · MIT · 创建于 2026-11-27
- 上榜理由：创建以来日均 +1,505 Stars；创建仅 1 天的新项目；近 7 天发布 v4.4.2
- 适合谁：适合希望调整 Windows 10 2004+ 或 Windows 11 标题栏视觉效果的桌面定制用户；不适合非 Windows 环境或需要改变单个应用完整界面的用户。
- 留意：仓库信息标注 MIT，但 README 徽章写 LGPL-3.0，采用前需核实实际许可证；效果受 Windows 版本、应用渲染方式和第三方主题影响，且运行包需保留 libvlc.dll。
- 链接：[仓库](https://github.com/Pixel679-cmyk/windows-titlebar-blur-customizer) · [最新 Release](https://github.com/Pixel679-cmyk/windows-titlebar-blur-customizer/releases/tag/v4.4.2)

### 3. qianyiai/KuroCat

开源 3D/2D 桌面打字猫与 AI 编程伴侣，Rust + Tauri v2 轻量跨平台

- 指标：⭐ 1,758 · 📈 近 24h +425 · 🍴 248 · TypeScript · MIT · 创建于 2026-11-21
- 上榜理由：近 24 小时 +425 Stars；创建仅 6 天的新项目；近 7 天发布 v5.1.3
- 适合谁：适合想要桌面宠物、直播打字可视化或键鼠互动装饰的开发者与主播；不适合不愿授予全局键盘/鼠标监控权限或需要企业级支持的用户。
- 留意：许可证为 MIT；README 明确警示仿冒站点 kurocat.net 分发带填充文件的非官方安装包，务必只从 kurocat.org、官方 GitHub Releases 或 Homebrew Tap 获取。macOS 需开启辅助功能与输入监控权限，AI/MCP 相关依赖与成本 README 未说明。
- 链接：[仓库](https://github.com/qianyiai/KuroCat) · [最新 Release](https://github.com/qianyiai/KuroCat/releases/tag/v5.1.3) · [Homepage](https://kurocat.org)

### 4. alesha-pro/llm.asm

纯x86-64汇编实现Qwen3推理、裸机OS和Mini-GPT训练，体积仅KB级。

- 指标：⭐ 2,165 · 📈 近 24h +705 · 🍴 328 · Assembly · MIT · 创建于 2026-11-25
- 上榜理由：近 24 小时 +705 Stars；创建仅 2 天的新项目
- 适合谁：适合对汇编、LLM推理/训练底层实现和bare-metal OS感兴趣的研究者或极客；不适合需要跨平台、快速集成或长期生产维护的团队。
- 留意：许可证为MIT；项目创建于2026-11-25，README未说明维护计划与生产支持，且需要AVX2/FMA/F16C硬件并自行导出模型权重（约614 MiB）。
- 链接：[仓库](https://github.com/alesha-pro/llm.asm)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [stablyai/orca](https://github.com/stablyai/orca) | 142,413 | 近 24h +2,098 | 2026-11-16 |
| [github/spec-kit](https://github.com/github/spec-kit) | 152,282 | 近 24h +682 | 2026-11-27 |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 26,013 | 今日 +1,615 | 2026-11-19 |
| [mdiri-ai/SoduWork](https://github.com/mdiri-ai/SoduWork) | 8,752 | 近 24h +519 | 2026-11-22 |
| [google-gemini/gemini-api-cli](https://github.com/google-gemini/gemini-api-cli) | 4,202 | 近 24h +458 | 2026-11-09 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
