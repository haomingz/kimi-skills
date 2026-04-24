---
name: gitlab-cli-guide
description: "提供 GitLab 命令行工具（glab）的完整参考与自动化脚本，涵盖超过30个子命令，包括合并请求创建与审查、CI/CD流水线调试、Issue管理、仓库操作和认证配置等核心工作流。适用于通过终端管理MR/Issue、调试CI失败任务、批量打标签、同步Fork和发布Release等场景。当用户提到glab、GitLab命令行、GitLab CLI、MR管理、流水线调试、glab auth、glab ci或glab mr等关键词时触发。"
metadata: {"openclaw": {"requires": {"bins": ["glab"], "anyBins": ["cosign"]}, "install": [{"id": "brew", "kind": "brew", "formula": "glab", "bins": ["glab"], "label": "Install glab (brew)"}, {"id": "download", "kind": "download", "url": "https://gitlab.com/gitlab-org/cli/-/releases", "label": "Download glab binary"}]}}
requirements:
  binaries:
    - glab
  binaries_optional:
    - cosign
  notes: |
    Requires GitLab authentication via 'glab auth login' (stores token in ~/.config/glab-cli/config.yml).
    Some features may access sensitive files: SSH keys (~/.ssh/id_rsa for DPoP), Docker config (~/.docker/config.json for registry auth).
    Review auth workflows and script contents before autonomous use.
openclaw:
  requires:
    credentials:
      - name: GITLAB_TOKEN
        description: "GitLab personal access token with 'api' scope. Used by automation scripts (e.g. post-inline-comment.py) to post MR comments via the REST API. If not set, scripts fall back to reading the token from glab CLI config (~/.config/glab-cli/config.yml)."
        required: false
        fallback: "glab config (set via glab auth login)"
    network:
      - description: "Outbound HTTPS to your GitLab instance (default https://gitlab.com)"
        scope: "authenticated API calls only; HTTPS enforced; token never sent over HTTP"
    write_access:
      - description: "Scripts in this skill can post comments, resolve threads, and approve merge requests on your behalf. Review scripts/post-inline-comment.py before use in automated or agentic contexts."
---

<!-- Localized from: gitlab-cli-skills -->

# GitLab CLI 技能集

GitLab CLI（glab）完整命令参考与工作流指南。

## 快速开始

```bash
# 首次配置
glab auth login

# 常用操作
glab mr create --fill              # 从当前分支创建合并请求
glab issue create                  # 创建 Issue
glab ci view                       # 查看流水线状态
glab repo view --web              # 在浏览器中打开仓库
```

## 技能组织结构

本技能按 GitLab 功能域路由到专项子技能：

**核心工作流：**
- `glab-mr` - 合并请求：创建、审查、批准、合并
- `glab-issue` - Issue：创建、列表、更新、关闭、评论
- `glab-ci` - CI/CD：流水线、任务、日志、产物
- `glab-repo` - 仓库：克隆、创建、Fork、管理

**项目管理：**
- `glab-milestone` - 发布计划与里程碑跟踪
- `glab-iteration` - Sprint/迭代管理
- `glab-label` - 标签管理与分类
- `glab-release` - 软件发布与版本管理

**认证与配置：**
- `glab-auth` - 登录、登出、Docker Registry 认证
- `glab-config` - CLI 配置与默认设置
- `glab-ssh-key` - SSH 密钥管理
- `glab-gpg-key` - GPG 密钥（用于提交签名）
- `glab-token` - 个人及项目访问令牌

**CI/CD 管理：**
- `glab-job` - 单个任务操作
- `glab-schedule` - 定时流水线与 Cron 任务
- `glab-variable` - CI/CD 变量与密钥
- `glab-securefile` - 流水线安全文件
- `glab-runner` - Runner 管理：列表、暂停、删除（v1.87.0 新增）
- `glab-runner-controller` - Runner 控制器与令牌管理（实验性，仅管理员）

**协作：**
- `glab-user` - 用户资料与信息
- `glab-snippet` - 代码片段（类似 GitLab Gist）
- `glab-incident` - 事件管理
- `glab-workitems` - 工作项：任务、OKR、关键成果、新一代 Epic（v1.87.0 新增）

**进阶：**
- `glab-api` - 直接调用 REST API
- `glab-cluster` - Kubernetes 集群集成
- `glab-deploy-key` - 部署密钥（用于自动化）
- `glab-stack` - 堆叠/依赖合并请求
- `glab-opentofu` - Terraform/OpenTofu 状态管理

**工具：**
- `glab-alias` - 自定义命令别名
- `glab-completion` - Shell 自动补全
- `glab-help` - 命令帮助与文档
- `glab-version` - 版本信息
- `glab-check-update` - 更新检查
- `glab-changelog` - 变更日志生成
- `glab-attestation` - 软件供应链安全
- `glab-duo` - GitLab Duo AI 助手
- `glab-mcp` - Model Context Protocol 服务器，用于 AI 助手集成（实验性）

