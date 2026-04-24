# 📊 chart-image

**从数据生成出版级质量的图表图片。无需浏览器，无需 Puppeteer，无需原生编译。**

直接从 JSON 数据生成精美的 PNG 图表——非常适合机器人、仪表板、告警和自动化报告。只要能运行 Node.js 的地方就能使用。

![折线图示例](readme-assets/framed-line.png)

## 为什么选择 chart-image？

大多数图表库需要浏览器（Puppeteer、Playwright）或原生依赖（`canvas`、`cairo`），这意味着 400MB 以上的安装体积、痛苦的 Docker 构建过程和缓慢的冷启动。

**chart-image 使用 Vega-Lite + Sharp 预编译二进制文件：**

| | chart-image | Puppeteer + Chart.js | QuickChart.io |
|---|---|---|---|
| **安装体积** | ~15MB | ~400MB+ | 0（API 调用） |
| **原生依赖** | 无 | Chromium | 不适用 |
| **冷启动** | <500ms | 2-5s | 网络延迟 |
| **离线使用** | ✅ | ✅ | ❌ |
| **Fly.io/Docker** | 开箱即用 | 配置繁琐 | 依赖服务可用性 |

## 安装

### 通过 ClawHub 安装（推荐）
```bash
clawhub install chart-image
```

### 手动安装
```bash
git clone https://github.com/Cluka-399/chart-image.git skills/chart-image
cd skills/chart-image/scripts && npm install
```

## 快速上手

```bash
node scripts/chart.mjs \
  --type line \
  --data '[{"x":"Mon","y":10},{"x":"Tue","y":25},{"x":"Wed","y":18}]' \
  --title "Weekly Trend" \
  --dark \
  --output chart.png
```

就这么简单。一条命令，一张 PNG。

---

## 图表类型

### 📈 折线图

追踪随时间变化的趋势。这是默认图表类型。

```bash
node scripts/chart.mjs --type line \
  --data '[{"x":"Mon","y":142},{"x":"Tue","y":148},{"x":"Wed","y":145},{"x":"Thu","y":155},{"x":"Fri","y":162}]' \
  --title "AAPL Weekly Price" --y-title "Price (USD)" \
  --dark --show-values --output chart.png
```

![折线图](readme-assets/framed-line.png)

### 📊 柱状图

并列比较各类别。

```bash
node scripts/chart.mjs --type bar \
  --data '[{"x":"React","y":45},{"x":"Vue","y":28},{"x":"Svelte","y":15},{"x":"Angular","y":12}]' \
  --title "Framework Usage %" --output chart.png
```

![柱状图](readme-assets/framed-bar.png)

### 🌊 面积图

与折线图类似，但用填充区域强调数据量。

```bash
node scripts/chart.mjs --type area \
  --data '[{"x":"Jan","y":100},{"x":"Feb","y":250},{"x":"Mar","y":180},{"x":"Apr","y":420},{"x":"May","y":380},{"x":"Jun","y":520}]' \
  --title "Monthly Signups" --dark --output chart.png
```

![面积图](readme-assets/framed-area.png)

### 🍩 环形图 / 饼图

一眼看清比例分布。使用 `--type pie` 生成实心圆饼图，使用 `--type donut` 生成环形图。

```bash
node scripts/chart.mjs --type donut \
  --data '[{"x":"Desktop","y":58},{"x":"Mobile","y":35},{"x":"Tablet","y":7}]' \
  --title "Traffic by Device" --dark --output chart.png
```

![环形图](readme-assets/framed-donut.png)

### 📉 多系列折线图

使用 `--series-field` 在同一张图表上对比多条趋势线。

```bash
node scripts/chart.mjs --type line \
  --data '[{"x":"Q1","y":30,"series":"2024"},{"x":"Q2","y":45,"series":"2024"},{"x":"Q3","y":52,"series":"2024"},{"x":"Q4","y":61,"series":"2024"},{"x":"Q1","y":40,"series":"2025"},{"x":"Q2","y":58,"series":"2025"},{"x":"Q3","y":72,"series":"2025"}]' \
  --title "Revenue Growth" --y-title "Revenue ($M)" \
  --series-field series --dark --legend top --output chart.png
```

