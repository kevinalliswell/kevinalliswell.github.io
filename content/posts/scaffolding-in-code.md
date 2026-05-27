---
title: "代码里的脚手架：写了就要拆，但不能不写"
date: 2026-05-27T22:00:00+08:00
draft: false
tags: ["脚手架", "软件工程", "代码质量", "原型", "重构", "开发方法"]
categories: ["技术"]
author: "Kevin"
description: "好的工程师懂得搭脚手架——用临时结构支撑你够到真正的目标。更好的工程师懂得拆脚手架——在它变成技术债之前。"
---

> 建筑工地上，没人会把脚手架留在楼里。但在代码世界里，大多数"临时方案"最终都变成了永久建筑。

---

## 先说结论

**脚手架代码是你为了到达目标而搭建的临时结构——它帮你验证想法、支撑开发、跨越不确定性，但它不是最终产物。** 好的工程师不怕写脚手架，因为不写就够不到高处；好的工程师也不怕拆脚手架，因为留着它，大楼迟早出问题。

如果只记住一件事：**脚手架的价值不在于它本身，而在于它让你能建造原本建不了的东西。用完就拆，拆完不心疼。**

---

## 背景：为什么要讨论这个

每个工程师都写过这样的代码：

- "先硬编码，后面再改"
- "这个 mock 数据先用着"
- "加个 console.log 调一下"
- "先 copy 一份能跑的，回头重构"

这些代码有个共同特点：**写的时候就知道它不是最终答案**。它们是临时的、过渡的、为了支撑当前阶段的工作而存在的。

问题不在于写了这些代码——问题在于写了之后发生了什么。

Martin Fowler 说过一句被广泛传播的话：

> "Any fool can write code that a computer can understand. Good programmers write code that **humans** can understand."

但他没说的是：**有些代码压根不需要被人理解，因为它不该存活到需要被理解的那天。** 这类代码就是脚手架。

---

## 什么是脚手架代码？

### 一句话定义

**脚手架代码（Scaffolding Code）：为支撑开发过程而编写的临时性代码，它帮助你到达目标，但不是目标本身。**

### 人话解释

建筑工地的脚手架你见过——钢管搭成的临时框架，工人踩着它砌墙、刷漆、装玻璃。楼建好了，脚手架就拆了。没有人会把脚手架留在大楼外面，说"这是我们的建筑成果"。

代码里的脚手架也是一样。它可以是一段 mock 数据、一个测试用的临时接口、一个快速验证想法的 prototype，甚至是一个 `TODO: 先这样，后面改` 注释。

### 类比理解

| 建筑脚手架 | 代码脚手架 |
|-----------|-----------|
| 钢管和扣件 | 硬编码的值、mock 数据、临时脚本 |
| 工人站在上面施工 | 开发者基于它继续开发 |
| 楼建好就拆 | 功能稳定后就删 |
| 留着会挡视线、增加风险 | 留着会增加复杂度、制造 bug |
| 没有脚手架就够不到高处 | 没有原型就无法验证想法 |

---

## 代码世界里的七种脚手架

### 1. 原型代码（Prototype）

最经典的脚手架。写一段快速、粗糙的代码，验证一个想法是否可行。

Frederick Brooks 在《人月神话》中给出了明确指令：

> "Plan to throw one away; you will, anyhow."

第一版代码几乎一定是错的——不是逻辑错，而是你还不够理解问题。原型的价值不是代码本身，而是**写它的过程让你理解了真正的需求**。

```python
# 脚手架：验证 API 是否返回预期格式
import requests
r = requests.get("https://api.example.com/data")
print(r.json().keys())
print(r.json()["items"][0])
```

这段代码没有错误处理、没有类型定义、没有日志。但它不需要——因为它的使命是"跑一次，看到结果，然后被删掉"。

### 2. 硬编码与魔法数字

```javascript
// 脚手架：先用固定值跑通流程
const TAX_RATE = 0.13;
const SHIPPING_FEE = 15;
const DISCOUNT = 0.8;

function calculateTotal(price) {
  return price * DISCOUNT * (1 + TAX_RATE) + SHIPPING_FEE;
}
```

