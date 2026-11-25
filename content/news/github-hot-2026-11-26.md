---
title: "GitHub 热点 2026-11-26｜mobile-agent-testers：免写测试脚本，在 GitHub Actions 并行跑多手机 Claud…"
date: "2026-11-26T07:00:00+08:00"
draft: false
tags: ["GitHub", "开源", "日报", "Python"]
categories: ["日报"]
summary: "今日主推 pierridotite/mobile-agent-testers（近 24h +605 Stars），速览 4 个：victory-fork、portwatch-vi、math 等。"
---

> 今日主推 pierridotite/mobile-agent-testers（近 24h +605 Stars），速览 4 个：victory-fork、portwatch-vi、math 等。

## 今日主推：[pierridotite/mobile-agent-testers](https://github.com/pierridotite/mobile-agent-testers)

> 免写测试脚本，在 GitHub Actions 并行跑多手机 Claude Code agent 做探索式测试。

⭐ 2,294 · 📈 近 24h +605 · 🍴 233 · Python · MIT · 创建于 2026-11-17

**为什么是今天**

- 近 24 小时 +605 Stars
- 近 3 天 +1,815 Stars
- 创建 9 天的新项目
- 近 7 天发布 v0.2.0

**它解决什么问题**

移动端探索式测试往往要写脚本，也难以并行覆盖多语言、大字体、不同屏幕与无障碍场景；该项目让多个 persona agent 在模拟器/仿真器上像新用户一样操作，并产出带截图的 bug 报告。

**和同类相比**

与 Maestro/Appium 执行预先编写的测试不同，它让 AI agent 探索并发现没人想到要测的问题；Android 还能把路径编译为 Maestro flow 回放，但该能力目前仅 Android，ECR 为早期草案。

**适合谁**

适合希望用 AI 补充多设备探索式移动测试的团队；不适合需要稳定自动化回归断言或不愿承担模型调用成本的人。

**最短上手**

```bash
gh repo create my-testers --public --template pierridotite/mobile-agent-testers --clone
cd my-testers && ./setup.sh
gh workflow run agent-testers.yml
bash scripts/collect.sh <run id>
```

**采用前留意**

MIT 许可证；README 未说明项目成熟度与维护承诺，运行依赖 GitHub Actions 与 Claude/Anthropic 兼容模型，public repo runner 免费但模型调用需付费（示例约 $0.15–$0.55/phone），发现质量取决于模型读图能力。

官方描述：20 AI testers on 20 different phones, in parallel, on GitHub's free runners: Claude Code agents on iOS Simulators and Android emulators that find broken flows, translation, layout and accessibility bugs

Topics：`accessibility-testing` `ai-agents` `ai-testing` `android` `android-emulator` `claude` `claude-code` `e2e-testing`

