# 信息图 Prompt 规范

> 给博客文章配 6 张"手绘教育风"信息图的标准化做法。下次写新文章想配图，从这里开始。

## 这是什么

一套可复用的信息图生成 prompt 体系，使用 `baoyu-image-gen`（OpenRouter / Gemini Flash Image 等模型）输出 16:9 中文信息图。整体风格统一为 **hand-drawn-edu**：warm cream 背景 + macaron 配色 + charcoal 手绘抖动线条 + stick figures / doodle icons。

实际效果可参考已发布的文章（见 [EXAMPLES.md](EXAMPLES.md)）。

## 文件导航

| 文件 | 用途 |
|---|---|
| [SPEC.md](SPEC.md) | 完整规范：颜色、6 种布局、prompt 模板、工作流、常见坑 |
| [EXAMPLES.md](EXAMPLES.md) | 案例索引：按布局类型查阅历史 prompt 实例与成图 |

## 何时用

- 写新博客文章，需要配 4-8 张论点信息图时
- 想复用统一视觉语言（让所有文章封面 / 配图风格一致）
- 给汇报、笔记、文档配信息密度高的概念图

## 怎么用

1. 读 [SPEC.md](SPEC.md) 的"工作流"一节（5 分钟）
2. 按章节论点选 layout（参考"6 种布局"对照表）
3. 套 prompt 模板填空（参考 EXAMPLES 里同 layout 的案例）
4. `bun ~/.claude/skills/baoyu-image-gen/scripts/main.ts --promptfiles <prompt.md> --image <out.png> --ar 16:9 --provider openrouter`
5. PNG → JPEG (quality 82) → 入仓
