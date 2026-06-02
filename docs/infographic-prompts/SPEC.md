# 信息图 Prompt 规范（hand-drawn-edu）

## 设计哲学

- **手绘 ≠ 业余**：所有线条都是手绘抖动质感（charcoal #2D2D2D），但布局必须严谨对称、信息层级清晰。
- **马卡龙 + 暖米色**：低饱和柔色给"教育友好"基调，避免过于商务/严肃。
- **中文为主，技术术语保留英文**：标签优先中文（如"先验目标"），公认术语保留英文（OKR / MVP / Cynefin）。
- **信息密度优先于美感**：每张图都要扛起一个完整论点，不是装饰。
- **图标语言统一**：stick figures、五角星、doodle 箭头、小气泡——别混入写实风或 3D。

---

## 颜色规范

| 名称 | Hex | 语义用途 |
|---|---|---|
| Warm Cream | `#F5F0E8` | **背景**（所有图统一） |
| Charcoal | `#2D2D2D` | **所有线条/文字**（统一） |
| Coral Red | `#E8655A` | **强调/中心节点/警示/不可逆/end-first** |
| Macaron Blue | `#A8D8EA` | **工程 / 技术 / 战略锚定 / 纪律** |
| Macaron Mint | `#B5E5CF` | **积极 / 解决方案 / 涌现 / start-first** |
| Macaron Lavender | `#D5C6E0` | **抽象 / 概念 / 整合 / 元层级** |
| Macaron Peach | `#FFD5C2` | **温暖 / 人物 / 案例 / 生活** |

**颜色语义分配原则**：

1. **中心强调用 Coral**（最醒目，每张图一个 focal point）
2. **左右/对立用 Mint vs Coral 或 Mint vs Blue**（视情绪色调）
3. **抽象总结/元概念用 Lavender**（顶部 banner、底部 summary、中间桥接）
4. **案例/人物卡用 Peach**（小卡片、附录、引用）
5. **同一张图最多用 4 种 macaron 色 + Coral 强调**，避免色彩噪音

---

## 6 种布局对照

| 布局 | 适用内容 | 视觉结构 | 易踩坑 |
|---|---|---|---|
| `hub-spoke` | 中心概念 + 4-6 子要素 | 中央 hub + 辐射 spokes，每 spoke 含 2-3 子项 | spoke 数量超过 6 拥挤；spoke 之间没有视觉差异 |
| `binary-comparison` | A vs B 对立 / 误解 vs 真相 | 中央垂直分隔线（虚线/太极/桥），左右对称 | 两侧权重不均；中间分隔过粗 |
| `bento-grid` | 4-6 个并列案例/失效模式 | 2×2 / 2×3 / 2×4 等大小格子，每格独立小标题 | 每格内容字数不均；缺少格间视觉节奏 |
| `linear-progression` | 时间轴 / 步骤 / 演化 | 横向 4-6 节点，箭头串联 | 节点数过多读不下来；只有时间没有节点价值 |
| `bridge` | Problem → Solution / 旧 → 新 | 左侧问题 + 中间桥/箭头 + 右侧解决 | 桥的隐喻不明显；左右两端没有对比张力 |
| `dense-modules` | 仪表盘 / 多维总结 | 杂志式版面，多个不等大模块组合 | 信息过载；缺少明确视觉入口 |

**选择决策树**：

```
论点类型？
├── 单中心 + 多分支         → hub-spoke
├── 对立/二分               → binary-comparison
├── 多个并列要素（无主次）   → bento-grid
├── 有先后顺序/时间          → linear-progression
├── 从旧到新/从坏到好        → bridge
└── 需要展示多维度仪表盘     → dense-modules
```

每种布局的详细使用方式见下方各小节。

---

### hub-spoke

**适用**：一个核心概念辐射出 4-6 个子维度的总览图。

**视觉结构**：
- 画面正中央一个大节点（hub），通常是五角星 / 大圆 / 高亮形状
- 4-6 根带轻微抖动的曲线向外辐射
- 每根辐条末端是一个圆角矩形或圆形子节点
- 子节点内含：编号 + 标题 + 2-3 条子要点
- 整体围绕中心呈对称放射结构

**推荐配色**：
- 中心 hub：**Coral Red**（强调焦点）
- 子节点：**Blue / Mint / Lavender / Peach** 轮换，每个色对应不同语义
- 装饰小元素（背景星星、doodle）：charcoal 细线

**适用场景**：
- 多维度概念体系（六大原则、四种力量、八种方法）
- 一个核心问题 + 多个对应解
- 角色 / 系统 / 框架的全景图

**示例**：[06-dense-modules-... NO, hub-spoke 示例]：`strategy-ends-tactics-means/imgs/prompts/05-hub-spoke-six-principles.md`

---

### binary-comparison

**适用**：两个对立概念的对比，分隔清晰、左右对称。

**视觉结构**：
- 顶部主标题带（含副标题）
- 中央垂直手绘虚线分隔线（可叠加小图标：太极 / 天平 / 桥）
- 左半区一整套元素（概念名 + 3-5 子要点 + 案例小卡）
- 右半区镜像结构
- 底部一句话总结（可选）

