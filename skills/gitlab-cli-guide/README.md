```
   ____ _ _   _          _        ____ _     ___   ____  _    _ _ _     
  / ___(_) |_| |    __ _| |__    / ___| |   |_ _| / ___|| | _(_) | |___ 
 | |  _| | __| |   / _` | '_ \  | |   | |    | |  \___ \| |/ / | | / __|
 | |_| | | |_| |__| (_| | |_) | | |___| |___ | |   ___) |   <| | | \__ \
  \____|_|\__|_____\__,_|_.__/   \____|_____|___| |____/|_|\_\_|_|_|___/
                                                                        
```

# GitLab CLI 技能集

一组遵循 Agent Skills 格式的 AI 编码代理技能集合。这些技能使 AI 代理能够高效使用 GitLab CLI（`glab`）。

## 可用技能

### 技能列表

- [`glab-auth`](./glab-auth)
- [`glab-alias`](./glab-alias)
- [`glab-api`](./glab-api)
- [`glab-attestation`](./glab-attestation)
- [`glab-changelog`](./glab-changelog)
- [`glab-check-update`](./glab-check-update)
- [`glab-ci`](./glab-ci)
- [`glab-cluster`](./glab-cluster)
- [`glab-completion`](./glab-completion)
- [`glab-config`](./glab-config)
- [`glab-deploy-key`](./glab-deploy-key)
- [`glab-duo`](./glab-duo)
- [`glab-gpg-key`](./glab-gpg-key)
- [`glab-help`](./glab-help)
- [`glab-incident`](./glab-incident)
- [`glab-issue`](./glab-issue)
- [`glab-iteration`](./glab-iteration)
- [`glab-job`](./glab-job)
- [`glab-label`](./glab-label)
- [`glab-mcp`](./glab-mcp)
- [`glab-milestone`](./glab-milestone)
- [`glab-mr`](./glab-mr)
- [`glab-opentofu`](./glab-opentofu)
- [`glab-release`](./glab-release)
- [`glab-repo`](./glab-repo)
- [`glab-schedule`](./glab-schedule)
- [`glab-securefile`](./glab-securefile)
- [`glab-snippet`](./glab-snippet)
- [`glab-ssh-key`](./glab-ssh-key)
- [`glab-stack`](./glab-stack)
- [`glab-token`](./glab-token)
- [`glab-user`](./glab-user)
- [`glab-variable`](./glab-variable)
- [`glab-version`](./glab-version)

## 安装

### OpenClaw / Agent Skills

```bash
npx skills add vince-winkintel/gitlab-cli-skills
```

### Claude.ai（组织技能）

Claude.ai 要求上传一个仅包含一个 `SKILL.md` 的 zip 包。从[最新发布版本](https://github.com/vince-winkintel/gitlab-cli-skills/releases/latest)下载预构建的 `claude-skill.zip`，然后在组织的**设置 → 自定义技能**中上传。

该 zip 包含一个合并后的 `SKILL.md`，将 37+ 个子技能整合为一份完整的 glab 参考文档。

**自行构建：**

```bash
bash scripts/build-claude-skill.sh
# 输出：./claude-skill.zip
```

## 使用方式

技能会在检测到相关任务时自动激活。示例提示：

- "登录 GitLab CLI"
- "检查 glab 认证状态"
- "配置 GitLab Docker 认证"

## 前置条件

- 已安装 GitLab CLI（`glab`）
- GitLab 访问令牌或浏览器认证

## 安装 glab（Homebrew）

```bash
brew install glab
```

## 许可证

MIT
