---
title: "从协议逆向到全栈 Dashboard —— 我与 AI 协作开发工业 MFC 控制库的全过程"
date: 2026-03-20T18:00:00+08:00
draft: false
tags: ["AI 协作", "Claude Code", "Python", "工业控制", "MFC", "FastAPI", "Dashboard"]
categories: ["技术实践"]
author: "Kevin"
description: "记录一次完整的人机协作开发实践：从一份设备通讯说明 PDF 出发，到最终交付一个可 pip install 的 Python 工业控制库 + Web 可视化面板的全过程。9 小时，4700+ 行 Python，114 个测试用例。"
---

> 记录一次完整的人机协作开发实践：从一份设备通讯说明 PDF 出发，到最终交付一个可 pip install 的 Python 工业控制库 + Web 可视化面板的全过程。

## 背景

实验室里有几台 Azbil（山武）MQV 系列质量流量控制器（MFC），用于精确控制气体流量。这类工业设备通常使用私有协议通讯，厂商不提供 Python SDK，每个新项目都要重新写一遍通讯代码。

我的目标很明确：**做一个标准化的第三方通讯库**，能在不同项目中复用，并带上混配控制和可视化操作能力。

整个开发过程我选择与 Claude 协作完成，以下是完整的复盘。

---

## 开发时间线

| 阶段 | 内容 | 耗时 |
|------|------|------|
| Phase 1 | 协议逆向 + 通讯库 | ~2h |
| Phase 2 | 混配控制系统 | ~3h |
| Phase 3 | 文档 + 集成指南 | ~1h |
| Phase 4 | Web Dashboard | ~3h |
| **合计** | **从零到发版** | **~9h** |

产出：**4700+ 行 Python**、**870+ 行 JavaScript**、**660+ 行 HTML/CSS**、**114 个测试用例**、**3 篇文档**、**CI/CD 自动发版**。

---

## Phase 1：协议逆向与通讯库

### 输入

一份 Azbil MQV 的通讯说明 PDF。

### 思路

设备走 RS-485 总线，但用的**不是 Modbus**，而是 Azbil 私有的 CPL 协议。协议结构：

```
STX | ADR(2B) | CMD(2B) | DATA(nB) | ETX | BCC
```

关键点：
- 地址 2 字节 ASCII（`"01"`~`"31"`）
- BCC 校验是 STX 到 ETX 之间所有字节异或
- 寄存器地址通过 `WRS`/`RRS` 命令读写
- 数据用 ASCII hex 编码传输

### 交给 AI 做的

1. **阅读 PDF，提炼出结构化协议文档**（`docs/azbil_mqv_cpl_protocol.md`）
2. **基于协议文档实现通讯库**

### 我做的决策

- 不依赖 pymodbus（协议不是 Modbus）
- 用 pyserial 直连串口
- 总线级加锁（`threading.Lock`），支持多设备共享一条 RS-485 总线
- 分层设计：`protocol.py`（帧编解码）→ `bus.py`（总线通讯）→ `client.py`（设备抽象）

### 架构产出

```
azbil_mfc/
├── protocol.py   # CPL 帧构建与解析
├── bus.py        # RS485Bus，线程安全的总线管理
├── client.py     # MFCDevice，面向用户的 API
├── registers.py  # 寄存器地址常量
└── constants.py  # 气体类型、满量程等常量
```

**关键设计**：`RS485Bus` 是单例级的总线对象，所有 `MFCDevice` 共享同一个 bus 实例，通过锁保证同一时刻只有一个设备在通讯。

```python
bus = RS485Bus("/dev/ttyUSB0", baudrate=38400)
mfc1 = MFCDevice(bus, address=1)
mfc2 = MFCDevice(bus, address=2)
# 两个设备可以安全地在不同线程中并发操作
```

### 反思

让 AI 做协议逆向（从 PDF 到结构化文档）效率极高。手动整理大概需要半天，AI 几分钟搞定，而且格式规范、没有遗漏。

---

## Phase 2：多通道混配控制系统

### 需求

实验中经常需要多台 MFC 同时工作，按比例配气。而且涉及可燃气体时，必须有安全联锁。

### 我提出的核心需求

1. 按配方（Recipe）一键配气
2. 支持条件触发（时间/温度/事件/实验阶段）
3. **可燃气体 + 助燃气体禁止混配**（硬拦截）
4. **LEL（爆炸下限）浓度监控**（25% 预警，50% 紧急停止）

### AI 的方案设计 + 我的纠偏

AI 初版方案中 gas type 直接用字符串分类。我要求改为枚举 + 分类体系：

