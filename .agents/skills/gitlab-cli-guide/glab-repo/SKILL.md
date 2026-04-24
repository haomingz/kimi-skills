---
name: glab-repo
description: 管理 GitLab 仓库和项目，包括克隆、创建、Fork、归档、查看、更新、删除、搜索、转移和成员管理。适用于管理仓库生命周期、Fork 项目、克隆仓库、搜索项目、管理协作者或配置仓库设置等场景。触发关键词：repository、repo、project、clone、fork、创建仓库、搜索项目、协作者。
---

# glab repo

管理 GitLab 仓库和项目。

## 快速入门

```bash
# Clone a repository
glab repo clone group/project

# Create new repository
glab repo create my-new-project --public

# Fork a repository
glab repo fork upstream/project

# View repository details
glab repo view

# Search for repositories
glab repo search "keyword"
```

## 常用工作流

### 创建新项目

1. **创建仓库：**
   ```bash
   glab repo create my-project \
     --public \
     --description "My awesome project"
   ```

2. **克隆到本地：**
   ```bash
   glab repo clone my-username/my-project
   cd my-project
   ```

3. **初始化内容：**
   ```bash
   echo "# My Project" > README.md
   git add README.md
   git commit -m "Initial commit"
   git push -u origin main
   ```

### Fork 工作流

1. **Fork 上游仓库：**
   ```bash
   glab repo fork upstream-group/project
   ```

2. **克隆你的 Fork：**
   ```bash
   glab repo clone my-username/project
   cd project
   ```

3. **添加上游远程仓库：**
   ```bash
   git remote add upstream https://gitlab.com/upstream-group/project.git
   ```

4. **保持 Fork 同步：**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

**自动同步：**

使用同步脚本一键更新 Fork：
```bash
scripts/sync-fork.sh main
scripts/sync-fork.sh develop upstream
```

该脚本自动完成：拉取 → 合并 → 推送到 origin。

### 仓库管理

**查看仓库信息：**
```bash
glab repo view
glab repo view group/project  # Specific repo
glab repo view --web          # Open in browser
```

**更新仓库设置：**
```bash
glab repo update \
  --description "Updated description" \
  --default-branch develop
```

**归档仓库：**
```bash
glab repo archive download main  # Downloads .tar.gz
glab repo archive download main --format zip
```

**转移到新命名空间：**
```bash
glab repo transfer my-project --target-namespace new-group
```

**删除仓库：**
```bash
glab repo delete group/project
```

### 成员管理

**列出协作者：**
```bash
glab repo members list
```

**添加成员：**
```bash
glab repo members add @username --access-level maintainer
```

**移除成员：**
```bash
glab repo members remove @username
```

**更新成员权限：**
```bash
glab repo members update @username --access-level developer
```

### 批量操作

**克隆群组中所有仓库：**
```bash
glab repo clone -g my-group
```

**搜索并克隆：**
```bash
glab repo search "api" --per-page 10
# Then clone specific result
glab repo clone group/api-project
```

**列出你的仓库：**
```bash
glab repo list
glab repo list --member          # Only where you're a member
glab repo list --mine            # Only repos you own
```

## 故障排除

**克隆失败（权限错误）：**
- 验证是否有访问权限：`glab repo view group/project`
- 检查认证状态：`glab auth status`
- 对于私有仓库，确保使用正确的账户登录

**Fork 操作失败：**
- 检查你的命名空间中是否已存在相同的 Fork
- 确认你有 Fork 权限（部分仓库禁用了 Fork 功能）
- 尝试指定路径：`glab repo fork --fork-path username/new-name`

**转移失败：**
- 确认你有 Owner/Maintainer 权限
- 检查目标命名空间是否存在且你有创建权限
- 部分项目可能启用了转移保护

**群组克隆失败：**
- 确认群组存在且你有访问权限
- 检查是否有足够的磁盘空间
- 大型群组可能会超时 —— 建议逐个克隆特定仓库

## 相关技能

**认证与访问：**
- 参见 `glab-auth` 了解登录和认证设置
- 参见 `glab-ssh-key` 了解 SSH 密钥管理
- 参见 `glab-deploy-key` 了解部署认证

**项目配置：**
- 参见 `glab-config` 了解 CLI 默认设置
- 参见 `glab-variable` 了解 CI/CD 变量

**Fork 同步：**
- 脚本：`scripts/sync-fork.sh` 自动化上游同步

## 命令参考

完整的命令文档和所有参数请参见 [references/commands.md](references/commands.md)。

**可用命令：**
- `clone` - 克隆仓库或群组
- `create` - 创建新项目
- `fork` - Fork 仓库
- `view` - 查看项目详情
- `update` - 更新项目设置
- `delete` - 删除项目
- `search` - 搜索项目
- `list` - 列出仓库
- `transfer` - 转移到新命名空间
- `archive` - 下载仓库归档
- `contributors` - 列出贡献者
- `members` - 管理项目成员
- `mirror` - 配置仓库镜像
- `publish` - 发布项目资源
