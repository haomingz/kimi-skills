> 本文件是原先的中文 README 存档。当前说明以英文 [README.md](README.md) 为准。

# kimi-skills

[Kimi](https://www.kimi.com/) 官方技能库的本地镜像，收录全部 120 个官方技能，以及 [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) 项目自带的 9 个工具技能，共 **129 个技能**。

每个技能以独立目录存放在 `skills/` 下，包含 `SKILL.md` 主文件及可选的参考资料、脚本和模板。

> 技能分类介绍与完整列表见 [skills/README.md](skills/README.md)。

---

## 安装技能

使用 [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI，一条命令即可将本仓库的所有技能安装到你的 AI 编程助手中（支持 Claude Code、Cursor、Copilot 等 45+ 个 Agent）：

```bash
# 安装到当前项目（推荐）
npx skills add haomingz/kimi-skills

# 全局安装（对所有项目生效）
npx skills add -g haomingz/kimi-skills

# 只安装某几个技能
npx skills add haomingz/kimi-skills -s equity-researcher,chart-gen

# 查看已安装的技能
npx skills list

# 升级到最新版本
npx skills update
```

> **说明：** 首次运行 `npx skills add` 时若提示选择 Agent，选择你使用的工具（如 `claude-code`）即可；也可用 `-a claude-code` 直接指定。

---

## 仓库结构

```
skills/
  <技能名>/
    SKILL.md          # 技能主定义文件
    references/       # 参考文档（部分技能）
    scripts/          # 辅助脚本（部分技能）
    ...
.claude/skills/
  kimi-sync.md        # Claude Code 自动加载的技能：Kimi 技能同步流程
scripts/
  kimi-list.js        # 浏览器片段（供 Agent 通过 Playwright browser_evaluate 执行）
  kimi-download.js    # 浏览器片段（供 Agent 通过 Playwright browser_evaluate 执行）
  kimi-audit.py       # Python：对比本地与 Kimi 官方，打印缺失清单
  kimi-extract.py     # Python：解压 zip 到 skills/ 目录（含去重）
```

---

## 开发环境

脚本依赖纯标准库，无需额外安装。推荐用 [uv](https://github.com/astral-sh/uv) 管理 Python 环境：

```bash
# 首次：自动创建 .venv 并锁定 Python 版本
uv sync

# 之后直接运行脚本
uv run python scripts/kimi-audit.py
uv run python scripts/kimi-extract.py
```

没有 uv 的话，直接 `python scripts/kimi-audit.py` 也可以（Python ≥ 3.9）。

---

## 如何更新 / 补齐技能

### 方式一（推荐）：让 Agent 自动完成

前提：Claude Code 已启用 Playwright MCP。推荐 `--extension` 模式——直接驱动你本地已登录 kimi.com 的 Chrome（隔离模式则需在 Playwright 打开的独立浏览器里登录一次）。

直接告诉 Agent：

```
用 kimi-sync 技能，把 kimi.com 上最新的技能同步到本仓库
```

Agent 会自动：
1. 用 Playwright MCP 打开 `https://www.kimi.com/extensions?tab=skill` 技能页
2. 执行 `scripts/kimi-list.js` 获取当前技能列表
3. 调用 `scripts/kimi-audit.py` 找出缺失的技能
4. 在浏览器中逐一通过技能卡的「⋯ 更多 → 下载」下载缺失的 zip
5. 调用 `scripts/kimi-extract.py` 解压到 `skills/`
6. `git add skills && git commit`

完整的步骤和细节见 [.claude/skills/kimi-sync.md](.claude/skills/kimi-sync.md)。

---

### 方式二：手动执行（不使用 Agent）

下面的步骤需要自己操作浏览器，适合不想配置 MCP 的情况。

> `kimi-list.js` / `kimi-download.js` 的文件本体是箭头函数表达式（供 Playwright `browser_evaluate` 直接调用）。在普通开发者工具控制台运行时，需要外包一层括号并立即调用：`(<粘贴内容>)()`。

#### 1. 获取 Kimi 当前技能列表

打开 https://www.kimi.com/extensions?tab=skill （技能标签页），在开发者工具控制台运行 `(<scripts/kimi-list.js 内容>)()`，复制输出的逗号分隔名称列表。

#### 2. 审计缺失技能

```bash
uv run python scripts/kimi-audit.py --kimi-names "skill-a,skill-b,..."
```

输出缺失清单和可直接粘贴的 `window._kimiTargets = [...]`。

#### 3. 下载缺失技能

在浏览器控制台（已打开技能标签页）中粘贴：

```js
window._kimiTargets = ["skill-a", "skill-b"];  // 仅缺失的技能
(<粘贴 scripts/kimi-download.js 的全部内容>)()
```

脚本会逐一通过技能卡的「⋯ 更多 → 下载」菜单下载 zip。若 Chrome 询问是否允许多文件下载，点击**允许**。每个技能约需 6 秒（内置 5.5 秒间隔）。

#### 4. 解压到仓库

```bash
# 默认自动定位真实 Downloads 目录（含 Windows 重定向到其他盘的情况，如 F:\Downloads）
uv run python scripts/kimi-extract.py
# 如需手动指定（例如 Playwright 隔离模式的 .playwright-mcp 目录）：
uv run python scripts/kimi-extract.py --downloads-dir "D:/Downloads"
```

#### 5. 提交

```bash
git add skills
git commit -m "Sync Kimi skills $(date +%Y-%m-%d)"
```

---

## 技术说明

- **zip 下载入口在哪？** 当前 Kimi UI（2026）下，下载按钮位于每张技能卡 `.skill-more-btn`（⋯ 更多）弹出的菜单项「下载」中；未安装的技能（按钮显示「安装」）需先点安装。`kimi-download.js` 已内置整套流程。
- **为何需要 5.5 秒延迟？** 浏览器会拦截/合并来自同一来源的快速连续下载，≥5 秒的间隔可避免此问题。
- **去重处理：** 浏览器将重复下载保存为 `skill (1).zip`、`skill (2).zip` 等，`kimi-extract.py` 会自动保留同名最新文件并去重解压。
- **下载落到哪个目录？** Playwright `--extension` 模式驱动真实 Chrome，文件进你正常的下载夹（`kimi-extract.py` 无参自动定位）；隔离模式落到 Playwright 输出目录 `.playwright-mcp/`，解压时用 `--downloads-dir` 指定。

---

## Credits

- **Kimi 官方技能** — [Moonshot AI](https://www.moonshot.cn/) 出品，技能版权归原作者所有，详见各技能目录下的 `LICENSE` 文件
- **kimi-cli 技能** — 来自 [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli)（Apache 2.0 许可）
- **下载脚本与文档** — 本仓库原创内容，MIT 许可

## License

本仓库中的 **脚本文件**（`scripts/` 目录）和 **文档文件**（`README.md`、`CLAUDE.md`）采用 [MIT License](https://opensource.org/licenses/MIT) 授权。

`skills/` 目录下各技能的版权归其原始作者所有，请参阅各技能目录中的 `LICENSE` 文件。部分技能未附 LICENSE 文件，视为保留所有权利（来自 Kimi 官方平台）。

---

*本仓库为个人镜像存档，与 Moonshot AI 官方无关联。*
