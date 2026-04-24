# kimi-skills

[Kimi](https://www.kimi.com/) 官方技能库的本地镜像，收录全部 120 个官方技能，以及 [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) 项目自带的 9 个工具技能，共 **129 个技能**。

每个技能以独立目录存放在 `skills/` 下，包含 `SKILL.md` 主文件及可选的参考资料、脚本和模板。

> 技能分类介绍与完整列表见 [skills/README.md](skills/README.md)。

---

## 仓库结构

```
skills/
  <技能名>/
    SKILL.md          # 技能主定义文件
    references/       # 参考文档（部分技能）
    scripts/          # 辅助脚本（部分技能）
    ...
scripts/
  kimi-list.js        # 浏览器片段：获取当前 Kimi 技能列表
  kimi-download.js    # 浏览器片段：批量下载技能 zip 文件
  kimi-extract.ps1    # PowerShell：解压 zip 到 skills/ 目录（含去重）
  kimi-audit.ps1      # PowerShell：对比本地与 Kimi 官方，打印缺失清单
```

---

## 如何更新 / 补齐技能

### 1. 获取 Kimi 当前技能列表

在 https://www.kimi.com/ 打开 Kimi Picks 技能面板，在开发者工具控制台中运行：

```js
// scripts/kimi-list.js — 输出所有技能名（逗号分隔）
```

### 2. 审计缺失技能

```powershell
.\scripts\kimi-audit.ps1 -KimiNames "skill-a,skill-b,..."
```

自动打印缺失技能清单和可直接粘贴的 `window._kimiTargets = [...]`。

### 3. 下载缺失技能

在浏览器控制台（已打开技能面板）中执行：

```js
// 可选：只下载缺失的技能
window._kimiTargets = ["skill-a", "skill-b"];

// 然后粘贴 scripts/kimi-download.js 的内容
```

Chrome 会询问是否允许多文件下载，点击**允许**。  
每个技能约需 6 秒（5.5 秒延迟，防止 Chrome 同时下载拦截）。

### 4. 解压到仓库

```powershell
.\scripts\kimi-extract.ps1
# 可选参数：
.\scripts\kimi-extract.ps1 -DownloadsDir "D:\Downloads" -HoursBack 6
```

### 5. 提交

```bash
git add skills
git commit -m "Update Kimi skills $(date +%Y-%m-%d)"
```

---

## 技术说明

- **为何需要"添加"技能才能下载 zip？** Kimi 只有在安装（点击 Add）后才会显示整个技能包的 zip 下载按钮；未安装时只能逐文件下载。
- **为何需要 5.5 秒延迟？** Chrome 会拦截来自同一来源的快速连续下载，≥5 秒的间隔可避免此问题。
- **去重处理：** Chrome 将重复下载保存为 `skill (1).zip`、`skill (2).zip` 等，`kimi-extract.ps1` 会自动保留同名最新文件并去重解压。

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
