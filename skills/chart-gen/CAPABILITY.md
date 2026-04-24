# chart-generation 能力说明

提供能力：chart-generation
Skill 名称：chart-image

## 方法

### lineChart

**输入：**
- data：数据点数组（包含 x/y、time/value 或 time/price 字段的对象）
- title：（可选）图表标题
- groupBy：（可选）多系列图表的分组字段
- options：（可选）附加选项
  - dark：boolean - 使用暗色主题
  - focusRecent：number - 缩放至最近 N 个数据点
  - showChange：boolean - 显示百分比变化标注
  - showValues：boolean - 在数据点上显示数值标签

**调用方式：**
```bash
# 将数据写入临时文件
echo '${JSON.stringify(data)}' > /tmp/chart-data.json

# 生成图表
node /data/clawd/skills/chart-image/scripts/chart.mjs \
  --type line \
  --data "$(cat /tmp/chart-data.json)" \
  --title "${title}" \
  ${options.dark ? '--dark' : ''} \
  ${options.focusRecent ? '--focus-recent ' + options.focusRecent : ''} \
  ${options.showChange ? '--show-change' : ''} \
  ${options.showValues ? '--show-values' : ''} \
  --output /tmp/chart-${Date.now()}.png
```

**输出：** `{ path: string }` - 生成的 PNG 文件路径

---

### barChart

**输入：**
- data：包含标签和数值字段的对象数组
- title：（可选）图表标题
- options：（可选）附加选项
  - dark：boolean - 使用暗色主题
  - showValues：boolean - 在柱状图上显示数值标签

**调用方式：**
```bash
# 将数据写入临时文件
echo '${JSON.stringify(data)}' > /tmp/chart-data.json

# 生成图表
node /data/clawd/skills/chart-image/scripts/chart.mjs \
  --type bar \
  --data "$(cat /tmp/chart-data.json)" \
  --title "${title}" \
  ${options.dark ? '--dark' : ''} \
  ${options.showValues ? '--show-values' : ''} \
  --output /tmp/chart-${Date.now()}.png
```

**输出：** `{ path: string }` - 生成的 PNG 文件路径

---

### areaChart

**输入：**
- data：数据点数组
- title：（可选）图表标题
- options：（可选）与 lineChart 相同

**调用方式：**
```bash
node /data/clawd/skills/chart-image/scripts/chart.mjs \
  --type area \
  --data '${JSON.stringify(data)}' \
  --title "${title}" \
  --output /tmp/chart-${Date.now()}.png
```

**输出：** `{ path: string }` - 生成的 PNG 文件路径

---

## 注意事项

- 所有方法默认将 PNG 图片输出到 /tmp 目录
- 在本地时间 20:00-07:00 之间使用 `--dark` 参数以获得更好的夜间视觉效果
- 对于时间序列数据，数据点的 `time` 或 `x` 字段应为 ISO 格式或可读的时间字符串
- 此 Skill 底层使用 Vega-Lite——完整选项请参阅 SKILL.md