## 何时使用 glab 与 Web 界面

**适合使用 glab 的场景：**
- 在脚本中自动化 GitLab 操作
- 以终端为中心的工作流
- 批量操作（处理多个 MR/Issue）
- 与其他 CLI 工具集成
- CI/CD 流水线工作流
- 无需切换浏览器即可快速导航

**适合使用 Web 界面的场景：**
- 带行内评论的复杂 diff 审查
- 可视化合并冲突解决
- 配置仓库设置与权限
- 跨项目的高级搜索/筛选
- 查看安全扫描结果
- 管理群组/实例级别的设置

## 常用工作流

### 日常开发

```bash
# 开始处理某个 Issue
glab issue view 123
git checkout -b 123-feature-name

# 准备好后创建 MR
glab mr create --fill --draft

# 标记为可审查
glab mr update --ready

# 审批通过后合并
glab mr merge --when-pipeline-succeeds --remove-source-branch
```

### 代码审查

```bash
# 查看待审查列表
glab mr list --reviewer=@me --state=opened

# 审查某个 MR
glab mr checkout 456
glab mr diff
npm test

# 批准
glab mr approve 456
glab mr note 456 -m "LGTM! Nice work on the error handling."
```

### CI/CD 调试

```bash
# 检查流水线状态
glab ci status

# 查看失败的任务
glab ci view

# 获取任务日志
glab ci trace <job-id>

# 重试失败的任务
glab ci retry <job-id>
```

## 决策树

### "应该先创建 MR 还是先创建 Issue？"

```
需要跟踪工作进度？
├─ 是 → 先创建 Issue（glab issue create）
│         然后：glab mr for <issue-id>
└─ 否 → 直接创建 MR（glab mr create --fill）
```

**使用 `glab issue create` + `glab mr for` 的场景：**
- 编码前需要讨论/审批
- 跟踪功能请求或 Bug
- Sprint 规划与分配
- 希望 MR 合并时自动关闭 Issue

**直接使用 `glab mr create` 的场景：**
- 快速修复或拼写错误
- 已有现成 Issue 在处理
- 紧急修复或热修复

### "应该使用哪个 CI 命令？"

```
你需要什么？
├─ 查看流水线整体状态 → glab ci status
├─ 可视化流水线视图 → glab ci view
├─ 查看特定任务日志 → glab ci trace <job-id>
├─ 下载构建产物 → glab ci artifact <ref> <job-name>
├─ 验证配置文件 → glab ci lint
├─ 触发新运行 → glab ci run
└─ 列出所有流水线 → glab ci list
```

**速查：**
- 流水线级别：`glab ci status`、`glab ci view`、`glab ci run`
- 任务级别：`glab ci trace`、`glab job retry`、`glab job view`
- 产物：`glab ci artifact`（按流水线）或通过 `glab job` 获取任务产物

### "克隆还是 Fork？"

```
你与仓库的关系？
├─ 有写入权限 → glab repo clone group/project
├─ 向他人项目贡献代码：
│   ├─ 一次性贡献 → glab repo fork + 工作 + MR
│   └─ 持续贡献 → glab repo fork，然后定期同步
└─ 仅阅读/浏览 → glab repo clone（或 view --web）
```

**适合 Fork 的场景：**
- 对原始仓库没有写入权限
- 为开源项目贡献代码
- 在不影响原始仓库的情况下进行实验
- 需要自己的副本用于长期工作

**适合 Clone 的场景：**
- 你是项目成员且有写入权限
- 在组织/团队仓库上工作
- 不需要个人副本

### "项目标签还是群组标签？"

```
标签应该放在哪？
├─ 跨多个项目使用 → glab label create --group <group>
└─ 仅限某个项目 → glab label create（在项目目录中）
```

**群组级别标签：**
- 跨组织统一标签体系
- 示例：priority::high、type::bug、status::blocked
- 集中管理，项目自动继承

**项目级别标签：**
- 项目特定的工作流
- 示例：needs-ux-review、deploy-to-staging
- 由项目维护者管理

## 相关技能

**MR 与 Issue 工作流：**
- 从 `glab-issue` 开始创建/跟踪工作
- 使用 `glab-mr` 创建关闭 Issue 的 MR
- 脚本：`scripts/create-mr-from-issue.sh` 自动化此流程

**CI/CD 调试：**
- 使用 `glab-ci` 进行流水线级别操作
- 使用 `glab-job` 进行单个任务操作
- 脚本：`scripts/ci-debug.sh` 快速诊断失败原因

**仓库操作：**
- 使用 `glab-repo` 进行仓库管理
- 使用 `glab-auth` 进行认证配置
- 脚本：`scripts/sync-fork.sh` 同步 Fork

**配置：**
- 使用 `glab-auth` 进行初始认证
- 使用 `glab-config` 设置默认值和首选项
- 使用 `glab-alias` 创建自定义快捷方式
