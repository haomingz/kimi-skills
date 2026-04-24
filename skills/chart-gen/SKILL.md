---
name: chart-gen
version: 2.5.1
description: "从JSON数据生成高质量PNG/SVG图表图片，支持折线图、柱状图、面积图、散点图、K线图、饼图/环形图、热力图、多系列图和堆叠图等多种类型。适用于快速可视化数据、生成报告图表、绘制趋势变化等场景。当用户请求“生成图表”、“画个趋势图”、“做个柱状图”、“可视化这些数据”，或提供具体数据并要求“做成图表图片”、“导出为PNG”时触发。"
provides:
  - capability: chart-generation
    methods: [lineChart, barChart, areaChart, pieChart, candlestickChart, heatmap]
---

<!-- Localized from: chart-image -->

# 图表图片生成器

使用 Vega-Lite 从数据生成 PNG 图表图片，非常适合无界面的服务器环境。

## 为什么选择这个 Skill？

**专为 Fly.io / VPS / Docker 部署而设计：**
- ✅ **无需原生编译** - 使用 Sharp 预编译二进制文件（不像 `canvas` 需要构建工具）
- ✅ **无需 Puppeteer/浏览器** - 纯 Node.js 实现，无需下载 Chrome，无需无头浏览器开销
- ✅ **轻量级** - 总依赖约 15MB，而基于 Puppeteer 的方案需要 400MB+
- ✅ **冷启动快** - 无需等待浏览器启动，图表生成耗时 <500ms
- ✅ **支持离线** - 无需任何外部 API 调用（不像 QuickChart.io）

## 安装（仅需一次）

```bash
cd /data/clawd/skills/chart-image/scripts && npm install
```

## 快速上手

```bash
node /data/clawd/skills/chart-image/scripts/chart.mjs \
  --type line \
  --data '[{"x":"10:00","y":25},{"x":"10:30","y":27},{"x":"11:00","y":31}]' \
  --title "Price Over Time" \
  --output chart.png
```

## 图表类型

### 折线图（默认）
```bash
node chart.mjs --type line --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output line.png
```

### 柱状图
```bash
node chart.mjs --type bar --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output bar.png
```

### 面积图
```bash
node chart.mjs --type area --data '[{"x":"A","y":10},{"x":"B","y":15}]' --output area.png
```

### 饼图 / 环形图
```bash
# 饼图
node chart.mjs --type pie --data '[{"category":"A","value":30},{"category":"B","value":70}]' \
  --category-field category --y-field value --output pie.png

# 环形图（中间有空洞）
node chart.mjs --type donut --data '[{"category":"A","value":30},{"category":"B","value":70}]' \
  --category-field category --y-field value --output donut.png
```

### K 线图（OHLC）
```bash
node chart.mjs --type candlestick \
  --data '[{"x":"Mon","open":100,"high":110,"low":95,"close":105}]' \
  --open-field open --high-field high --low-field low --close-field close \
  --title "Stock Price" --output candle.png
```

### 热力图
```bash
node chart.mjs --type heatmap \
  --data '[{"x":"Mon","y":"Week1","value":5},{"x":"Tue","y":"Week1","value":8}]' \
  --color-value-field value --color-scheme viridis \
  --title "Activity Heatmap" --output heatmap.png
```

### 多系列折线图
在同一张图表上对比多条趋势线：
```bash
node chart.mjs --type line --series-field "market" \
  --data '[{"x":"Jan","y":10,"market":"A"},{"x":"Jan","y":15,"market":"B"}]' \
  --title "Comparison" --output multi.png
```

### 堆叠柱状图
```bash
node chart.mjs --type bar --stacked --color-field "category" \
  --data '[{"x":"Mon","y":10,"category":"Work"},{"x":"Mon","y":5,"category":"Personal"}]' \
  --title "Hours by Category" --output stacked.png
```

