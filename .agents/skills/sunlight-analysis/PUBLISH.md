# sun-path — 版本与发布

## 版本（当前：1.3.0）

- 版本号在 `SKILL.md` 前言（front matter）的 `version` 字段中设置。
- 发布前，确保没有调试或仅用于测试的代码。可选择在 git 中打标签：
  `git tag skill/sun-path-v1.3.0`

## 部署到 SSH OpenClaw（VPS）

从你的**本地**项目根目录执行（替换为你的密钥路径和主机地址）：

```bash
rsync -avz -e "ssh -i /path/to/your-key.key" \
  ClawSkills/sun-path/ \
  ubuntu@170.9.8.41:~/.openclaw/skills/sun-path/
```

同步完成后，VPS 上的 OpenClaw 将在下次会话时加载新版本；无需重启服务。

## 发布到 ClawHub（公开安装）

**执行环境：** 使用你的**本地机器**（Mac 上的 zsh），而非 VPS。你的仓库是唯一数据源；从本地发布可确保上传的文件与你版本控制的内容完全一致。VPS 仅用于运行 OpenClaw（通过 rsync 部署）；ClawHub 发布请在你的开发机器上操作。

1. **安装 CLI 并登录**（首次使用，在你的 Mac 上）：

   ```bash
   npm i -g clawhub
   clawhub login
   ```
   按提示操作（浏览器或 `--token`）完成登录。

2. **发布本技能**（从你的本地项目根目录）：

   ```bash
   clawhub publish ClawSkills/sun-path --slug sun-path --name "Sun Path & Environmental Analysis" --version 1.3.0 --tags latest --changelog "Annual sun hours, terrain DEM shadow, doc updates"
   ```

   如果 slug 已存在，则会创建一个新版本。你可以省略或缩短 `--changelog`。

3. **后续更新**：升级版本号（例如升至 1.3.1），然后运行：

   ```bash
   clawhub publish ClawSkills/sun-path --slug sun-path --version 1.3.1 --tags latest --changelog "Bug fix: ..."
   ```

发布后，其他人可通过 `clawhub install sun-path` 进行安装。

**注意：** 发布前，请将 `clawhub.json` 中的 `support_url` 和 `homepage` 设置为你实际的仓库 URL。
