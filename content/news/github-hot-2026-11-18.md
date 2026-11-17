---
title: "GitHub 热点 2026-11-18｜Wireless-Device-Battery-Monitor：在Windows任务栏显示无线外设电量的轻量C++托盘工具，免厂商软件。"
date: "2026-11-18T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "C++"]
categories: ["日报"]
summary: "今日主推 krisgfx9/Wireless-Device-Battery-Monitor（日均 +2,561 Stars），速览 4 个：apkstart、LoopForge、last30days-skill 等。"
---

> 今日主推 krisgfx9/Wireless-Device-Battery-Monitor（日均 +2,561 Stars），速览 4 个：apkstart、LoopForge、last30days-skill 等。

## 今日主推：[krisgfx9/Wireless-Device-Battery-Monitor](https://github.com/krisgfx9/Wireless-Device-Battery-Monitor)

> 在Windows任务栏显示无线外设电量的轻量C++托盘工具，免厂商软件。

⭐ 2,561 · 📈 日均 +2,561 · 🍴 228 · C++ · GPL-3.0 · 创建于 2026-11-17

**为什么是今天**

- 创建以来日均 +2,561 Stars
- 创建仅 1 天的新项目
- 近 7 天发布 v1.0.7

**它解决什么问题**

解决无线鼠标、耳机、键盘和手柄的电量需要分别打开Logitech G HUB、Razer Synapse等厂商软件才能查看的问题；它把电量直接放到Windows任务栏。

**和同类相比**

README未说明与同类方案的直接对比；其特点是纯C++/Win32、约350 KB、约2 MB RAM、无运行时和后台服务，并直接读取多品牌设备HID报告。

**适合谁**

适合想在Windows 10/11任务栏集中查看多品牌无线外设电量、且不想常开厂商软件的用户；不适合需要非Windows平台或开箱即用支持所有设备的用户。

**最短上手**

```bash
下载最新Release的WirelessBattery-Setup
运行安装程序并按提示完成
或使用portable zip
源码构建：make或build.bat
```

**采用前留意**

License为GPL-3.0，修改或再分发需遵守其条款；README未说明项目成熟度与长期维护计划，且部分设备依赖厂商HID/虚拟COM协议（如ATK耳机需关闭桌面应用），兼容性可能受固件变化影响。另需注意README支持表存在重复行且可能被截断，选型前应核对具体型号。

官方描述：Show the battery level of wireless mice, headsets, keyboards and controllers on the Windows 10/11 taskbar. Lightweight tray app, no vendor software needed. Supports Logitech, Razer, SteelSeries, Corsair, HyperX, Glorious, PS4/PS5 DualSense, Xbox and Bluetooth devices.

链接：[仓库](https://github.com/krisgfx9/Wireless-Device-Battery-Monitor) · [最新 Release](https://github.com/krisgfx9/Wireless-Device-Battery-Monitor/releases/tag/v1.0.7)

---

## 速览

### 1. RoutineMiku/apkstart

Windows 上双击 APK，用自持运行时把安卓应用变独立窗口。

- 指标：⭐ 7,392 · 📈 近 24h +885 · 🍴 707 · JavaScript · MIT · 创建于 2026-10-29
- 上榜理由：近 24 小时 +885 Stars；创建 19 天的新项目；近 7 天发布 v0.5.8
- 适合谁：适合想在 Windows 10/11 x64 上以接近原生软件方式运行 APK 的用户；不适合需要稳定生产力、非 Windows x64 或不愿承担大体积运行时的用户。
- 留意：MIT 许可证；README 明确为早期版本、作者自娱自乐且暂时不是很好用；仅支持 Windows 10/11 x64，完整安装包约 1.3 GB，空闲预热约常驻 1 GB 内存。
- 链接：[仓库](https://github.com/RoutineMiku/apkstart) · [最新 Release](https://github.com/RoutineMiku/apkstart/releases/tag/v0.5.8)

### 2. Tencent/LoopForge

自托管 coding agent 工作流引擎，用 SOP 与人工审批把关交付。

- 指标：⭐ 3,085 · 📈 今日 +590 · 🍴 436 · Go · 创建于 2026-07-28
- 上榜理由：GitHub Trending 今日 +590 Stars；近 3 天 +2,217 Stars；近 7 天发布 v0.4.0
- 适合谁：适合需要自托管、可审计、多人审批的团队；不适合只想临时对话改代码、不愿维护 Docker 服务的个人。
- 留意：仓库元数据未声明 License，README 徽章显示 MIT，采用前应以 LICENSE 文件为准；项目创建于 2026-07-28，较新，且依赖 Docker、外网下载、模型 API key 与 GitHub 授权。
- 链接：[仓库](https://github.com/Tencent/LoopForge) · [最新 Release](https://github.com/Tencent/LoopForge/releases/tag/v0.4.0) · [Homepage](https://loopforge.cn)

### 3. mvanhorn/last30days-skill

跨多平台做近30天调研的 AI agent skill，按真实互动排序并综合摘要。

- 指标：⭐ 68,992 · 📈 今日 +772 · 🍴 6,144 · Python · MIT · 创建于 2026-01-24
- 上榜理由：GitHub Trending 今日 +772 Stars；近 7 天发布 v4.3.2
- 适合谁：适合需要会前调研、趋势追踪或多平台社区信号汇总的开发者与研究、销售场景；不适合要求零配置、结果可完全复现或严格学术引用的用户。
- 留意：MIT 许可；项目创建于 2026-01-23，较新，README 未说明成本、速率限制和长期维护承诺。部分数据源依赖 API key、登录会话、PATH 中的 CLI 或本地服务，采用前需评估 auth、rate limit 和稳定性。
- 链接：[仓库](https://github.com/mvanhorn/last30days-skill) · [最新 Release](https://github.com/mvanhorn/last30days-skill/releases/tag/v4.3.2)

### 4. heygen-com/hyperframes

用 HTML/CSS 渲染确定性 MP4，并让 AI agent 参与视频制作。

- 指标：⭐ 85,955 · 📈 近 24h +734 · 🍴 7,964 · TypeScript · Apache-2.0 · 创建于 2026-03-10
- 上榜理由：近 24 小时 +734 Stars；近 4 天 +1,922 Stars；近 7 天发布 v0.9.64
- 适合谁：适合前端/创意开发者以及使用 Claude Code、Codex、Cursor 等 agent 做视频自动化的用户，不适合需要传统非线性剪辑或 README 未说明的高级后期能力的人。
- 留意：采用前注意需要 Node.js >=22；Studio 免费，但 Pro 计划会接入 HeyGen 的付费视频、图像、语音和音乐模型。README 未说明渲染性能、平台兼容性和资源开销细节。
- 链接：[仓库](https://github.com/heygen-com/hyperframes) · [最新 Release](https://github.com/heygen-com/hyperframes/releases/tag/v0.9.64) · [Homepage](https://hyperframes.heygen.com)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [dream-num/univer](https://github.com/dream-num/univer) | 28,878 | 今日 +1,776 | 2026-11-16 |
| [ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go) | 25,971 | 近 24h +1,226 | 2026-11-15 |
| [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | 19,968 | 今日 +1,444 | 2026-11-17 |
| [libracoder/kiri](https://github.com/libracoder/kiri) | 10,068 | 近 24h +1,242 | 2026-11-17 |
| [stablyai/orca](https://github.com/stablyai/orca) | 127,797 | 近 24h +1,060 | 2026-11-16 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