![多系列图表](readme-assets/framed-multi.png)

### 📏 水平参考线

使用 `--hline` 添加阈值线、目标线或买入价格线。

```bash
node scripts/chart.mjs --type line \
  --data '[{"x":"Jan 1","y":0.00072},{"x":"Jan 5","y":0.00085},{"x":"Jan 10","y":0.00091},{"x":"Jan 15","y":0.00078},{"x":"Jan 20","y":0.00062},{"x":"Jan 25","y":0.00071}]' \
  --title "Token Price" --y-title "Price (USD)" \
  --dark --show-values --hline "0.0008,#e63946,Buy Price" --output chart.png
```

![参考线图表](readme-assets/framed-hline.png)

### 🎨 条件颜色

根据阈值为柱状图/数据点着色——非常适合 KPI 仪表板。

```bash
node scripts/chart.mjs --type bar \
  --data '[{"month":"Jan","score":72},{"month":"Feb","score":45},{"month":"Mar","score":38},{"month":"Apr","score":61},{"month":"May","score":29},{"month":"Jun","score":55},{"month":"Jul","score":82},{"month":"Aug","score":47},{"month":"Sep","score":68},{"month":"Oct","score":34},{"month":"Nov","score":76},{"month":"Dec","score":91}]' \
  --x-field month --y-field score --x-sort none \
  --conditional-color "50,#e63946,#2a9d8f" --hline "50,#888,Target" \
  --title "Monthly Performance Score" --subtitle "Target: 50" --dark
```

![条件颜色图表](readme-assets/framed-conditional.png)

### ↔️ 水平柱状图

翻转坐标轴，适用于排行榜、排名或较长的类别名称。

```bash
node scripts/chart.mjs --type bar \
  --data '[{"lang":"Python","stars":95},{"lang":"JavaScript","stars":82},{"lang":"TypeScript","stars":78},{"lang":"Rust","stars":71},{"lang":"Go","stars":63},{"lang":"Java","stars":58},{"lang":"C++","stars":45},{"lang":"Swift","stars":38}]' \
  --x-field lang --y-field stars --horizontal --sort desc \
  --conditional-color "60,#e63946,#2a9d8f" --bar-labels \
  --title "GitHub Stars by Language" --dark
```

![水平柱状图](readme-assets/framed-horizontal-bar.png)

### 更多图表类型

- **`point`** — 散点图
- **`candlestick`** — OHLC 金融 K 线图（`--open-field`, `--high-field`, `--low-field`, `--close-field`）
- **`heatmap`** — 网格热力图（`--color-value-field`, `--color-scheme viridis`）
- **堆叠柱状图** — `--type bar --stacked --color-field category`
- **成交量叠加** — 使用 `--volume-field` 实现双 Y 轴
- **迷你图** — 使用 `--sparkline` 生成小型内联图表（80×20，无坐标轴）

---

## 简写语法

不想写 JSON？使用简写格式：

```bash
node scripts/chart.mjs --type bar \
  --data "Mon:10,Tue:25,Wed:18,Thu:30,Fri:22,Sat:35,Sun:28" \
  --title "Weekly Activity" --dark --output chart.png
```

![简写示例](readme-assets/framed-shorthand.png)

格式：`标签:值,标签:值,...`

---

## 暗色模式与亮色模式

使用 `--dark` 开启暗色背景（适合 Discord、Slack、暗色仪表板）：

![暗色模式](readme-assets/framed-horizontal.png)

不加 `--dark` 则为亮色模式（适合报告、邮件、浅色界面）：

![亮色模式](readme-assets/framed-bar.png)

**机器人使用小贴士：** 根据时间自动切换——在 20:00–07:00 之间使用 `--dark`。

---

## 警报风格图表

内置的监控和告警专用选项：

```bash
node scripts/chart.mjs --type line --data '[...]' \
  --title "Iran Strike Odds (48h)" \
  --show-change --focus-change --show-values --dark \
  --output alert.png
```

| 选项 | 效果 |
|------|--------|
| `--show-change` | 标注首尾数据点之间的百分比变化 |
| `--focus-change` | 将 Y 轴缩放至数据范围的 2 倍以突出变化 |
| `--focus-recent N` | 只显示最近 N 个数据点 |
| `--show-values` | 在图表上标注最大值/最小值 |

