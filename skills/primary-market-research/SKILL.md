---
name: primary-market-research
description: "生成专业的一级市场/风险投资（PE/VC）行业研究报告，覆盖TMT、消费、医疗健康、工业等常见赛道，输出深度讨论型（15-25页）或传统行业型（30-60页）的PDF、DOCX或PPTX文档。当用户要求创建行业研究报告、赛道深度研究、市场分析报告、投资备忘录、Best Ideas摘要，或请求分析特定行业、市场趋势、竞争格局及技术图谱时触发。"
---

# 一级市场行业研究报告

以机构一级市场（PE/VC）研究风格生成专业行业研究报告。

## 参考来源

- **类型**：上传的参考文件（PDF）
- **参考文件格式**：PDF
- **语言**：中文或英文（根据用户查询自动识别；默认使用用户的语言）

## 支持的输出格式

- PDF（默认）
- DOCX
- PPTX（仅在明确要求时）

**默认输出**：PDF。如果用户明确要求 DOCX 或 PPTX，则按其要求输出。

## 工作流程

1. **理解研究范围**：根据用户查询确定目标行业、子话题、深度、页数
2. **确定报告风格**：根据用户偏好或任务上下文选择：
   - **风格 A（深度讨论型）**：观点驱动，聚焦 TMT/科技，章节编号为 01、02...，无目录
   - **风格 B（传统行业型）**：数据密集，图表丰富，带多级编号目录
3. **规划内容结构**：使用相应的结构规范（见参考文件）
4. **调研与数据收集**：按需使用网络搜索和数据源工具
5. **梳理投融资历史**：搜索该赛道的关键融资轮次、交易规模、领投机构、IPO/退出事件及资金流向趋势。数据来源包括 Crunchbase、PitchBook、CB Insights、IT桔子、烯牛数据以及公开披露的交易信息
6. **生成报告**：严格遵循风格规范和结构规范
7. **完整性审查**：确保所有图表均已编号、数据来源已标注、格式一致

## 风格选择指南

根据上下文选择报告风格：

| 判断维度 | 使用风格 A（深度讨论型） | 使用风格 B（传统行业型） |
|-----------|------------------------------|---------------------------|
| 行业 | TMT、AI、软件、SaaS | 消费、医疗健康、工业、材料 |
| 语调 | 观点鲜明、论点驱动 | 数据驱动、客观中立 |
| 图表 | 适量（原生图表，AI 研究的基准对比表） | 密集（饼图、柱状图、折线图） |
| 目录 | 无 | 有，三级层级 + 点线引导 + 页码 |
| 章节编号 | 01、02、03...，红色/深红色 | 1、1.1、1.2、2.1...，黑色 |
| 页数 | 通常 15-25 页 | 通常 30-60 页 |

详细风格规则参见 [references/style_contract.md](references/style_contract.md)。

## 结构模板

提供两种主要结构模式。详见 [references/structure_contract.md](references/structure_contract.md)。

### 风格 A 结构（深度讨论型）

```
Cover Page:
  [White background]
  [Institution logo (top-right): icon + institution name (bilingual)]
  [Main title: bold KaiTi, left-aligned, large, dark-red accent underline]
  [Author line: "Cr.: [Author Name]"]
  [Date line: "Date: YYYY-Mon"]
  [QR code (right side)]

Executive Summary (~1 page)
  [Bordered/quoted paragraph block]

01 [Chapter Title]
  [Section Heading in red/dark-red KaiTi]
  [Subsection Heading in red/dark-red KaiTi]
```

### 风格 B 结构（传统行业型）

```
Cover Page:
  [White background, ultra-minimal]
  [Full title: centered, KaiTi, large]
  [Institution logo: centered below title]
  [Institution name: centered below logo]
  [Date: centered, bottom area (YYYY.MM format)]

Table of Contents (page 2-3)
  [Title "目录": centered, large character spacing]
  [1  [Main Chapter]..................p3]
  [  1.1 [Section]...................p3]

Content Pages:
  [Header: report title centered + horizontal rule below]
  [Footer: page number]
```

## 字体策略

### 中文报告
- **标题**：楷体（KaiTi）——书法风格，彰显机构特色
- **风格 A 正文**：宋体（SimSun）——正式衬线风格
- **风格 B 正文**：华文楷体（STKaitiSC-Regular）——与标题字体家族保持一致
- **西文**：Times New Roman（正文 + 斜体用于来源标注）、Arial Bold（页眉强调）
- **图表标签**：等线（DengXian）或 Calibri（用于英文标签）
- 所有文档文本路径统一使用支持 CJK 的字体

### 英文报告
- **标题**：Georgia 或 Times New Roman——机构风格衬线字体
- **正文**：Times New Roman 或 Garamond——正式、易读
- **图表标签/表格**：Calibri 或 Arial
- **页眉强调**：Arial Bold

### 通用规则
- 当参考字体不可用时，优先选择同一视觉系列的替代字体
- 双语内容中，确保 CJK 和西文字体在字重和大小上协调统一

## 图表编号

- **图片**：顺序编号，标题在下方——"图 N"（中文）或"Figure N"（英文）
- **表格**：顺序编号，标题在上方——"表 N"（中文）或"Table N"（英文）
- 每个图表下方标注数据来源："数据来源：xxx"（中文）或"Source: xxx"（英文）
- 风格 B 中每个主要章节重新编号；风格 A 全文连续编号

## 来源标注规则

- 每个数据点、统计数字或论断必须标明来源
- 行内标注：在括号内或脚注中注明来源
- 图表：每个图/表下方标注"数据来源："（中文）或"Source:"（英文）
- 优先来源：政府数据库、行业协会、上市公司披露文件、知名分析师报告、权威媒体

## 质量检查清单

- [ ] 封面页与所选风格（风格 A 或 B）精确匹配
- [ ] 配色方案与所选风格一致——不使用自定义深色主题或现代渐变
- [ ] 所有章节/小节编号一致且符合所选编号规则
- [ ] 目录带有点线引导和页码（仅风格 B）
- [ ] 所有内容页带有页眉横线（风格 B）
- [ ] 所有图表均已编号并添加标题
- [ ] 所有数据点均已标注来源
- [ ] 字体按语言统一使用（中文报告使用 CJK 字体，英文报告使用衬线字体）
- [ ] 表格边框简洁：无竖线，表头上下有边框，表格上下有粗边框（风格 B）
- [ ] 机构/出版方标识出现在文档中（logo 区域或页眉文字）
- [ ] 文档中无占位符文本残留
