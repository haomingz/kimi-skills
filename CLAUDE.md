# kimi-skills — 项目上下文

本仓库是 Kimi 官方技能库的本地镜像，用于离线访问和版本管理。

## 目录结构

- `skills/<名称>/` — 每个技能一个目录，`SKILL.md` 为入口文件
- `scripts/` — 浏览器 JS 片段（供 Agent 通过 Playwright MCP 的 `browser_evaluate` 执行）和 Python 脚本（本地审计与解压）
- `.claude/skills/kimi-sync.md` — Claude Code 自动加载的技能：完整的 Kimi 技能同步流程

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

推荐方式：告诉 Claude Code「用 kimi-sync 技能同步技能」，Claude 会自动通过 Playwright MCP 完成全流程。

手动方式（Playwright MCP 执行 JS 片段 + 本地 Python 脚本）：
1. `browser_navigate` 打开 `https://www.kimi.com/extensions?tab=skill`（技能标签页）
2. `browser_evaluate` 执行 `scripts/kimi-list.js` → 获取当前 Kimi 技能名列表
3. `python scripts/kimi-audit.py --kimi-names "..."` → 找出缺失技能，生成 `window._kimiTargets`
4. `browser_evaluate` 注入 targets + 执行 `scripts/kimi-download.js` → 下载 zip
5. `python scripts/kimi-extract.py` → 解压到 `skills/`
6. `git add skills && git commit`

> **Playwright 模式**：`--extension` 模式驱动你本地已登录的 Chrome（工具名 `mcp__playwright__browser_*`，下载落到真实 Chrome 下载夹）；隔离模式则用独立浏览器（需在其中登录，下载落到 `.playwright-mcp/`）。

完整步骤与时序约束详见 `.claude/skills/kimi-sync.md`。

## 关键约束

- **下载入口在「⋯ 更多」菜单**：当前 Kimi UI（2026）下，每张技能卡的下载按钮位于卡片 `.skill-more-btn`（⋯ 更多）弹出的菜单项「下载」中；未安装的技能（按钮显示「安装」）需先点安装。`kimi-download.js` 已内置这套流程。
- **当前 UI 选择器**：卡片 `.skill-card`、名称 `.skill-card-title`、滚动容器 `main.skill-page`、更多菜单项 `.skill-menu-item`。UI 改版导致抓取/下载失效时，对照 `.claude/skills/kimi-sync.md` 末尾的选择器表重新确认。
- **5.5 秒下载间隔**：浏览器会拦截/合并快速连续下载，`kimi-download.js` 中已内置延迟
- **去重解压**：浏览器产生的 `skill (1).zip` 重复文件由 `kimi-extract.py` 自动处理，只保留最新版本
- **下载目录随模式而变**：`--extension` 模式下载落到真实 Chrome 下载夹（`kimi-extract.py` 无参即可，注册表自动定位，支持 `F:\Downloads` 这类重定向）；隔离模式落到 `.playwright-mcp/`（需 `--downloads-dir` 指定）
- **排除 kimi-cli 技能**：`kimi-audit.py` 的 `KIMI_CLI_SKILLS` 集合已默认排除这 9 个技能

## Credits 与 License

- Kimi 官方技能版权归 [Moonshot AI](https://www.moonshot.cn/) 及各技能作者所有
- kimi-cli 技能采用 Apache 2.0 许可
- 本仓库脚本与文档采用 MIT 许可