上线前，这些值应该来自配置中心或数据库。但在开发初期，硬编码让你跳过"配置系统还没搭好"这个障碍，先把业务逻辑跑通。

**危险在于**：这些硬编码非常容易活过它的保质期。三个月后，没人记得 `0.13` 是临时值还是真实税率。

### 3. Mock 数据与假接口

后端还没开发完，前端需要界面数据。怎么办？Mock。

```json
// mock/users.json —— 脚手架数据
[
  { "id": 1, "name": "张三", "role": "admin" },
  { "id": 2, "name": "李四", "role": "user" }
]
```

Mock 数据是前后端并行开发的润滑剂。它让前端不用等后端，后端不用赶前端。

但 Mock 有一个隐蔽的陷阱：**Mock 数据的结构可能和真实 API 不一致**。前端基于 Mock 开发了两周，对接真实接口时发现字段名不同、嵌套层级不同、分页逻辑不同——返工。

**最佳实践**：先定义 API 契约（OpenAPI / JSON Schema），再基于契约生成 Mock。这样脚手架和真实建筑用的是同一张图纸。

### 4. 调试代码

```python
print(">>> 到这了")
print(f">>> user_id = {user_id}")
print(f">>> response = {response.status_code}")
```

每个程序员的老朋友。它的生命周期应该以分钟计——定位问题、修复问题、删除 print。

现实是什么？打开任何一个上线半年的项目，`Ctrl+F` 搜一下 `console.log` 或 `print(`，你会发现遗留的调试代码像化石一样嵌在地层里。

Rob Pike（Go 语言联合创作者）曾说：

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it."

调试代码是必要的脚手架。但它应该是最短命的那种——用完即删，绝不过夜。

### 5. 临时脚本

```bash
# 一次性数据迁移脚本
psql -c "UPDATE users SET status = 'active' WHERE created_at > '2026-01-01'"
```

为解决一个特定问题写的脚本，跑一次就不再需要。

这类脚手架的风险不是"留在代码里"，而是"丢了找不到"。下次遇到类似问题时，你会重新写一遍。

**建议**：放在 `scripts/` 目录，文件名带日期（如 `2026-05-27-migrate-user-status.sh`），附一行注释说明用途。跑完不用删，但也别混入正式代码。

### 6. 权宜之计（Workaround）

```python
# HACK: 第三方库 v2.3.1 的 bug，升级到 v2.4 后可删除
# See: https://github.com/xxx/issues/1234
def parse_date(s):
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)
```

因为某个外部约束（第三方库 bug、系统限制、历史遗留）而写的临时补丁。

这类脚手架**必须带注释**——不是解释代码做什么，而是解释**为什么这样做**和**什么时候可以删除**。否则六个月后，没有人敢动它，因为没人知道删了会不会炸。

### 7. 功能开关（Feature Flag）

```python
if settings.ENABLE_NEW_CHECKOUT:
    return new_checkout_flow(cart)
else:
    return legacy_checkout_flow(cart)
```

功能开关让你在不改变部署节奏的情况下控制功能的可见性。它是持续交付的关键基础设施。

但功能开关也是最容易堆积的脚手架。每加一个 flag，代码就多一个分支。加到第 20 个的时候，代码变成了一棵条件判断的圣诞树。

Martin Fowler 在专门讨论 Feature Toggles 的文章中警告：

> "Feature Toggles have a tendency to **multiply** and **rot**. They require a proactive approach to removing them."

---

## 核心问题：为什么脚手架拆不掉

搭脚手架不难，难的是拆。为什么？

### 原因一：恐惧

"这段代码我不确定还有没有用，先留着吧。"

这是最常见的原因。删除代码需要勇气，因为删错了会出 bug，而保留一段无用代码不会。

**反直觉的事实**：保留无用代码的风险比删除它更大。无用代码会被后来的开发者误读、误用、误维护。它占据认知空间，增加理解成本。

Kent Beck 说得直接：

