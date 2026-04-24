---
name: sunlight-analysis
version: 1.4.1
description: "生成太阳轨迹图，计算实时太阳位置，分析建筑阴影投射范围与全年日照时数，并提供热舒适度评估，适用于建筑设计与场地环境分析。当用户询问太阳位置、请求绘制太阳轨迹、分析建筑阴影、计算全年日照时间、评估热舒适度或进行地形阴影分析时触发。"
author: qrost
permissions:
  - shell:exec
---

<!-- Localized from: sun-path -->

# 太阳轨迹与环境分析

本技能为建筑师和设计师提供全面的环境分析工具。

## 依赖项

本技能需要 Python 及以下库：

- `pysolar`（太阳位置计算）
- `matplotlib`（绑图）
- `pytz`（时区处理）
- `shapely`（阴影几何计算）
- `numpy`（数学计算）
- `rasterio`（地形/DEM 阴影分析；DEM 功能为可选项）

**安装：** OpenClaw 不会自动安装 Python 包。安装本技能后（例如通过 `clawhub install sun-path`），请在技能目录中或指定其路径运行一次：`pip install -r requirements.txt`。如果脚本运行时报 `ModuleNotFoundError` 错误，请从上述列表或 `requirements.txt` 中安装缺失的包。

## 将图片发送到 Telegram

在 OpenClaw Telegram 对话中使用。生成图片的脚本（`plot_sunpath.py`、`shadow_calc.py`、`comfort_calc.py`、`annual_sun_hours.py --output`、`terrain_shadow.py --plot`）会将 PNG/JPG 写入你指定的路径。运行脚本时使用 `--output` 参数（或 `--plot` 并使用脚本默认的图片路径），然后通过 OpenClaw 消息/媒体工具**将该图片文件发送**给用户，使其在聊天中可见。

**OpenClaw 允许的路径：** 消息工具只能发送允许目录下的文件（`~/.openclaw/media/`、`~/.openclaw/agents/` 或 `/tmp`）。输出路径请始终指定为上述目录之一（例如 `--output ~/.openclaw/media/sunpath.png` 或 `/tmp/shadow.png`）；不要使用技能安装目录，否则发送将失败。

**Agent 行为：** 当用户请求太阳位置、太阳轨迹图、阴影分析、全年日照时数图表、舒适度图表或地形阴影时，**直接运行对应脚本**（使用 `exec`），并将图片输出路径指定到允许目录下；然后将生成的 PNG/JPG 发送给用户。无需请求确认；直接执行并返回图片及简要说明。

## 使用方法

### 1. 计算太阳位置

获取指定位置的当前方位角和高度角。

```bash
python3 scripts/sun_calc.py --lat 34.05 --lon -118.24 --timezone "America/Los_Angeles"
```

### 2. 生成太阳轨迹图

创建极坐标图，展示太阳全年运行轨迹。

```bash
python3 scripts/plot_sunpath.py --lat 34.05 --lon -118.24 --output sunpath.png
```

### 3. 阴影分析（2D）

模拟指定时间下简单建筑体（长方体）的阴影投射。

**参数：**

- `--lat`、`--lon`：位置坐标。
- `--time`：ISO 格式的日期时间（例如 "2024-06-21T12:00:00"）或 "now"。
- `--width`、`--depth`：建筑平面尺寸（米）。
- `--height`：建筑高度（米）。
- `--rotation`：从正北方向顺时针旋转的角度。
- `--output`：输出图片文件名。

```bash
python3 scripts/shadow_calc.py --lat 34.05 --lon -118.24 --time "2024-06-21T15:00:00" --width 15 --depth 10 --height 20 --rotation 45 --output shadow_analysis.png
```

### 4. 全年日照/阴影时数计算

计算指定点全年的**直射阳光**时数、**建筑阴影**时数或**夜间**（太阳位于地平线以下）时数。使用与阴影分析相同的建筑长方体和 2D 阴影模型；点的位置以建筑中心为原点、以米为单位表示。

**参数：**

- `--lat`、`--lon`：位置坐标。
- `--width`、`--depth`、`--height`、`--rotation`：建筑尺寸和旋转角度（与阴影分析相同）。
- `--point-x`、`--point-y`：待评估点的位置（以建筑中心为原点的米数；例如旋转角为 0 时，正北方向为正 X 值）。
- `--year`：年份（默认：当前年份）。
- `--interval`：采样间隔（分钟，默认 60；值越小越精确，但计算越慢）。
- `--timezone`：时区（例如 `Asia/Shanghai`）。
- `--output`：可选；将月度柱状图（日照/阴影/夜间时数）保存到此文件。