```python
class GasCategory(Enum):
    INERT = "inert"           # N2, Ar, He
    OXIDIZER = "oxidizer"     # O2, Air
    COMBUSTIBLE = "combustible"  # H2, CH4, CO, C3H8
    USER_DEFINED = "user_defined"
```

安全校验逻辑我明确指定了规则：
- **COMBUSTIBLE + OXIDIZER → 硬拦截，抛出 `GasSafetyError`**
- **COMBUSTIBLE 浓度 > 25% LEL → 警告**
- **COMBUSTIBLE 浓度 > 50% LEL → 自动 Emergency Stop**

### SP 设定值计算

MFC 的 SP（设定值）是 0~50000 的整数，对应 0~满量程：

```python
sp_raw = int(flow / max_flow * 50000)
```

这个换算逻辑封装在 Recipe 层，用户只需要指定百分比或流量值。

### 状态机设计

```
IDLE ──apply()──→ RUNNING ──emergency_stop()──→ EMERGENCY_STOP
  ↑                  │                              │
  └───── reset() ────┘──── stop() ────→ IDLE ←──────┘
```

Emergency Stop 的实现要点：**逐通道写入 SP=0，任意一个通道写入失败不影响其他通道继续归零**。

### 条件触发系统

```python
# 时间触发
TimeTrigger(datetime(2026, 3, 20, 14, 0))

# 周期触发
IntervalTrigger(timedelta(minutes=30))

# 温度触发（需外部回调）
TemperatureTrigger(threshold=150.0, callback=read_thermocouple)

# 事件触发
EventTrigger("vacuum_ready")
event_trigger.fire()  # 外部系统触发
```

### 反思

这个阶段 AI 产出代码的速度非常快，但**安全相关的逻辑必须由人来审核和指定规则**。AI 不了解实验室安全规范，它能实现你描述的任何规则，但规则本身必须由领域专家（你）来定义。

---

## Phase 3：文档与项目集成

### 关键决策：用户视角优先

一开始 AI 写的使用指南是按模块结构组织的（安装 → 协议 → 总线 → 设备 → ...）。我提出：

> "如果在其他项目中使用这些设备，该如何接入？直接 pip install？"

于是我要求把**项目集成**作为第一章，涵盖：
1. `pip install` 安装方式
2. 多设备注册模式
3. 封装为项目 Service 的示例
4. 设备数量无限制说明

这个调整让文档从"库开发者视角"转向了"库使用者视角"。

### 反思

文档的章节顺序看似小事，实际上反映了**你把谁当作第一读者**。AI 默认按技术栈组织，但用户关心的是"我怎么用"。

---

## Phase 4：Web Dashboard

### 方案选型

AI 给了两个方案：
- **方案 A**：FastAPI + React/Vue（前后端分离，需要 Node.js）
- **方案 B**：FastAPI + 原生 HTML/JS/CSS（单体部署，零前端工具链）

我选了 **方案 B**。理由：
1. 这是工业控制工具，不是互联网产品，不需要前端工程化
2. 部署越简单越好：`pip install` 后一行命令启动
3. 减少依赖 = 减少出问题的可能

### 架构设计

```
python -m azbil_mfc.dashboard --demo --port 8080
     │
     ▼
  FastAPI
  ├── GET  / ──→ index.html (SPA)
  ├── WS   /ws/live ──→ 实时推送（1s 间隔）
  ├── REST /api/mixer/* ──→ 混配控制
  ├── REST /api/recipe/* ──→ 配方管理
  ├── REST /api/device/* ──→ 设备管理
  ├── REST /api/safety/* ──→ 安全状态
  └── REST /api/experiment/* ──→ 实验序列
```

### 最难的技术点：Sync/Async 桥接

核心通讯库是同步的（`threading.Lock` + `serial`），但 FastAPI 是异步的。解决方案：

```python
# 在 async 端点中调用同步方法
result = await asyncio.to_thread(mixer.apply_recipe, recipe)
```

WebSocket 推送循环也用 `asyncio.to_thread` 读取设备状态，避免阻塞事件循环。

### Demo 模式：无硬件开发

`SimulatedBus` 替换 `RS485Bus`，在内存中模拟寄存器读写：
- PV（过程值）通过指数平滑追踪 SP（设定值）
- 叠加高斯噪声模拟真实波动
- 随机生成报警事件

```python
# 指数平滑
pv = pv * (1 - alpha) + sp * alpha + random.gauss(0, noise)
```

这让前端开发完全不需要连接真实设备。

### 前端：6 个功能页签

| 页签 | 功能 |
|------|------|
| 概览 | 环形仪表盘 + 60s 趋势线 + 紧急停止按钮 |
| 配方管理 | 配方 CRUD + 通道动态增删 + 安全校验 |
| 混配控制 | 选择配方 → 一键下发 → 实时状态 |
| 实验序列 | 多阶段实验编排 + 进度条 |
| 设备管理 | 总线扫描 + 设备增删 |
| 安全 | 相容性矩阵 + LEL 表 + 报警历史 |

