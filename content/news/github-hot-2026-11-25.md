---
title: "GitHub 热点 2026-11-25｜VIctory：Rust在Windows原生运行自备GTA VI Xbox文件，技术探索…"
date: "2026-11-25T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Rust"]
categories: ["日报"]
summary: "今日主推 Marvisak/VIctory（近 24h +10,443 Stars），速览 4 个：fast-anything、xnulinux、xcl 等。"
---

> 今日主推 Marvisak/VIctory（近 24h +10,443 Stars），速览 4 个：fast-anything、xnulinux、xcl 等。

## 今日主推：[Marvisak/VIctory](https://github.com/Marvisak/VIctory)

> Rust在Windows原生运行自备GTA VI Xbox文件，技术探索价值高

⭐ 11,185 · 📈 近 24h +10,443 · 🍴 1,633 · Rust · GPL-3.0 · 创建于 2026-11-24

**为什么是今天**

- 近 24 小时 +10,443 Stars
- 创建仅 1 天的新项目

**它解决什么问题**

项目尝试在 Windows 上原生运行用户自备的 GTA VI Xbox Series X|S 文件，由 VIctory 提供底层平台、数据转换和 D3D12 渲染路径。当前目标是让游戏启动、菜单、加载和世界场景逐步跑通，而不是提供可直接游玩的成品。

**和同类相比**

README 未说明与同类方案的直接对比；其特点是把游戏 x86-64 代码原样运行在本进程，并提前转换着色器和管线。取舍是当前世界场景仅 1-2 秒每帧，光照与部分几何缺失，真实查询、HDR、缩放等也未完成。

**适合谁**

适合关注主机游戏加载/移植、DXIL 着色器转换、D3D12 与 Rust 工程实践的技术研究者；不适合想现在正常游玩 GTA VI 的玩家。

**最短上手**

```bash
copy victory.example.toml victory.toml
cargo run -p victory -- config
cargo build --release -p victory
target\release\victory.exe run <game dir>\<the title's exe> --execute
```

**采用前留意**

项目明确标注 Not playable yet：世界渲染 1-2 秒/帧且存在画面缺陷，仅在单台 Windows 11 + RX 6700 XT 机器上测试；进入世界曾导致 GPU hang 和显示驱动重置。许可证为 GPL-3.0，需用户自备游戏文件，README 未说明相关法律授权安排。

官方描述：An attempt at running GTA VI on PC

链接：[仓库](https://github.com/Marvisak/VIctory)

---

## 速览

### 1. EL4CTEO/fast-anything

面向多语言的局部 Rust 加速工具，用真实调用验证热点函数移植。

- 指标：⭐ 3,582 · 📈 近 24h +494 · 🍴 255 · Rust · MIT · 创建于 2026-11-21
- 上榜理由：近 24 小时 +494 Stars；近 2 天 +1,758 Stars；创建仅 3 天的新项目；近 7 天发布 v0.8.7
- 适合谁：适合已有 Python、Node/TypeScript、Ruby、Java/Kotlin、Go、PHP、C/C++、C# 或 R 应用并想局部提速的开发者；不适合需要零依赖或要移植非确定性、非纯数据函数的人。
- 留意：许可证为 MIT；采用前需准备 Rust 工具链，部分语言依赖 FFI 或特定运行时版本（如 PHP 需 ffi 扩展），README 未说明长期维护与安全审计情况。
- 再次上榜：2026-11-23 推荐过，发布新版本 v0.8.7
- 链接：[仓库](https://github.com/EL4CTEO/fast-anything) · [最新 Release](https://github.com/EL4CTEO/fast-anything/releases/tag/v0.8.7) · [Homepage](https://www.npmjs.com/package/@el4cteo/fast-anything)

### 2. AFK-surf/xnulinux

把 XNU 作为 Linux 内核模块加载，在 arm64 Linux 上原生运行 macOS 用户态

- 指标：⭐ 3,316 · 📈 近 24h +1,371 · 🍴 148 · Objective-C++ · 创建于 2026-11-20
- 上榜理由：近 24 小时 +1,371 Stars；创建仅 4 天的新项目
- 适合谁：适合有 arm64 硬件（Apple Silicon 或 DGX Spark）、愿意自建工具链的内核与系统层爱好者；不适合需要稳定生产环境、缺少 Mac 与 Xcode，或使用 x86 机器的人。
- 留意：仓库整体 License 未声明，仅说明各源码文件带 SPDX 标识（如 fki-ko/、linux/ 为 GPL-2.0-only），商用前需自行确认。项目创建于 2026-11-20、极为早期，依赖自备 macOS 27 安装盘与 Xcode、至少 16 GB 内存，并包含多处生产化尚未完成的临时方案。
- 链接：[仓库](https://github.com/AFK-surf/xnulinux)

### 3. xcl-dev/xcl

原生运行 Xbox Series 游戏的兼容层，重编译 RDNA2 着色器

- 指标：⭐ 7,772 · 📈 日均 +1,943 · 🍴 1,018 · Rust · GPL-2.0 · 创建于 2026-11-21
- 上榜理由：创建以来日均 +1,943 Stars；创建仅 4 天的新项目
- 适合谁：适合拥有已解包 Xbox Series 游戏、愿意在 Windows 上做兼容性测试的开发者和技术用户；不适合期望一键运行未解包或受 DRM 保护游戏的普通玩家。
- 留意：项目采用 GPL-2.0，采用前需评估许可证义务；README 显示兼容性仍按游戏和功能分项，部分管线会被拒绝，且只支持已解包且自有的游戏，不提供下载、解密、解包或 DRM 绕过。它还依赖系统或 Windows SDK 的 XGameRuntime、XAudio2、D3D12、DXC，不随项目分发。
- 链接：[仓库](https://github.com/xcl-dev/xcl) · [Homepage](https://discord.gg/xcl)

### 4. ersinkoc/phonebox

旧 Android 手机变身电脑桌面触控面板，支持 USB/Wi-Fi 与可视化编辑

- 指标：⭐ 5,986 · 📈 近 24h +549 · 🍴 728 · JavaScript · MIT · 创建于 2026-11-08
- 上榜理由：近 24 小时 +549 Stars；创建 17 天的新项目；近 7 天发布 v0.9.29
- 适合谁：适合有旧 Android 手机、想给 Windows/Linux/macOS 加桌面控制面板的开发者或 Home Assistant 用户；不适合 iOS 用户或不愿安装桌面 agent/APK 的人。
- 留意：MIT 许可证；Windows release agent 仍未签名，SmartScreen 或杀软可能警告或拦截；手机 app 不在应用商店、仅从 GitHub Releases 获取，需自行确认 APK 来源。
- 链接：[仓库](https://github.com/ersinkoc/phonebox) · [最新 Release](https://github.com/ersinkoc/phonebox/releases/tag/v0.9.29) · [Homepage](https://ersinkoc.github.io/phonebox/)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [google-gemini/gemini-api-cli](https://github.com/google-gemini/gemini-api-cli) | 2,278 | 近 24h +1,206 | 2026-11-09 |
| [stablyai/orca](https://github.com/stablyai/orca) | 136,009 | 近 24h +1,576 | 2026-11-16 |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 21,379 | 今日 +1,833 | 2026-11-19 |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | 5,813 | 今日 +936 | 2026-11-20 |
| [mdiri-ai/SoduWork](https://github.com/mdiri-ai/SoduWork) | 7,607 | 近 24h +558 | 2026-11-22 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