```bash
# 示例：建筑中心以北 15 米处的点，上海，2024 年
python3 scripts/annual_sun_hours.py --lat 31.23 --lon 121.47 --width 10 --depth 10 --height 20 --point-x 15 --point-y 0 --year 2024 --timezone Asia/Shanghai

# 包含月度图表
python3 scripts/annual_sun_hours.py --lat 31.23 --lon 121.47 --width 10 --depth 10 --height 20 --point-x 15 --point-y 0 --year 2024 --timezone Asia/Shanghai --output annual_hours.png
```

输出：日照总时数、阴影总时数和夜间总时数，以及可选的月度分布图表。

### 5. 地形阴影（DEM）

根据 GeoTIFF DEM 数据，计算指定时间下地形的阴影分布（日照 vs 阴影）。使用太阳位置和射线追踪算法；适用于中等规模的 DEM 数据（1GB 内存下建议网格不超过约 2000×2000，或处理更小的裁剪区域）。

**参数：**

- `dem`：GeoTIFF DEM 文件路径。
- `--lat`、`--lon`：用于计算太阳位置的经纬度。
- `--time`：ISO 格式的时间或 "now"（按 `--timezone` 解析后转换为 UTC）。
- `--timezone`：时区名称（例如 `Asia/Shanghai`）。
- `--output`：输出 GeoTIFF 路径（默认：`terrain_shadow.tif`）。
- `--plot`：同时保存 PNG 可视化图。
- `--step`：射线步进像素数（默认 1；值越大速度越快但精度越低）。

```bash
# 示例：当地时间中午的阴影分析
python3 scripts/terrain_shadow.py /path/to/dem.tif --lat 31.23 --lon 121.47 --time "2024-06-21T12:00:00" --timezone Asia/Shanghai --output shadow.tif --plot
```

### 6. 舒适度分析（焓湿图）

在焓湿图上可视化当前温度和湿度，评估热舒适度。

**参数：**

- `--temp`：干球温度（°C）。
- `--rh`：相对湿度（%）。
- `--output`：输出图片文件名。

```bash
python3 scripts/comfort_calc.py --temp 28 --rh 60 --output comfort_chart.png
```

## 示例

**用户：** "洛杉矶现在的太阳位置是什么？"
**操作：**

1. 确定洛杉矶的坐标（纬度：34.05，经度：-118.24）。
2. 运行 `sun_calc.py`。
3. 返回方位角和高度角。

**用户：** "显示冬至日下午 2 点上海一栋 20 米高、10×10 米建筑的阴影。"
**操作：**

1. 确定坐标（上海：31.23, 121.47）。
2. 确定时间（冬至：2024-12-21 14:00）。
3. 运行 `shadow_calc.py`：

   ```bash
   python3 scripts/shadow_calc.py --lat 31.23 --lon 121.47 --time "2024-12-21T14:00:00" --width 10 --depth 10 --height 20 --output shanghai_shadow.png
   ```

4. 返回图片。

**用户：** "新加坡现在舒适吗？温度 32°C，湿度 80%。"
**操作：**

1. 运行 `comfort_calc.py`：

   ```bash
   python3 scripts/comfort_calc.py --temp 32 --rh 80 --output singapore_comfort.png
   ```

2. 返回图片和分析结果。

**用户：** "这个点全年的日照和阴影时数是多少？建筑 10×10×20 米，点在正北 15 米处。"
**操作：**

1. 运行 `annual_sun_hours.py`，传入场地经纬度、建筑尺寸和 `--point-x 15 --point-y 0`。
2. 返回打印的摘要（直射日照/阴影/夜间时数），如果使用了 `--output` 则同时返回月度图表。

**用户：** "下午 2 点这个场地哪些地形处于阴影中？我有 DEM 数据。"
**操作：**

1. 运行 `terrain_shadow.py`，传入 DEM 路径、场地 `--lat`/`--lon`、`--time`（例如当地时间 14:00）、`--timezone`，以及 `--output`/`--plot`。
2. 返回阴影栅格和/或 PNG 图片及简要说明。