**推荐配色**：
- 两侧背景轻染不同 macaron 色（如左 Coral / 右 Mint）
- 顶部 banner 与中央分隔用 **Lavender**（暗示这是元层级判断）
- 案例小卡用 **Peach**
- 关键名词卡片用 **Blue**

**适用场景**：
- 误解 vs 真相
- 旧范式 vs 新范式
- A 思维 vs B 思维
- 战略 vs 战术

**示例**：`strategy-ends-tactics-means/imgs/prompts/01-binary-comparison-epistemology-split.md`

**坑**：两侧权重必须均衡——左侧 5 个 bullet，右侧也要接近 5 个，否则视觉失衡。

---

### bento-grid

**适用**：4-8 个并列、无明显主次的要素。

**视觉结构**：
- 2×3 / 2×4 / 3×2 等矩阵排布
- 每格大小相近（可适度变化以制造节奏，但别太碎）
- 每格内：顶部小标题 + 中部一句话症状/描述 + 底部 2-3 个关键词或极简图标

**推荐配色**：
- 左列 vs 右列分两个色阵营（如 Coral vs Blue），区分类别
- 标题底色与边框统一同色，正文留白
- 案例小条用 **Peach**

**适用场景**：
- 失效模式枚举（如本次第 3 章 8 种失效）
- 多领域案例并列
- 工具箱 / 模式库
- 多个对照案例

**示例**：`strategy-ends-tactics-means/imgs/prompts/03-bento-grid-failure-modes.md`

**坑**：每格内容字数不均会非常难看——写 prompt 时强制每格 2-3 个 bullet、每 bullet ≤ 10 字。

---

### linear-progression

**适用**：时间轴、步骤、演化序列。

**视觉结构**：
- 横向主轴贯穿整张图
- 4-6 个节点，等距排列
- 每节点：上方时间/年份标签 + 节点本身 + 下方双层条带（如"承诺"+"实际涌现"）
- 节点间细虚线箭头串联
- 底部一行横跨全图的总结带

**推荐配色**：
- 上层条带（稳定/承诺/北极星）：**Coral**
- 下层条带（涌现/路径/实验）：**Mint**
- 工程细节标签：**Blue**
- 人物头像 / 时间标签：**Peach**
- 底部总结带：**Lavender**

**适用场景**：
- 历史案例时间轴（本次第 4 章）
- 流程步骤（5 步法）
- 渐变 / 演化（从 X 到 Y 到 Z）

**示例**：`strategy-ends-tactics-means/imgs/prompts/04-linear-progression-historical-cases.md`

**坑**：节点超过 6 个会读不动，宁可挑最有代表性的 4 个；每节点必须有差异（不要做"五个相同模板换标题"）。

---

### bridge

**适用**：从问题到解决、从旧状态到新状态的转换叙事。

**视觉结构**：
- 左半：问题/旧/负面（情绪色：coral/red 警示）
- 中间：一座桥 / 大箭头 / 旋转门，标注关键转换机制
- 右半：解决/新/正面（mint/blue 积极）
- 桥本身可带文字标签（如"层级分离"、"分类机制"）

**推荐配色**：
- 左 Coral / 右 Mint（或左 Lavender 抽象旧 / 右 Blue 工程新）
- 桥本体用 **Lavender**（元层级机制）
- 案例侧卡用 **Peach**

**适用场景**：
- 误区 → 正解
- 概念分层 / 层级整合（本次第 2 章用了双层桥结构）
- 从 A 到 B 的转换方法

**示例**：`strategy-ends-tactics-means/imgs/prompts/02-bridge-hierarchy-separation.md`

**坑**：桥的隐喻必须显眼（画成真桥 / 隧道 / 大箭头），不能只是中间一条线；左右两端必须有充分对比（不只是配色不同）。

---

### dense-modules

**适用**：杂志/仪表盘式总结，多个不等大模块组合。

**视觉结构**：
- 顶部主视觉（占 30-50% 高度的核心信息卡 / 雷达图 / 大概念图）
- 中部 3-5 个并列模块（信息密度均匀）
- 嵌入式案例引用框（不同色突出）
- 底部一行操作流程带 / 关键提示

**推荐配色**：
- 顶部主视觉用 **Lavender**（整合 / 元判断）
- 中部模块按语义分色（警示 Coral，纪律 Blue）
- 案例引用框 **Peach**
- 底部流程带按步骤渐变（Lavender → Mint → Blue → Coral → Peach）

**适用场景**：
- 决策卡 / 诊断表（本次第 6 章）
- 总结 / 仪表盘
- 多角度组合呈现

**示例**：`strategy-ends-tactics-means/imgs/prompts/06-dense-modules-diagnostic-card.md`

**坑**：信息过载——必须先有清晰的视觉入口（主视觉），别把所有模块做成同等大小。

---

## Prompt 输出模板

