# kimi-skills — 项目上下文

本仓库是 Kimi 官方技能库的本地镜像，用于离线访问和版本管理。

## 目录结构

- `skills/<名称>/` — 每个技能一个目录，`SKILL.md` 为入口文件
- `scripts/` — 浏览器 JS 片段（优先在 Agent 内置浏览器中执行；没有内置浏览器时再用 Playwright MCP 或其他浏览器 MCP）和 Python 脚本（本地审计与解压）
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

推荐方式：告诉 Agent「用 kimi-sync 技能同步技能」。浏览器按这个顺序选：

1. **Agent 内置浏览器**（优先，例如 Cursor 的 `browser_navigate` / `browser_cdp`）
2. 没有内置浏览器时，再用 **Playwright MCP**（`--extension` 驱动本机已登录 Chrome；隔离模式需在该浏览器里登录）
3. 再没有，就用其他能打开页面并执行 JS 的浏览器 MCP

页面地址是 `https://www.kimi.com/skills`。内置浏览器用 `Runtime.evaluate` 跑 `scripts/kimi-list.js`；Playwright 用 `browser_evaluate`。随后 `kimi-audit.py` 对名称，再按文件树比对内容，下载缺失或有更新的 zip，解压到 `skills/`。

> Playwright `--extension` 的下载进真实 Chrome 下载夹；隔离模式进 `.playwright-mcp/`。内置浏览器往往不能把文件存进系统下载夹，改用页面返回的签名 zip URL，用 `curl` 下载。

完整步骤与时序约束详见 `.claude/skills/kimi-sync.md`。

## 关键约束

- **下载入口在「⋯ 更多」菜单**：菜单项文案是「下载」或 Download。未添加的技能（按钮为「安装」/ Add）需先添加。内置浏览器优先走签名 zip URL，菜单点击是给能保存下载文件的浏览器用的后备。
- **分类默认只渲染约 10 张卡片**：抓列表前要点 `button.skill-section-overflow`（View … more），`kimi-list.js` 已内置。选择器改版时对照 `.claude/skills/kimi-sync.md` 末尾的表。
- **5.5 秒下载间隔**：浏览器会拦截/合并快速连续下载，`kimi-download.js` 中已内置延迟
- **去重解压**：浏览器产生的 `skill (1).zip` 重复文件由 `kimi-extract.py` 自动处理，只保留最新版本
- **下载目录随模式而变**：`--extension` 模式下载落到真实 Chrome 下载夹（`kimi-extract.py` 无参即可，注册表自动定位，支持 `F:\Downloads` 这类重定向）；隔离模式落到 `.playwright-mcp/`（需 `--downloads-dir` 指定）
- **排除 kimi-cli 技能**：`kimi-audit.py` 的 `KIMI_CLI_SKILLS` 集合已默认排除这 9 个技能

## Credits 与 License

- Kimi 官方技能版权归 [Moonshot AI](https://www.moonshot.cn/) 及各技能作者所有
- kimi-cli 技能采用 Apache 2.0 许可
- 本仓库脚本与文档采用 MIT 许可
