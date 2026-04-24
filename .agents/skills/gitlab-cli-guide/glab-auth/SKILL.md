---
name: glab-auth
description: 管理 GitLab CLI 认证，包括登录/登出、检查认证状态、切换账户以及配置 Docker 镜像仓库访问。适用于首次设置 glab、排查认证问题、切换 GitLab 实例/账户或配置 Docker 从 GitLab 镜像仓库拉取镜像。触发关键词：auth、login、logout、认证、凭证、token、Docker 镜像仓库。
---

# glab auth

管理 GitLab CLI 认证。

## 快速开始

```bash
# 交互式登录
glab auth login

# 查看当前认证状态
glab auth status

# 登录到其他实例
glab auth login --hostname gitlab.company.com

# 登出
glab auth logout
```

## 工作流程

### 首次设置

1. 运行 `glab auth login`
2. 选择认证方式（token 令牌或浏览器）
3. 按照提示操作，连接你的 GitLab 实例
4. 使用 `glab auth status` 验证

### 切换账户/实例

1. **从当前账户登出：**
   ```bash
   glab auth logout
   ```

2. **登录到新实例：**
   ```bash
   glab auth login --hostname gitlab.company.com
   ```

3. **验证：**
   ```bash
   glab auth status
   ```

### Docker 镜像仓库访问

1. **配置 Docker 凭证助手：**
   ```bash
   glab auth configure-docker
   ```

2. **验证 Docker 是否可以认证：**
   ```bash
   docker login registry.gitlab.com
   ```

3. **拉取私有镜像：**
   ```bash
   docker pull registry.gitlab.com/group/project/image:tag
   ```

## 故障排查

**"401 Unauthorized"（未授权）错误：**
- 检查状态：`glab auth status`
- 验证 token 是否过期（在 GitLab 设置中查看）
- 重新认证：`glab auth login`

**多实例场景：**
- 使用 `--hostname` 参数指定实例
- 每个实例的认证信息独立维护

**Docker 认证失败：**
- 重新运行：`glab auth configure-docker`
- 检查 Docker 配置：`cat ~/.docker/config.json`
- 确认凭证助手已设置：`"credHelpers": { "registry.gitlab.com": "glab-cli" }`

## 子命令

详细参数文档请参见 [references/commands.md](references/commands.md)：
- `login` - 向 GitLab 实例进行认证
- `logout` - 从 GitLab 实例登出
- `status` - 查看认证状态
- `configure-docker` - 配置 Docker 使用 GitLab 镜像仓库
- `docker-helper` - Docker 凭证助手
- `dpop-gen` - 生成 DPoP 令牌

## 相关技能

**初始设置：**
- 完成认证后，参见 `glab-config` 设置 CLI 默认配置
- 参见 `glab-ssh-key` 进行 SSH 密钥管理
- 参见 `glab-gpg-key` 设置提交签名

**仓库操作：**
- 参见 `glab-repo` 克隆仓库
- 首次克隆/推送前需要先完成认证