每张图一个 `.md` 文件，命名格式：`NN-<layout>-<short-slug>.md`，例如 `03-bento-grid-failure-modes.md`。

完整模板（复制粘贴改空格）：

````markdown
Create a professional infographic following these specifications:

## Image Specifications
- **Layout**: <layout-name>
- **Style**: hand-drawn-edu
- **Aspect Ratio**: 16:9
- **Language**: Chinese (zh)

## Layout Guidelines (<layout-name>)
<3-5 句话，针对本次主题的具体布局说明。
描述：画面如何分区、每区放什么、节点位置/数量/形状、视觉入口在哪里>

## Style Guidelines (hand-drawn-edu)
Hand-drawn educational infographic, macaron pastels on warm cream paper:
- Background: Warm cream (#F5F0E8)
- <区域 1>: <颜色 + 语义说明>
- <区域 2>: <颜色 + 语义说明>
- <区域 3>: <颜色 + 语义说明>
- <…按本次实际分区列出>
- All lines: hand-drawn wobble, charcoal (#2D2D2D)
- Stick figures, doodle icons, star decorations

---

## 标题（顶部居中）
<插图中文主标题，10-18 字，可加副标题>

## 内容区域

<按布局分块描述：每个区域包含什么文字、什么图标、什么数据>

<示例（hub-spoke）：
**中央枢纽**（五角星）：
- 大字：「核心概念」
- 小字：「副标题」

**辐条一·正上方**：原则一名称
- 子要点 1
- 子要点 2
- 图标：xxx
…
>

Text labels (in Chinese):
- <标签 1>
- <标签 2>
- <…至少 8 个中文标签，覆盖所有图中应出现的文字>
````

---

## 写作工作流

从"我有一个论点"到"我有一个 prompt"的 5 步法：

1. **抽核心论点（1 句话）**——这张图想让读者带走什么？
   - ❌ "讲讲战略和战术" → 太泛
   - ✅ "两种思维不是节奏之争，是认识论之争" → 一句话能讲完

2. **选布局**——按上面的决策树。一图一论点，宁可拆成两图也别堆。

3. **填核心元素**——按布局的视觉结构，写出每个区放什么：
   - 主标题（10-18 字）
   - 各区子标题
   - 数据/引用/案例（要具体，避免空泛）
   - 关键中文标签清单（≥ 8 个）

4. **分配颜色**——按颜色规范的"语义分配原则"。一张图最多 4 macaron + Coral 强调。

5. **加密度装饰**——doodle 箭头、五角星、stick figures、小气泡。**让画面"不空"但不"乱"**。

每个 prompt 约 1.5-2.5KB，太短信息不够、太长模型会丢细节。

---

## 常见坑

| 坑 | 症状 | 修正 |
|---|---|---|
| **英文堆砌** | 关键标签大量是 English | 优先用中文短语，公认术语保留英文 |
| **文字过多** | 一张图 > 200 字，密集到看不清 | 每区 ≤ 30 字，长论述移到正文 |
| **颜色乱配** | 一张图 5+ 种 macaron + 强调色 | 锁定 3-4 色 + 1 强调，按语义分配 |
| **空泛标签** | "重要"、"核心"、"关键"等无信息词 | 用具体数据 / 人名 / 年份 / 引用 |
| **节点过多** | hub-spoke 8 spokes / linear 7 steps | hub-spoke ≤ 6，linear ≤ 5 |
| **左右失衡** | binary-comparison 一边 5 项一边 2 项 | 强制两侧元素数量、字数接近 |
| **桥隐喻弱** | bridge 中间只画一条线 | 画成真桥 / 隧道 / 大箭头 + 桥上标文字 |
| **网格碎片化** | bento 每格内容差异大、风格不统一 | 每格模板对称（标题 + 一句话 + 图标） |
| **缺视觉入口** | dense-modules 模块全等大 | 顶部留一个 30-50% 的主视觉 |
| **装饰过度** | 满屏 doodle 抢戏 | 装饰服务于布局，留白比噪音重要 |

---

## 生成 & 入仓命令

```bash
# 单张
bun ~/.claude/skills/baoyu-image-gen/scripts/main.ts \
  --promptfiles content/posts/<slug>/imgs/prompts/01-<layout>-<short>.md \
  --image /tmp/blog-imgs/<slug>/01.png \
  --ar 16:9 \
  --provider openrouter

# 6 张并行：每张 run_in_background

# 压缩
cd content/posts/<slug>/imgs
for f in *.png; do
  sips -s format jpeg -s formatOptions 82 "$f" --out "${f%.png}.jpg"
done
rm *.png

# 替换文章中的 <!-- IMG_N --> 占位符为 markdown image refs
```

目标：单张 < 1MB，6 张总计 < 6MB。

---

## 与 `/kevin-blog-post` skill 的关系

该 skill（位于 `~/.claude/skills/kevin-blog-post/`）已内置这套规范并自动执行完整流程（写文章 → 配图 → 压缩 → 提交）。本规范是它的"参考资料"——单独配图（不写文章）时直接用本规范即可。