> "I'm not a great programmer; I'm just a good programmer with **great habits**."

删除无用代码就是一个"great habit"。

### 原因二：沉没成本

"这段代码我花了两天才写好，删了多可惜。"

代码的价值不在于你花了多少时间写它，而在于它**现在**是否在创造价值。如果它的使命已经完成（验证了想法、跑通了流程、定位了 bug），那它就应该功成身退。

### 原因三：没有明确的"到期日"

建筑工地的脚手架有明确的拆除节点——楼封顶了就拆。但代码里的脚手架通常没有。

没人在写 `console.log` 的时候会说"这行代码的到期日是下周三"。于是它就一直留着，直到有人在生产日志里看到一行 `>>> 到这了` 然后崩溃。

### 原因四：缺乏所有权

"这不是我写的，我不敢删。"

代码的集体所有权听起来很美好，但副作用是没人对清理负责。脚手架代码尤其容易落入这个陷阱——当初写它的人早就忘了，后来看到的人不敢动。

---

## 脚手架的生命周期管理

### 第一阶段：搭建——快、准、有标记

搭脚手架时做三件事：

1. **快**：不要在脚手架上追求完美。它是临时的，够用就行
2. **准**：明确它是脚手架。用注释、命名或文件位置标记出来
3. **有标记**：记录拆除条件。"后端 API 上线后替换""升级到 v3.0 后删除""本周五前处理"

```python
# SCAFFOLD: 后端 /api/v2/orders 上线后替换为真实调用
def get_orders():
    return [
        {"id": 1, "total": 299.0, "status": "paid"},
        {"id": 2, "total": 150.0, "status": "pending"},
    ]
```

`SCAFFOLD` 这个标记让你可以全局搜索，一眼看到项目里有多少临时代码。

### 第二阶段：使用——依赖但不信任

用脚手架支撑开发时，始终记住它是临时的。不要基于 mock 数据写复杂的业务逻辑，不要基于硬编码的值做性能优化。

**原则：脚手架承重，但不要在脚手架上装修。**

### 第三阶段：拆除——定期清理，果断删除

| 策略 | 做法 |
|------|------|
| 定期搜索 | 每个迭代结束时搜索 `SCAFFOLD`、`HACK`、`TODO`、`FIXME` |
| Code Review 把关 | Review 时检查 PR 是否引入了新的脚手架，是否标注了到期条件 |
| 设置提醒 | 在项目管理工具中创建"清理脚手架"任务，附上到期日 |
| 自动化检测 | CI 中加一步：统计 `SCAFFOLD` 注释数量，超过阈值报警 |

Ward Cunningham（技术债概念的提出者）说：

> "Shipping first-time code is like going into debt. A little debt speeds development so long as it is **paid back promptly**."

脚手架就是一种主动借的债。借债不可怕，不还才可怕。

---

## 案例：一个脚手架的完整生命周期

以一个真实场景为例：你在开发一个电商系统的订单模块。

**Day 1 — 搭建脚手架**

```python
# SCAFFOLD: 支付网关对接完成前，模拟支付结果
def process_payment(order_id, amount):
    import random
    success = random.random() > 0.1  # 90% 成功率
    return {"success": success, "transaction_id": f"MOCK-{order_id}"}
```

这段代码让你在支付网关还没对接的情况下，开发和测试整个订单流程。

**Day 5 — 基于脚手架开发**

订单创建、状态流转、退款逻辑全部开发完成。Mock 支付接口支撑了整个开发过程。

**Day 8 — 支付网关 SDK 就绪**

```python
# 真实实现：替换 SCAFFOLD
from payment_sdk import PaymentGateway

gateway = PaymentGateway(api_key=settings.PAYMENT_API_KEY)

def process_payment(order_id, amount):
    result = gateway.charge(amount_cents=int(amount * 100), reference=str(order_id))
    return {"success": result.status == "succeeded", "transaction_id": result.id}
```

脚手架被替换。`SCAFFOLD` 注释消失。`git log` 留下记录。

**Day 8.5 — 验证拆除**

