# 信息图 Prompt 案例索引

按布局类型分组的真实 prompt 与成图。复用时挑同 layout 最接近主题的一个，复制改写。

---

## 主参考：`strategy-ends-tactics-means` 全套 6 张

文章：[北极星与脚下的路](../../content/posts/strategy-ends-tactics-means/index.md)

| # | Layout | 主题 | Prompt | 成图 |
|---|---|---|---|---|
| 1 | `binary-comparison` | 两种思维的根本分野（认识论） | [01-binary-comparison-epistemology-split.md](../../content/posts/strategy-ends-tactics-means/imgs/prompts/01-binary-comparison-epistemology-split.md) | [01.jpg](../../content/posts/strategy-ends-tactics-means/imgs/01.jpg) |
| 2 | `bridge` | 层级分离：战略 / 战术双层桥 | [02-bridge-hierarchy-separation.md](../../content/posts/strategy-ends-tactics-means/imgs/prompts/02-bridge-hierarchy-separation.md) | [02.jpg](../../content/posts/strategy-ends-tactics-means/imgs/02.jpg) |
| 3 | `bento-grid` | 两种思维各 4 种失效模式 | [03-bento-grid-failure-modes.md](../../content/posts/strategy-ends-tactics-means/imgs/prompts/03-bento-grid-failure-modes.md) | [03.jpg](../../content/posts/strategy-ends-tactics-means/imgs/03.jpg) |
| 4 | `linear-progression` | 历史现场时间轴（长征/丰田/登月/SpaceX） | [04-linear-progression-historical-cases.md](../../content/posts/strategy-ends-tactics-means/imgs/prompts/04-linear-progression-historical-cases.md) | [04.jpg](../../content/posts/strategy-ends-tactics-means/imgs/04.jpg) |
| 5 | `hub-spoke` | 六条整合原则中心辐射 | [05-hub-spoke-six-principles.md](../../content/posts/strategy-ends-tactics-means/imgs/prompts/05-hub-spoke-six-principles.md) | [05.jpg](../../content/posts/strategy-ends-tactics-means/imgs/05.jpg) |
| 6 | `dense-modules` | 工作日诊断卡 + 三陷阱 | [06-dense-modules-diagnostic-card.md](../../content/posts/strategy-ends-tactics-means/imgs/prompts/06-dense-modules-diagnostic-card.md) | [06.jpg](../../content/posts/strategy-ends-tactics-means/imgs/06.jpg) |

**这套 6 张特点**：
- 覆盖全部 6 种 layout 一遍（适合作为模板库）
- 颜色语义分配严格遵循 SPEC.md
- 每张图都嵌入了 2-4 个具体案例（Kennedy / Mintzberg / Kodak / Bezos 等）

---

## 按布局速查

### `binary-comparison`

| 来源 | 主题 | Prompt |
|---|---|---|
| strategy-ends-tactics-means | 终先于始 vs 始孕育终（认识论） | [01](../../content/posts/strategy-ends-tactics-means/imgs/prompts/01-binary-comparison-epistemology-split.md) |
| quant-trading-first-principles | 量化交易：误解 vs 真相 | [01](../../content/posts/quant-trading-first-principles/imgs/prompts/01-binary-comparison-conclusion.md) |
| mental-models | 第一性原理 vs 类比 | [02](../../content/posts/mental-models/imgs/prompts/02-binary-comparison-first-principles.md) |

### `bridge`

| 来源 | 主题 | Prompt |
|---|---|---|
| strategy-ends-tactics-means | 战略层 → 战术层（双层桥） | [02](../../content/posts/strategy-ends-tactics-means/imgs/prompts/02-bridge-hierarchy-separation.md) |
| quant-trading-first-principles | 模型层 → 地基层 | [03](../../content/posts/quant-trading-first-principles/imgs/prompts/03-bridge-model-layer.md) |

### `bento-grid`

| 来源 | 主题 | Prompt |
|---|---|---|
| strategy-ends-tactics-means | 8 种失效模式（2×4 网格） | [03](../../content/posts/strategy-ends-tactics-means/imgs/prompts/03-bento-grid-failure-modes.md) |
| quant-trading-first-principles | 误区成因（2×3 网格） | [05](../../content/posts/quant-trading-first-principles/imgs/prompts/05-bento-grid-misconception-causes.md) |

### `linear-progression`

| 来源 | 主题 | Prompt |
|---|---|---|
| strategy-ends-tactics-means | 历史时间轴（4 段双轨叙事） | [04](../../content/posts/strategy-ends-tactics-means/imgs/prompts/04-linear-progression-historical-cases.md) |
| quant-trading-first-principles | 第一性原理拆解步骤 | [02](../../content/posts/quant-trading-first-principles/imgs/prompts/02-linear-progression-decomposition.md) |

### `hub-spoke`

| 来源 | 主题 | Prompt |
|---|---|---|
| strategy-ends-tactics-means | 六条整合原则 | [05](../../content/posts/strategy-ends-tactics-means/imgs/prompts/05-hub-spoke-six-principles.md) |
| quant-trading-first-principles | 三大地基 | [04](../../content/posts/quant-trading-first-principles/imgs/prompts/04-hub-spoke-three-foundations.md) |
| mental-models | 思维模型 + 三领域 | [01](../../content/posts/mental-models/imgs/prompts/01-hub-spoke-mental-models-overview.md) |

### `dense-modules`

| 来源 | 主题 | Prompt |
|---|---|---|
| strategy-ends-tactics-means | 工作日诊断卡 + 三陷阱 + 操作流程 | [06](../../content/posts/strategy-ends-tactics-means/imgs/prompts/06-dense-modules-diagnostic-card.md) |
| quant-trading-first-principles | 决策框架仪表盘 | [06](../../content/posts/quant-trading-first-principles/imgs/prompts/06-dense-modules-decision-framework.md) |

---

## 复用建议

**新文章想配图，按主题反向找模板**：

| 你的章节是… | 看哪个案例 |
|---|---|
| 两种概念对比 | `binary-comparison` 任选 |
| 一组并列失效 / 错误 / 案例 | `bento-grid` |
| 历史/演化/步骤 | `linear-progression` |
| 误区 → 正解 / 旧 → 新 | `bridge` |
| 一个中心 + 多个原则 | `hub-spoke` |
| 决策卡 / 诊断表 / 总结 | `dense-modules` |

**改写策略**：
1. 复制最接近的 prompt
2. 替换 layout 区描述里的具体词（"长征" → 你的案例名）
3. 替换 style 区颜色分配里的语义（"以终为始区" → 你的分类名）
4. 完全重写"标题"和"内容区域"
5. 重写 Text labels 列表（中文，≥ 8 个）

---

## 历史教训（避免重复踩坑）

收集已发布文章配图过程中的真实问题：

- **过早压缩**：图 02、03 单张接近 1MB；若想严格 < 1MB，sips `formatOptions` 调到 75-78
- **未来日期被 Hugo 跳过**：post 写完发现 Hugo 不渲染——检查 frontmatter `date` 是否晚于当前时间
- **gallery class 自动包装**：Stack 主题会把相邻图片包成 gallery；如果只想要单图不要 gallery 效果，图片间需要插入文字段落隔开
- **OpenRouter Gemini 偶尔漏字**：长 prompt（> 2.5KB）容易丢细节；prompt 控制在 1.5-2.5KB