Chart.js 本地化部署（`vendor/chart.min.js`），不依赖 CDN，确保离线可用。

### 反思

工业软件的前端不需要花哨，但必须**信息密度高、操作路径短**。一个紧急停止按钮要随时可见，比动画效果重要一万倍。

---

## 发版与 CI/CD

### 自动 Release 工作流

```yaml
on:
  push:
    tags:
      - 'v*'
```

打 tag 即触发：跑测试 → 构建 wheel → 自动生成 release notes → 发布 GitHub Release。

```bash
git tag v0.2.0
git push origin v0.2.0
# → 自动出现在 GitHub Releases 页面
```

用户可以直接从 Release 页面下载 wheel 包，或者：

```bash
pip install git+https://github.com/your-org/azbil-mfc.git@v0.2.0
```

---

## 协作模式复盘

### 什么适合交给 AI

| 任务类型 | AI 效率 | 说明 |
|----------|---------|------|
| 协议逆向（PDF → 结构化文档） | ★★★★★ | 最适合 AI 的任务，准确且快 |
| 样板代码生成（CRUD、路由、前端模板） | ★★★★★ | 大量重复结构，AI 一次搞定 |
| 测试用例编写 | ★★★★☆ | 114 个测试，覆盖边界情况 |
| 文档撰写 | ★★★★☆ | 需要人调整视角和优先级 |
| CSS / 前端样式 | ★★★★☆ | 暗色工业风一次成型 |
| 架构设计 | ★★★☆☆ | AI 提供选项，人做决策 |

### 什么必须由人来做

1. **安全规则定义** —— AI 不知道哪些气体不能混、LEL 阈值该设多少
2. **方案选型** —— 前后端分离 vs 单体部署，AI 给方案，人选型
3. **用户视角** —— 文档该以什么顺序组织，API 该怎么设计才符合直觉
4. **实际测试** —— 连上真实设备跑一遍，这是 AI 无法替代的

### 协作节奏

整个过程的节奏是：

```
我提需求（通常 1-2 句话）
  → AI 输出方案 / 代码（大段）
    → 我审核 + 纠偏（通常指出 1-2 个问题）
      → AI 修正
        → 下一个模块
```

每个 Phase 平均经过 2-3 轮对话就能完成。关键是**需求要明确**，含糊的需求会导致 AI 猜测，猜错了反而浪费时间。

---

## 项目最终结构

```
azbil-mfc/
├── azbil_mfc/
│   ├── __init__.py          # 库入口，版本号
│   ├── protocol.py          # CPL 协议帧编解码
│   ├── bus.py               # RS-485 总线管理
│   ├── client.py            # MFCDevice 设备抽象
│   ├── registers.py         # 寄存器地址常量
│   ├── constants.py         # 气体类型、满量程
│   ├── exceptions.py        # 自定义异常
│   ├── safety.py            # 气体安全校验
│   ├── recipe.py            # 配方模型与存储
│   ├── mixer.py             # 混配控制器
│   ├── scheduler.py         # 条件触发与实验调度
│   └── dashboard/           # Web 可视化面板
│       ├── app.py           # FastAPI 工厂
│       ├── simulation.py    # 硬件模拟器
│       ├── state.py         # 全局状态
│       ├── routes/          # API 路由（6 个模块）
│       └── static/          # 前端资源
│           ├── index.html
│           ├── css/style.css
│           ├── js/          # 9 个 JS 模块
│           └── vendor/      # Chart.js
├── tests/                   # 114 个测试用例
├── docs/                    # 协议文档 + 使用指南
├── examples/                # 使用示例
├── .github/workflows/       # 自动发版
├── pyproject.toml
└── README.md
```

---

## 总结

这次协作的核心体会：

> **AI 是一个极其高效的实现者，但架构决策和领域知识仍然需要人来把控。**

具体来说：
- **让 AI 做体力活**：协议解析、样板代码、测试用例、文档初稿
- **自己做脑力活**：安全规则、方案选型、用户体验、实际验证
- **明确需求是关键**：说清楚要什么，比说清楚怎么做更重要

9 小时，从一份设备 PDF 到一个完整的 Python 库 + Web Dashboard + 自动发版，这是传统开发模式下至少需要 2-3 周的工作量。

效率提升的本质不是"AI 写代码快"，而是**人机之间的决策-执行循环被极度压缩了**。

---

*工具链：Claude Code CLI + Python 3.11 + FastAPI + Chart.js*
*协作时间：2026-03-18 ~ 2026-03-20*
