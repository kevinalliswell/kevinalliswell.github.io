---
title: "GitHub 热点 2026-11-24｜Leonida：Xbox 版 GTA VI 的静态重编译项目，把主机代码原生跑在 Win…"
date: "2026-11-24T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Python"]
categories: ["日报"]
summary: "今日主推 ProjectLeonida/Leonida（日均 +11,192 Stars），速览 4 个：ARTEX、agy-fast、agent_skills 等。"
---

> 今日主推 ProjectLeonida/Leonida（日均 +11,192 Stars），速览 4 个：ARTEX、agy-fast、agent_skills 等。

## 今日主推：[ProjectLeonida/Leonida](https://github.com/ProjectLeonida/Leonida)

> Xbox 版 GTA VI 的静态重编译项目，把主机代码原生跑在 Windows 上，但还开不了机

⭐ 33,575 · 📈 日均 +11,192 · 🍴 3,041 · Python · GPL-3.0 · 创建于 2026-11-21

**为什么是今天**

- 创建以来日均 +11,192 Stars
- 创建仅 3 天的新项目

**它解决什么问题**

让 Xbox Series 版游戏的可执行代码、RDNA2 GPU 程序与资源包在 PC 上原生运行：游戏代码按 x86-64 直接加载执行，主机系统软件被重新实现，着色器翻译为 SPIR-V 交给 Vulkan，模型、纹理与音频从玩家自己的游戏包中读取。

**和同类相比**

走静态重编译路线而非模拟器，因此依赖 x86-64 与 PC 同构这一点；所有产物（着色器、资源、运行时目录、存档）都在本地由玩家自有副本生成，仓库不提供游戏、密钥或可执行文件，也不绕过任何保护。

**适合谁**

适合愿意自备 Xbox Series 1.0.2.1 游戏副本、能读 C++/Python 工具链并想参与着色器翻译与 D3D12→Vulkan 层工作的开发者；不适合只想直接玩到游戏的普通玩家。

**最短上手**

```bash
README 未说明具体构建命令（提供的 README 中 How to build 章节被截断）
需自备 Xbox Series 版本 1.0.2.1 的游戏副本，且文件已在磁盘上可读
运行时入口在 README 中提到为 gta6rt --run，但完整步骤 README 未说明
```

**采用前留意**

项目处于极早期：游戏尚不能启动，PE loader 与 D3D12 层均未对真实可执行文件验证。许可证为 GPL-3.0，有 copyleft 约束；同时需自行合法持有游戏副本，仓库不含游戏、密钥或绕过保护的手段。

官方描述：Leonida Is A Native PC Recompilation Of The Xbox Version Of Grand Theft Auto 6

链接：[仓库](https://github.com/ProjectLeonida/Leonida)

---

## 速览

### 1. BaaRai/ARTEX

自托管 LLM 多智能体渗透测试平台，每个发现都绑定可复核的流量证据。

- 指标：⭐ 17,662 · 📈 近 24h +1,333 · 🍴 6,544 · Go · AGPL-3.0 · 创建于 2026-10-09
- 上榜理由：近 24 小时 +1,333 Stars；近 3 天 +3,998 Stars；近 7 天发布 v0.7.0
- 适合谁：适合需要自建环境、看重证据链与人工审批的红队与漏洞赏金团队，不适合想要开箱即用托管服务或不愿维护数据库与模型接入的个人用户。
- 留意：许可证为 AGPL-3.0，对外提供服务或分发时需评估其传染性义务；仓库创建于 2026-10-08，属较新项目，且 README 说明 v0.7.0 早于镜像发布步骤，需本地构建，成熟度与镜像可用性需自行验证。
- 链接：[仓库](https://github.com/BaaRai/ARTEX) · [最新 Release](https://github.com/BaaRai/ARTEX/releases/tag/v0.7.0)

### 2. INK-Q/agy-fast

零依赖 Antigravity MCP 加速插件，批处理工具调用以降低延迟和 token 配额。

- 指标：⭐ 775 · 📈 近 24h +278 · 🍴 45 · TypeScript · MIT · 创建于 2026-11-19
- 上榜理由：近 24 小时 +278 Stars；创建仅 4 天的新项目；近 7 天发布 v0.3.0
- 适合谁：适合使用 Google Antigravity CLI/Desktop/IDE 并希望减少延迟、token 配额和上传流量的开发者；不适合不用 Antigravity 或需要通用非 MCP 方案的人。
- 留意：采用前注意它强依赖 Antigravity 插件/MCP 接口，且性能数据来自作者对 55 个会话的分析，README 未说明第三方独立复现。使用 --dangerously-skip-permissions 会跳过工具权限确认，应仅在可信仓库或配合 --sandbox 使用；许可证为 MIT。
- 链接：[仓库](https://github.com/INK-Q/agy-fast) · [最新 Release](https://github.com/INK-Q/agy-fast/releases/tag/v0.3.0)

### 3. janestreet/agent_skills

Jane Street 开源的 AI agent 技能集，含苏格拉底式导师技能。

- 指标：⭐ 11,337 · 📈 近 24h +679 · 🍴 779 · Unknown · MIT · 创建于 2026-11-04
- 上榜理由：近 24 小时 +679 Stars；近 7 天 +1,767 Stars；创建 20 天的新项目
- 适合谁：适合使用支持 SKILL.md 的 coding agent，或想用聊天机器人进行苏格拉底式教学的人；不适合寻找多技能集合或希望提交新技能/修改现有文本的贡献者。
- 留意：MIT 许可证；目前 README 仅列出一个技能，且说明 issues 不一定能全部处理，采用前需确认目标 agent 对 SKILL.md 的支持方式。
- 链接：[仓库](https://github.com/janestreet/agent_skills)

### 4. cathrynlavery/diagram-design

面向编程 Agent 的图表技能，输出自包含 HTML+SVG，含 52 种图表类型。

- 指标：⭐ 70,926 · 📈 今日 +624 · 🍴 4,746 · HTML · MIT · 创建于 2026-04-17
- 上榜理由：GitHub Trending 今日 +624 Stars；近 7 天 +3,293 Stars
- 适合谁：适合使用 Claude Code、Codex、Cursor 等 Agent Skills 宿主并需要快速产出品牌化图表的开发者；不适合无法使用 Agent Skills 宿主或只想传统手动画图的用户。
- 留意：MIT 许可证风险较低；采用前需确认宿主支持 Agent Skills，Claude Desktop 需按 README 构建受限 ZIP，且技能会联网，建议先阅读 PRIVACY.md。
- 链接：[仓库](https://github.com/cathrynlavery/diagram-design) · [Homepage](https://diagramdesign.dev)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [EL4CTEO/fast-anything](https://github.com/EL4CTEO/fast-anything) | 3,088 | 近 24h +1,264 | 2026-11-23 |
| [stablyai/orca](https://github.com/stablyai/orca) | 134,433 | 近 24h +1,503 | 2026-11-16 |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 19,662 | 今日 +2,037 | 2026-11-19 |
| [erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything) | 8,687 | 近 24h +720 | 2026-11-22 |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | 4,912 | 今日 +755 | 2026-11-20 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
