# 分析框架 — 市场洞察报告

市场分析和数据驱动洞察生成指南。本框架定义的是**如何分析**，而不仅仅是如何排版。报告中每一个分析章节都应追溯到此处描述的一个或多个方法。

## 目录

1. [市场规模测算方法论](#1-市场规模测算方法论)
2. [品类与增长驱动因素分析](#2-品类与增长驱动因素分析)
3. [渠道分析](#3-渠道分析)
4. [消费者行为分析](#4-消费者行为分析)
5. [竞争分析](#5-竞争分析)
6. [数据到洞察的方法论](#6-数据到洞察的方法论)

---

## 1. 市场规模测算方法论

### 自上而下法
从宏观数据出发逐步缩小范围：

```
Total Population / Households
  × Target Demographic %
  × Category Penetration Rate
  × Average Purchase Frequency (per year)
  × Average Spend per Purchase
  = Total Addressable Market (TAM)
```

**适用场景**：初始市场规模测算、新市场进入分析、跨国对比。

**数据来源**：国家统计局、Euromonitor、Statista、行业协会。

### 自下而上法
从单元级数据出发逐步汇总：

```
Number of Active SKUs/Brands
  × Average Revenue per SKU
  = Brand-level Revenue

Sum of all brand revenues = Market Size

OR:

Number of Retail Outlets (online + offline)
  × Average Category Revenue per Outlet
  = Market Size
```

**适用场景**：验证自上而下的估算、细分市场规模测算、拥有较好企业级数据的市场。

**数据来源**：企业财报、渠道数据（电商平台 GMV）、零售审计数据（尼尔森/凯度）。

### 交叉验证规则
**必须同时使用两种方法并进行对比。** 若差异超过20%，需调查差距原因：
- 自上而下 > 自下而上：自下而上法中可能遗漏了品牌/渠道
- 自下而上 > 自上而下：自上而下法中可能高估了渗透率/购买频次
- 同时展示两种估算结果及验证后的区间

### TAM / SAM / SOM 框架

| 层级 | 定义 | 计算方式 |
|-------|-----------|------------------|
| **TAM**（总可触达市场） | 假设所有潜在客户都购买的总市场需求 | 人口 × 渗透率上限 × 平均消费金额 |
| **SAM**（可服务可触达市场） | 你的产品/服务能够触及的那部分市场 | TAM × 地理/渠道/细分市场筛选条件 |
| **SOM**（可服务可获得市场） | 3-5年内可实际获取的市场份额 | SAM × 预期市场份额（通常5-20%） |

### 数据来源优先级
1. 政府统计/人口普查数据（最权威）
2. 行业协会报告
3. 零售审计数据（尼尔森、凯度、GfK）
4. 上市公司财报和业绩说明会
5. 电商平台数据（官方报告或第三方追踪器）
6. 第三方研究报告（咨询公司、券商研究）
7. 专家访谈和实地调研

---

## 2. 品类与增长驱动因素分析

### 增长分解公式

任何消费市场的基本方程式：

```
Revenue = Penetration × Purchase Frequency × Spend per Occasion

Growth (%) = Penetration Growth + Frequency Growth + Price/Mix Growth
```

对每个品类，将增长分解为这三大驱动因素，并识别哪个是核心增长引擎。

### 量价分解

```
Revenue Growth = Volume Growth + ASP Growth

Where:
  Volume Growth = Unit Shipment Growth (quantity effect)
  ASP Growth = Average Selling Price change (price/mix effect)
```

**解读矩阵**：

| 量 | 价 | 判断 |
|--------|-------|-----------|
| + | + | 健康增长（扩大渗透率 + 高端化升级） |
| + | - | 量驱动增长，可能存在价格战 |
| - | + | 高端化升级 / 市场成熟化 |
| - | - | 市场萎缩，结构性衰退 |

### 品类生命周期定位

将每个品类定位在生命周期曲线上：

| 阶段 | 增长率 | 渗透率 | 竞争强度 | 策略启示 |
|-------|------------|-------------|----------------------|---------------------|
| **导入期** | >30% | <10% | 低（参与者少） | 教育市场，建立认知 |
| **成长期** | 15-30% | 10-40% | 上升 | 抢占份额，规模化分销 |
| **成熟期** | 0-15% | 40-70% | 高 | 防守份额，优化利润 |
| **衰退期** | <0% | 下降 | 整合中 | 收割或转型 |

### 品类矩阵（四象限分析）

将品类绘制在2×2矩阵上：
- **X轴**：营收增长率（%）
- **Y轴**：市场份额变化（百分点）

| 象限 | 增长 | 份额 | 解读 |
|----------|--------|-------|---------------|
| 明星（右上） | 高 | 上升 | 品类领导者，积极投入 |
| 现金牛（右下） | 高 | 下降 | 增长市场但正在失守 |
| 问号（左上） | 低 | 上升 | 在低增长市场中抢占份额 |
| 瘦狗（左下） | 低 | 下降 | 表现不佳，需重组或退出 |

### 价格带分析

按价格层级细分市场并追踪迁移趋势：

```
Price Band Structure:
  Premium (top 20% price):    XX% of revenue, XX% of volume
  Mid-range (middle 50%):     XX% of revenue, XX% of volume
  Value (bottom 30% price):   XX% of revenue, XX% of volume

Price Band Migration (YoY change in share):
  Premium: +X pp (premiumization trend)
  Mid-range: -X pp (hollowing out)
  Value: +/-X pp
```

---

## 3. 渠道分析

### 渠道份额追踪

追踪至少3-5年的渠道份额演变：

```
Channel Share Table:
              Year 1   Year 2   Year 3   CAGR
Online total:  XX%      XX%      XX%      XX%
  - Platform A XX%      XX%      XX%      XX%
  - Platform B XX%      XX%      XX%      XX%
  - Platform C XX%      XX%      XX%      XX%
Offline total: XX%      XX%      XX%      XX%
  - Modern trade XX%    XX%      XX%      XX%
  - Traditional  XX%    XX%      XX%      XX%
```

用堆叠百分比柱形图 + CAGR 侧表进行可视化。

### 渠道迁移矩阵

对每一次重大渠道变迁，追踪流向：

```
Where did [Channel A]'s lost share go?
  → X pp to Channel B (driven by: [reason])
  → Y pp to Channel C (driven by: [reason])
  → Z pp to Channel D (driven by: [reason])

Where did [Channel E]'s new share come from?
  → X pp from Channel A (driven by: [reason])
  → Y pp from Channel B (driven by: [reason])
```

### 渠道效率对比

用标准化指标比较各渠道：

| 指标 | 渠道A | 渠道B | 渠道C |
|--------|-----------|-----------|-----------|
| GMV / 流量（转化价值） | | | |
| 转化率 | | | |
| 平均客单价 | | | |
| 复购率 | | | |
| 获客成本 | | | |
| 退货率 | | | |

### 新兴渠道评估框架

对任何新兴/快速增长的渠道，从以下维度评估：

1. **规模**：当前 GMV/用户量，增长率
2. **渗透率轨迹**：目标用户中有多少比例已尝试该渠道？
3. **用户重叠度**：与现有渠道的重叠程度如何？（高重叠 = 替代效应，低重叠 = 增量贡献）
4. **单位经济模型**：该渠道在规模化后能否盈利？
5. **可持续性**：增长是由补贴/促销驱动还是有机需求？

---

## 4. 消费者行为分析

### 购买决策旅程

描绘该品类的消费者旅程：

```
Awareness → Interest → Consideration → Purchase → Loyalty/Advocacy
   ↑            ↑           ↑              ↑            ↑
[Touchpoints] [Content]  [Comparison]  [Channel]   [Retention]
```

对每个阶段，识别：
- 什么触发了消费者向下一阶段的转移？
- 关键触点有哪些？
- 最大的流失环节在哪里？

### 消费者分群框架

叠加多个维度进行分群：

**维度1：人口统计学**
- 年龄世代（Z世代 / 千禧一代 / X世代 / 银发族）
- 城市层级（一线 / 新一线 / 二线 / 三线及以下）
- 收入水平

**维度2：行为特征**
- 购买频次（重度 / 中度 / 轻度 / 流失用户）
- 渠道偏好（线上优先 / 线下优先 / 全渠道）
- 价格敏感度（追求高端 / 追求性价比 / 追求折扣）

**维度3：心理特征**
- 生活方式价值观（健康导向 / 便利导向 / 地位追求 / 环保意识）
- 信息获取来源（社交媒体驱动 / 专家驱动 / 同伴驱动）

**交叉分析规则**：最具可执行性的分群来自人口统计 × 行为特征的交叉，而非仅凭人口统计学。

### 需求场景/消费时机分析

描绘消费场景以理解需求驱动因素：

```
Occasion Matrix:
                    High Frequency    Low Frequency
High Spend/Order    [Habitual Premium] [Special Occasion]
Low Spend/Order     [Daily Routine]    [Impulse/Trial]
```

对每个象限：识别品类适配性、增长潜力和未被满足的需求。

### 调研数据解读规则

引用消费者调研数据时：
- **始终标注样本量和方法论**（在线面板、街头拦截等）
- **区分声称行为与实际行为**——调研会高估意愿，低估习惯性行为
- **尽可能与交易数据交叉验证**
- **注意近因偏差**——消费者会过度放大近期体验的权重
- **小样本时报告置信区间**

### 从行为数据到人群画像

基于数据构建人群画像，而非凭空想象：

```
Step 1: Identify behavioral clusters in the data (purchase patterns, channel usage, price points)
Step 2: Profile each cluster demographically (age, city, income)
Step 3: Validate with qualitative data (interviews, social listening)
Step 4: Name the persona and define its defining behavior (not just demographics)
Step 5: Size each persona (% of total market, % of total revenue)
```

**规则**：好的人群画像由他们**做什么**定义，而非他们**是谁**。

---

## 5. 竞争分析

### 市场份额归因

当市场份额发生变动时，分解驱动因素：

```
Brand X Share Change = Brand Effect + Channel Effect + Price Effect + Innovation Effect

Where:
  Brand Effect:     Share change due to brand preference/loyalty shifts
  Channel Effect:   Share change due to distribution gains/losses
  Price Effect:     Share change due to relative pricing moves
  Innovation Effect: Share change due to new product launches
```

对市场中每一次重大份额变动，归因其主要驱动因素。

### 集中度指标

| 指标 | 公式 | 解读 |
|--------|---------|---------------|
| **CR3** | 前3名市场份额之和 | >60% = 寡头垄断；<40% = 分散竞争 |
| **CR5** | 前5名市场份额之和 | >80% = 高度集中 |
| **HHI** | 各品牌市场份额平方之和（×10,000） | <1,500 = 竞争性市场；1,500-2,500 = 适度集中；>2,500 = 高度集中 |

追踪 CR3/CR5 的变化趋势——上升 = 行业整合，下降 = 格局分散。

### 品牌竞争力雷达图

对每个主要品牌从5-6个维度评估：

1. **品牌认知度/心智份额**（辅助/非辅助回忆率、搜索指数）
2. **产品实力**（质量感知、创新管线、组合广度）
3. **渠道覆盖**（分销宽度 × 深度、线上/线下平衡）
4. **价格竞争力**（价格定位、促销力度、价值感知）
5. **营销效率**（声量份额、社交热度、投入产出比）
6. **增长动能**（营收增长、份额趋势、新用户获取）

用雷达/蛛网图对3-5个核心竞品进行可视化。

### 竞争格局叙事框架

将竞争叙事构建为演进故事：

```
Phase 1: [Past state] — "[Describe the old competitive landscape]"
  Key characteristics: [who dominated, why]

Phase 2: [Disruption] — "[What changed]"
  Trigger: [technology shift / new entrant / regulation / demand change]

Phase 3: [Current state] — "[Today's competitive landscape]"
  Key characteristics: [new leaders, new dynamics]

Outlook: [Where the landscape is heading]
  Driving forces: [what will shape the next phase]
```

### 品牌份额桥接图

将总市场份额变化分解为瀑布/桥接图：

```
Starting Share (Year N-1)
  + Gains from new product launches
  + Gains from distribution expansion
  + Gains from pricing strategy
  - Losses to competitor innovation
  - Losses from channel shifts
  - Losses from brand perception decline
  = Ending Share (Year N)
```

用瀑布图可视化（绿色表示增长，红色表示下降）。

---

## 6. 数据到洞察的方法论

### 洞察发现流程（5步法）

```
Step 1: OBSERVE — Spot an anomaly or pattern in the data
  "This number is surprisingly high/low/different from expectations"

Step 2: HYPOTHESIZE — Form a testable explanation
  "This might be because..."

Step 3: VALIDATE — Test the hypothesis with additional data
  "The data [confirms/refutes] this because..."

Step 4: ATTRIBUTE — Identify the root cause
  "The primary driver is X, secondary driver is Y"

Step 5: SYNTHESIZE — Distill into an actionable insight
  "[Stakeholder] should [action] because [finding] which means [implication]"
```

**报告中每一个分析段落都应追溯到这个5步流程。** 段落可能不会明确列出全部5步，但分析师在思维层面必须经历了完整流程。

### "So What?"检验

报告中每一个数据点都必须通过此检验：

```
Data point: "Category X grew 15% YoY"
So what?  → "This outpaced the overall market growth of 8%"
So what?  → "Category X is gaining wallet share from adjacent categories"
So what?  → "Brands in Category X should invest in capacity/distribution now
             while the growth window is open"
```

**规则**：持续追问"So what?"直到得出可执行的启示。如果无法导出行动，该数据点不应出现在报告中。

### 对比驱动的洞察

洞察来源于对比，而非孤立的数据点。每个数据至少要与一个基准进行对比：

| 对比类型 | 示例 | 洞察触发点 |
|----------------|---------|-----------------|
| **同比**（YoY） | "增速从25%放缓至12%" | 趋势转变 |
| **环比**（QoQ） | "Q4是Q3的3倍" | 季节性或事件驱动的激增 |
| **跨品类** | "护肤增长20%而彩妆下降5%" | 品类替代 |
| **跨渠道** | "线上增长30%而线下下降8%" | 渠道迁移 |
| **跨区域** | "一线城市下降而三线城市增长" | 需求转移 |
| **vs 共识** | "实际值是分析师预期的2倍" | 市场定价偏差 |
| **vs 基准** | "A公司利润率高于行业均值10个百分点" | 竞争优势 |

### 洞察质量标准

一个好的洞察必须同时满足以下四个标准：

1. **具体**：包含具体数字、百分比或具名实体——不是模糊的概括
2. **量化**：发现的幅度被清晰地标注
3. **可执行**：能为特定利益相关者导出具体建议
4. **因果**：解释了**为什么**，而非仅仅陈述**是什么**——包含因果链条

**反面案例**："市场在增长"（模糊、无量级、无行动、无因果）

**正面案例**："X品类同比增长22%，主要由三四线城市渗透率提升（+8个百分点）驱动，这意味着品牌应加速在低线城市的分销布局，因为那里的增长天花板依然很高（当前渗透率15% vs 一线城市45%）"

### 洞察到建议的模板

```
INSIGHT: [What we found — specific, quantified]
DRIVER: [Why this is happening — root cause]
IMPLICATION: [What this means — for whom, by when]
RECOMMENDATION: [What to do — specific action, expected impact]
```

报告中每一个建议章节都应遵循此结构。没有明确洞察支撑的建议是观点，而非分析。

---

## 适配指南

本框架为消费/零售市场设计，但可适配至其他领域：

- **B2B市场**：将"渗透率 × 购买频次 × 客单价"替换为"客户数 × 合同金额 × 续约率"
- **科技市场**：增加"采用曲线"分析（创新者 → 早期采用者 → 早期主流）
- **服务市场**：在增长分解中增加"利用率"和"客户终身价值"
- **平台/市场平台型市场**：分别增加"供给侧"和"需求侧"指标

在适配时，始终保留：
1. 增长分解逻辑（什么 × 多少 × 多频繁）
2. 竞争归因框架（份额为什么变动了）
3. 5步洞察发现流程
4. 每个数据点的"So what?"检验