链接：[仓库](https://github.com/pierridotite/mobile-agent-testers) · [最新 Release](https://github.com/pierridotite/mobile-agent-testers/releases/tag/v0.2.0)

---

## 速览

### 1. fxceless/victory-fork

Xbox Series 游戏的 Windows 兼容层 WIP fork，专注渲染修复

- 指标：⭐ 3,037 · 📈 近 24h +1,483 · 🍴 869 · Rust · GPL-3.0 · 创建于 2026-11-25
- 上榜理由：近 24 小时 +1,483 Stars；创建仅 1 天的新项目
- 适合谁：适合研究 Xbox 兼容层、Direct3D 12 与 shader recompiler 的开发者；不适合想直接玩游戏的普通用户。
- 留意：GPL-3.0 许可证；项目为 WIP，当前约 8 到 10 fps、阴影区域全黑，仅在一台 Windows 11 机器上验证，且需要自备游戏文件。
- 链接：[仓库](https://github.com/fxceless/victory-fork)

### 2. 4lwayz/portwatch-vi

追踪GTA VI社区PC重编译/模拟进展的静态站点，统一阶梯评分并每3小时刷新。

- 指标：⭐ 4,024 · 📈 近 24h +1,268 · 🍴 118 · JavaScript · 创建于 2026-11-22
- 上榜理由：近 24 小时 +1,268 Stars；创建仅 3 天的新项目
- 适合谁：适合关注GTA VI PC移植/模拟社区进展的读者和项目维护者；不适合想下载游戏文件或可执行文件的人。
- 留意：README未声明许可证，采用或复用代码前需确认授权；站点依赖GitHub Actions、外部数据源和可选付费API（如Claude、X），自动生成内容需复核。
- 链接：[仓库](https://github.com/4lwayz/portwatch-vi) · [Homepage](portwatch-vi.xyz)

### 3. openai/math

OpenAI 内部模型生成的数学手稿与 Lean 形式化集合，可观察模型数学研究产出。

- 指标：⭐ 18,316 · 📈 近 24h +581 · 🍴 2,029 · Lean · Apache-2.0 · 创建于 2026-10-07
- 上榜理由：近 24 小时 +581 Stars；来自重点官方组织
- 适合谁：适合数学研究者、Lean formalization 研究者和模型评测人员查阅；不适合需要同行评审级结论或生产级可靠性的读者。
- 留意：部分未形式化结果可能存在错误，README 明确说会尽快修复；采用前需独立核查数学论证和 Lean 构建，不能把仓库内容当作已同行评审结论。许可证为 Apache-2.0，README 未说明其他依赖或成本。
- 链接：[仓库](https://github.com/openai/math)

### 4. erkamyaman/rust-anything

用行为录制校验多语言应用逐步重写为 Rust 的迁移工具

- 指标：⭐ 9,586 · 📈 近 24h +395 · 🍴 784 · Rust · MIT · 创建于 2026-11-16
- 上榜理由：近 24 小时 +395 Stars；近 7 天 +6,301 Stars；创建 9 天的新项目；近 7 天发布 v4.2.0
- 适合谁：适合需要把现有 CLI、HTTP server 或 library 逐步迁移到 Rust 并做行为校验的团队；不适合期望全自动代码翻译或不愿维护录制与测试的人。
- 留意：采用前需确认录制用例是否覆盖目标行为，因为一致性校验依赖录制回放；项目成熟度与长期维护 README 未说明，且流程涉及 coding agent、FFI 和多语言运行时依赖。
- 再次上榜：2026-11-22 推荐过，发布新版本 v4.2.0
- 链接：[仓库](https://github.com/erkamyaman/rust-anything) · [最新 Release](https://github.com/erkamyaman/rust-anything/releases/tag/v4.2.0) · [Homepage](rust-anything.com)

---

## 持续关注

近 30 天内已推荐过、今天仍在快速增长的项目，不再重复介绍：

| 项目 | Stars | 增长 | 上次推荐 |
|------|-------|------|----------|
| [stablyai/orca](https://github.com/stablyai/orca) | 137,903 | 近 24h +1,894 | 2026-11-16 |
| [google-gemini/gemini-api-cli](https://github.com/google-gemini/gemini-api-cli) | 3,019 | 近 24h +741 | 2026-11-09 |
| [Marvisak/VIctory](https://github.com/Marvisak/VIctory) | 12,573 | 近 24h +1,388 | 2026-11-25 |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | 6,449 | 今日 +853 | 2026-11-20 |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 22,913 | 今日 +1,644 | 2026-11-19 |

---

## 筛选方法

- 候选来源：GitHub Trending 日榜、近 30 天新建仓库、AI 主题关键词与重点 owner 的活跃仓库。
- 排序依据：以 Stars **增量**为主（Trending 当日增量 → 每日快照差值 → 新仓库日均），总量、owner、主题只做小幅加分。
- 去重规则：推荐过的仓库 30 天内不再进入正文，除非发布了新的大版本；同一 owner 每天最多 1 个。
- 点评由 LLM 基于仓库 README 生成，可能存在偏差，请以仓库原文为准。
- 数据来源：GitHub Search API、GitHub Trending、仓库 README 与 Release 页面。