### 成交量叠加（双 Y 轴）
价格折线与成交量柱状图叠加显示：
```bash
node chart.mjs --type line --volume-field volume \
  --data '[{"x":"10:00","y":100,"volume":5000},{"x":"11:00","y":105,"volume":3000}]' \
  --title "Price + Volume" --output volume.png
```

### 迷你图（内联小图表）
```bash
node chart.mjs --sparkline --data '[{"x":"1","y":10},{"x":"2","y":15}]' --output spark.png
```
迷你图默认尺寸为 80x20，透明背景，无坐标轴。

## 选项参考

### 基础选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--type` | 图表类型：line, bar, area, point, pie, donut, candlestick, heatmap | line |
| `--data` | JSON 数据数组 | - |
| `--output` | 输出文件路径 | chart.png |
| `--title` | 图表标题 | - |
| `--width` | 宽度（像素） | 600 |
| `--height` | 高度（像素） | 300 |

### 坐标轴选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--x-field` | X 轴字段名 | x |
| `--y-field` | Y 轴字段名 | y |
| `--x-title` | X 轴标签 | 字段名 |
| `--y-title` | Y 轴标签 | 字段名 |
| `--x-type` | X 轴类型：ordinal（分类）, temporal（时间）, quantitative（数值） | ordinal |
| `--y-domain` | Y 轴范围，格式为 "最小值,最大值" | 自动 |

### 视觉选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--color` | 线条/柱状图颜色 | #e63946 |
| `--dark` | 暗色主题 | false |
| `--svg` | 输出 SVG 格式（而非 PNG） | false |
| `--color-scheme` | Vega 配色方案（category10, viridis 等） | - |

### 警报/监控选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--show-change` | 在最后一个数据点显示涨跌百分比标注 | false |
| `--focus-change` | 将 Y 轴缩放至数据范围的 2 倍，突出变化 | false |
| `--focus-recent N` | 只显示最近 N 个数据点 | 全部 |
| `--show-values` | 标注最大值/最小值 | false |

### 多系列/堆叠选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--series-field` | 多系列折线图的分组字段 | - |
| `--stacked` | 启用堆叠柱状图模式 | false |
| `--color-field` | 堆叠/颜色分类字段 | - |

### K 线图选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--open-field` | OHLC 开盘价字段 | open |
| `--high-field` | OHLC 最高价字段 | high |
| `--low-field` | OHLC 最低价字段 | low |
| `--close-field` | OHLC 收盘价字段 | close |

### 饼图/环形图选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--category-field` | 饼图扇区分类字段 | x |
| `--donut` | 渲染为环形图（中间有空洞） | false |

### 热力图选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--color-value-field` | 热力图色彩强度字段 | value |
| `--y-category-field` | Y 轴分类字段 | y |

### 双 Y 轴选项（通用）
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--y2-field` | 第二 Y 轴字段（独立的右侧坐标轴） | - |
| `--y2-title` | 第二 Y 轴标题 | 字段名 |
| `--y2-color` | 第二系列颜色 | #60a5fa（暗色）/ #2563eb（亮色） |
| `--y2-type` | 第二坐标轴图表类型：line, bar, area | line |

**示例：** 收入柱状图（左轴）+ 流失率面积图（右轴）：
```bash
node chart.mjs \
  --data '[{"month":"Jan","revenue":12000,"churn":4.2},...]' \
  --x-field month --y-field revenue --type bar \
  --y2-field churn --y2-type area --y2-color "#60a5fa" \
  --y-title "Revenue ($)" --y2-title "Churn (%)" \
  --x-sort none --dark --title "Revenue vs Churn"
```

### 成交量叠加选项（K 线图）
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--volume-field` | 成交量柱状图字段（启用双 Y 轴） | - |
| `--volume-color` | 成交量柱状图颜色 | #4a5568 |