---

## 通过管道传入数据

从标准输入读取：

```bash
curl -s api.example.com/metrics | node scripts/chart.mjs --type line --dark --output metrics.png
echo '[{"x":"A","y":1},{"x":"B","y":2}]' | node scripts/chart.mjs --output out.png
```

---

## 选项参考

### 核心选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--type` | `line`, `bar`, `area`, `point`, `pie`, `donut`, `candlestick`, `heatmap` | `line` |
| `--data` | JSON 数组或简写格式 `key:val,...` | stdin |
| `--output` | 输出文件路径 | `chart.png` |
| `--title` | 图表标题 | — |
| `--subtitle` | 标题下方的副标题 | — |
| `--width` | 宽度（像素） | `600` |
| `--height` | 高度（像素） | `300` |
| `--dark` | 暗色主题 | `false` |
| `--svg` | 输出 SVG 格式（而非 PNG） | `false` |

### 坐标轴选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--x-field` | X 轴字段名 | `x` |
| `--y-field` | Y 轴字段名 | `y` |
| `--x-title` / `--y-title` | 坐标轴标签 | 字段名 |
| `--x-type` | `ordinal`（分类）, `temporal`（时间）, `quantitative`（数值） | `ordinal` |
| `--y-domain` | Y 轴范围，格式为 `"最小值,最大值"` | 自动 |
| `--y-format` | `percent`, `dollar`, `compact`, `decimal4`, `integer`, `scientific` | 自动 |

### 样式选项
| 选项 | 说明 | 默认值 |
|--------|-------------|---------|
| `--color` | 主色调 | `#e63946` |
| `--color-scheme` | Vega 配色方案（如 `viridis`, `category10`） | — |
| `--no-grid` | 移除网格线 | `false` |
| `--legend` | `top`, `bottom`, `left`, `right`, `none` | — |
| `--hline` | 参考线：格式为 `"值,颜色,标签"`（可重复使用） | — |

### 多系列选项
| 选项 | 说明 |
|--------|-------------|
| `--series-field` | 用于拆分为多条线的分组字段 |
| `--stacked` | 堆叠柱状图/面积图 |
| `--color-field` | 颜色编码字段 |

### 标注选项
| 选项 | 说明 |
|--------|-------------|
| `--show-change` | 显示百分比变化标注 |
| `--focus-change` | 缩放 Y 轴以突出变化 |
| `--focus-recent N` | 只显示最近 N 个数据点 |
| `--show-values` | 标注最大值/最小值 |
| `--annotations` | JSON 格式的事件标记数组：`[{"x":"14:00","label":"News"}]` |

---

## Y 轴格式化

```bash
--y-format dollar    # → $1,234.56
--y-format percent   # → 45.2%
--y-format compact   # → 1.2K, 3.4M
--y-format decimal4  # → 0.0004
--y-format integer   # → 1,234
```

也可以传入任意 [d3-format](https://github.com/d3/d3-format) 字符串：`--y-format ',.3f'`

---

## 专为 Fly.io / VPS / Docker 设计

这个 Skill 专为无法（或不想）安装浏览器的无界面服务器环境而构建：

- **Fly.io** — 通过 `flyctl deploy` 即可直接使用，无需特殊 Dockerfile。
- **Docker** — 无需 `apt-get install` 安装 Cairo/Pango 等依赖，只需 `npm install`。
- **VPS** — 只要有 Node.js 18+ 即可运行，无需 GPU，无需显示服务器。
- **CI/CD** — 可在 GitHub Actions、GitLab CI 等环境中生成图表。

其原理：[Vega-Lite](https://vega.github.io/vega-lite/) 原生渲染为 SVG，然后 [Sharp](https://sharp.pixelplumbing.com/)（自带预编译的 libvips 二进制文件）将其转换为 PNG。全程无需浏览器参与。

---

## 许可证

MIT

---

<p align="center">
  <sub>由 <a href="https://clawhub.ai/u/Cluka-399">@Cluka-399</a> 构建 · 发布于 <a href="https://clawhub.ai">ClawHub</a> · <a href="https://github.com/Cluka-399/chart-image">GitHub</a></sub>
</p>
