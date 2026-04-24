# kimi-skills — 项目上下文

本仓库是 Kimi 官方技能库的本地镜像，用于离线访问和版本管理。

## 目录结构

- `skills/<名称>/` — 每个技能一个目录，`SKILL.md` 为入口文件
- `scripts/` — 浏览器 JS 片段和 PowerShell 辅助脚本，用于下载与审计技能

## 技能来源说明

### Kimi 官方技能（120 个）

来自 [kimi.com](https://www.kimi.com/) 的官方 Kimi Picks 技能库，分为以下几类：

- **投资研究与金融分析**：equity-researcher、financial-report-reader、stock-tech-analysis、cashflow-valuation 等
- **营销与内容创作**：ad-copywriter、seo-copywriting-guide、wechat-post-craft、xhs-note-creator 等
- **软件开发工程**：code-safety-audit、api-doc-gen、tdd-coach、web-security-audit 等
- **数据分析与可视化**：chart-gen、auto-stat-test、outlier-scan、split-test-evaluator 等
- **产品与项目管理**：idea-to-prd、gantt-chart-builder、incident-retrospective 等
- **写作与学术研究**：research-paper-refiner、xindaya-translator、flashcard-studio 等
- **职场与效率提升**：resume-craft、interview-simulator、pro-email-composer 等
- **法律与合规**：legal-contract-gen、compliance-review-planner、tos-risk-checker 等
- **视觉设计与创意排版**：ui-blueprint、sci-paper-cn、photo-magazine-cn 等

### kimi-cli 工具技能（9 个）

来自 [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli)，与官方技能存放在同一目录：

`codex-worker`、`feature-smoke-test`、`gen-changelog`、`gen-docs`、`gen-rust`、`pull-request`、`release`、`translate-docs`、`worktree-status`

在对比 Kimi 官方列表时，需将上述 9 个排除在外。

## 更新技能流程

详见 `README.md`，简要步骤：

1. 浏览器控制台运行 `scripts/kimi-list.js` → 获取当前 Kimi 技能名列表
2. 运行 `.\scripts\kimi-audit.ps1 -KimiNames "..."` → 查看缺失技能，自动生成 `window._kimiTargets`
3. 浏览器控制台设置 targets → 运行 `scripts/kimi-download.js` 下载
4. 运行 `.\scripts\kimi-extract.ps1` 解压
5. `git add skills && git commit`

## 关键约束

- **zip 下载按钮仅在安装后出现**：需先点击 Add 安装技能才能下载完整 zip 包
- **5.5 秒下载间隔**：Chrome 会拦截快速连续下载，`kimi-download.js` 中已内置延迟
- **去重解压**：Chrome 产生的 `skill (1).zip` 重复文件由 `kimi-extract.ps1` 自动处理，只保留最新版本
- **排除 kimi-cli 技能**：`kimi-audit.ps1` 的 `-ExcludeLocal` 参数已默认排除这 9 个技能

## Credits 与 License

- Kimi 官方技能版权归 [Moonshot AI](https://www.moonshot.cn/) 及各技能作者所有
- kimi-cli 技能采用 Apache 2.0 许可
- 本仓库脚本与文档采用 MIT 许可