### 格式化选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--y-format` | Y 轴格式：percent, dollar, compact, decimal4, integer, scientific，或 d3-format 字符串 | 自动 |
| `--subtitle` | 图表副标题（显示在标题下方） | - |
| `--hline` | 水平参考线：格式为 "值" 或 "值,颜色" 或 "值,颜色,标签"（可重复使用） | - |

### 标注选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--annotation` | 静态文字标注 | - |
| `--annotations` | JSON 格式的事件标记数组 | - |

## 警报风格图表（推荐用于监控场景）

```bash
node chart.mjs --type line --data '[...]' \
  --title "Iran Strike Odds (48h)" \
  --show-change --focus-change --show-values --dark \
  --output alert.png
```

只查看最近的变化：
```bash
node chart.mjs --type line --data '[hourly data...]' \
  --focus-recent 4 --show-change --focus-change --dark \
  --output recent.png
```

## 时间线标注

在图表上标记事件：
```bash
node chart.mjs --type line --data '[...]' \
  --annotations '[{"x":"14:00","label":"News broke"},{"x":"16:30","label":"Press conf"}]' \
  --output annotated.png
```

## 时间类型 X 轴

用于需要正确处理日期间隔的时间序列：
```bash
node chart.mjs --type line --x-type temporal \
  --data '[{"x":"2026-01-01","y":10},{"x":"2026-01-15","y":20}]' \
  --output temporal.png
```

当 X 值为 ISO 日期格式且你希望间距反映实际时间间隔（而非等间距排列）时，使用 `--x-type temporal`。

## Y 轴格式化

格式化坐标轴数值以提高可读性：
```bash
# 美元金额
node chart.mjs --data '[...]' --y-format dollar --output revenue.png
# → $1,234.56

# 百分比（值为 0-1 的小数）
node chart.mjs --data '[...]' --y-format percent --output rates.png
# → 45.2%

# 大数字简写
node chart.mjs --data '[...]' --y-format compact --output users.png
# → 1.2K, 3.4M

# 加密货币价格（4 位小数）
node chart.mjs --data '[...]' --y-format decimal4 --output molt.png
# → 0.0004

# 自定义 d3-format 字符串
node chart.mjs --data '[...]' --y-format ',.3f' --output custom.png
```

可用的快捷格式：`percent`, `dollar`/`usd`, `compact`, `integer`, `decimal2`, `decimal4`, `scientific`

## 图表副标题

在标题下方添加补充说明：
```bash
node chart.mjs --title "MOLT Price" --subtitle "20,668 MOLT held" --data '[...]' --output molt.png
```

## 主题选择

使用 `--dark` 开启暗色模式。建议根据时间自动选择：
- **夜间（20:00-07:00 本地时间）**：`--dark`
- **白天（07:00-20:00 本地时间）**：亮色模式（默认）

## 通过管道传入数据

```bash
echo '[{"x":"A","y":1},{"x":"B","y":2}]' | node chart.mjs --output out.png
```

## 自定义 Vega-Lite 规范

用于高级图表定制：
```bash
node chart.mjs --spec my-spec.json --output custom.png
```

## ⚠️ 重要：务必发送图片！

生成图表后，**务必将图片发送回用户的频道**。
不要只是保存到文件然后描述它——图表的意义在于可视化呈现。

```bash
# 1. 生成图表
node chart.mjs --type line --data '...' --output /data/clawd/tmp/my-chart.png

# 2. 发送图片！使用 message 工具的 filePath 参数：
#    action=send, target=<channel_id>, filePath=/data/clawd/tmp/my-chart.png
```

**小贴士：**
- 保存到 `/data/clawd/tmp/`（持久化存储）而非 `/tmp/`（可能被清理）
- 使用 `action=send` 配合 `filePath`——`thread-reply` 不支持文件附件
- 在消息文本中附上简短说明
- 在 20:00-07:00 之间自动使用 `--dark`

---
*更新于：2026-02-04 - 新增 --y-format（percent/dollar/compact/decimal4）和 --subtitle 选项*