跑一遍完整的测试套件，确认替换没有引入回归。搜索 `MOCK-` 确认没有其他代码依赖旧的 mock transaction ID 格式。

**这就是脚手架的理想生命周期：搭建 → 使用 → 替换 → 验证 → 清理痕迹。**

---

## 脚手架思维：超越代码

脚手架思维不只适用于代码。它是一种通用的做事方法：

**先搭一个粗糙但能用的结构，踩着它到达更高的位置，然后替换为正式方案。**

| 领域 | 脚手架 | 正式建筑 |
|------|--------|---------|
| 写作 | 大纲和草稿 | 终稿 |
| 创业 | MVP（最小可行产品） | 成熟产品 |
| 学习 | 类比和简化模型 | 精确理解 |
| 管理 | 临时流程和试行方案 | 标准化制度 |
| 设计 | 线框图和低保真原型 | 最终设计稿 |

Eric Ries 在《精益创业》中把 MVP 定义为：

> "The minimum viable product is that version of a new product which allows a team to collect the **maximum amount of validated learning** with the **least effort**."

MVP 就是商业世界的脚手架——它的目标不是成为最终产品，而是帮你验证假设。验证完了，要么在它基础上重建，要么推倒重来。

---

## 风险与边界

### 1. 脚手架不是偷懒的借口

"先随便写，后面再重构"——如果这句话变成口头禅，说明你不是在搭脚手架，而是在积累技术债。

**区分标准**：脚手架有明确的替换条件和时间预期。如果你说不出"什么时候拆"和"拆了换什么"，那它不是脚手架，只是烂代码。

### 2. 不是所有代码都该先搭脚手架

数据模型、API 契约、安全逻辑——这些是地基，不是脚手架。地基要从一开始就认真设计。

**判断标准**：这段代码被错误实现后，修复成本有多高？如果答案是"非常高"（数据迁移、API 兼容性、安全漏洞），那一开始就要做对，不能用脚手架应付。

### 3. 团队中的脚手架需要共识

一个人写脚手架，自己知道在哪里、什么时候拆。五个人写脚手架，没有统一标记和管理机制，脚手架会像杂草一样蔓延。

**团队协作的最低标准**：统一的脚手架标记（如 `SCAFFOLD:`）、Code Review 时的检查、迭代结束时的清理环节。

### 4. AI 时代的脚手架问题

当 AI 帮你写代码时，脚手架问题会被放大。AI 不知道哪些是"临时的"、哪些是"正式的"——它会基于你的脚手架继续构建，像在沙子上盖楼。

**应对方法**：在 CLAUDE.md 或规则文件中明确标注哪些是脚手架代码、哪些文件是临时的。让 AI 也知道什么该拆。

---

## 三点总结

1. **敢搭** — 脚手架是到达高处的必要工具。不要因为"代码不完美"就拒绝前进。原型、mock、硬编码、调试日志——它们的使命是支撑你跨过不确定性
2. **敢拆** — 脚手架的价值在使命完成的那一刻达到顶峰，之后每多留一天都在贬值。Ward Cunningham 的忠告：技术债要尽快还
3. **有章法** — 搭的时候标记清楚（`SCAFFOLD:`），用的时候不在上面过度建设，拆的时候搜索、验证、清理痕迹。脚手架管理不是英雄行为，是日常纪律

最后：

> **好的代码库不是没有脚手架的痕迹，而是脚手架来过、支撑过、然后干净地离开了。就像好的建筑，你看不到脚手架，但它一定曾经在那里。**

---

## 参考资源

- Frederick Brooks, *The Mythical Man-Month* (1975)
- Kent Beck, *Extreme Programming Explained* (1999)
- Martin Fowler, [Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) (2016)
- Ward Cunningham, [Technical Debt Metaphor](http://wiki.c2.com/?WardExplainsDebtMetaphor) (1992)
- Eric Ries, *The Lean Startup* (2011)
- Rob Pike, "Notes on Programming in C" (1989)

---

> 本文是个人对软件工程中"临时性代码"的理解与实践总结，欢迎讨论。
