# GitLab CI 流水线模板

即用型 `.gitlab-ci.yml` 模板，适用于常见工作流。

## 可用模板

### 1. nodejs-basic.yml

**适用于：** 具有基本 CI/CD 需求的简单 Node.js 项目

**包含：**
- 带缓存的依赖安装
- 代码检查（Linting）
- 带覆盖率报告的测试
- 构建步骤
- 手动生产环境部署

**最适合：**
- 中小型 Node.js 应用
- 部署流程简单的项目
- GitLab CI 入门项目

---

### 2. nodejs-multistage.yml

**适用于：** 拥有多个环境的 Node.js 项目

**包含：**
- 独立的单元测试和集成测试作业
- 自动部署到预发布环境（`develop` 分支）
- 手动部署到生产环境（`main` 分支）
- 合并请求的 Review App
- 环境清理作业

**最适合：**
- 需要预发布环境的生产应用
- 使用 GitFlow 或类似分支策略的团队
- 需要 Review App 进行 MR 测试的项目

---

### 3. docker-build.yml

**适用于：** 使用 Docker 的容器化应用

**包含：**
- Docker 镜像构建并推送到 GitLab Container Registry
- 容器测试（在镜像内运行测试）
- 使用 Trivy 进行安全扫描
- 多标签策略（SHA、latest、发布标签）
- Kubernetes 部署示例
- Registry 清理作业

**最适合：**
- 微服务和容器化应用
- Kubernetes 部署
- 需要镜像安全扫描的项目
- Docker 优先的开发工作流

---

## 使用方式

### 快速开始

1. **复制合适的模板：**
   ```bash
   cp glab-ci/templates/nodejs-basic.yml .gitlab-ci.yml
   ```

2. **根据项目需求自定义：**
   - 更新部署命令
   - 设置环境 URL
   - 配置变量（如需要）

3. **推送前验证：**
   ```bash
   glab ci lint
   ```

4. **提交并推送：**
   ```bash
   git add .gitlab-ci.yml
   git commit -m "Add GitLab CI pipeline"
   git push
   ```

### 验证

在提交前务必验证流水线配置：

```bash
# Validate .gitlab-ci.yml in current directory
glab ci lint

# Validate a template before copying
glab ci lint --path glab-ci/templates/nodejs-multistage.yml
```

### 自定义技巧

**调整 Node.js 版本：**
```yaml
image: node:18-alpine  # Change to 16, 18, 20, etc.
```

**更换包管理器：**
```yaml
# For yarn
- yarn install --frozen-lockfile

# For pnpm
- pnpm install --frozen-lockfile
```

**更新不同 lockfile 的缓存 key：**
```yaml
cache:
  key:
    files:
      - yarn.lock      # or pnpm-lock.yaml
```

**配置部署：**
```yaml
deploy:
  script:
    - npm run deploy           # Generic
    - vercel --prod            # Vercel
    - netlify deploy --prod    # Netlify
    - aws s3 sync dist/ s3://bucket  # AWS S3
```

### 环境变量

在 GitLab 中设置所需变量：
**设置 → CI/CD → 变量**

**常用配置变量：**
- `VERCEL_TOKEN` - 用于 Vercel 部署
- `NETLIFY_AUTH_TOKEN` - 用于 Netlify 部署
- `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` - 用于 AWS
- `KUBE_CONTEXT` - 用于 Kubernetes 部署
- `DOCKER_AUTH_CONFIG` - 用于私有 Docker Registry

**保护措施：**
- ✅ 标记为 **Protected**，用于生产密钥（仅在受保护分支上可用）
- ✅ 标记为 **Masked**，在作业日志中隐藏

---

## 模板对比

| 功能 | nodejs-basic | nodejs-multistage | docker-build |
|---------|--------------|-------------------|--------------|
| **复杂度** | 简单 | 中等 | 高级 |
| **阶段数** | 5 | 5 + Review App | 4 |
| **环境** | 仅生产环境 | 预发布 + 生产 | 预发布 + 生产 |
| **测试** | 单一测试作业 | 单元 + 集成 | 容器测试 |
| **部署** | 手动 | 预发布自动，生产手动 | 预发布自动，生产手动 |
| **Docker** | 否 | 否 | 是 |
| **安全扫描** | 否 | 否 | 是（Trivy） |
| **Review App** | 否 | 是 | 否 |
| **最适合** | 简单应用 | 多环境应用 | 容器化应用 |

---

## 进阶模式

### Monorepo 支持

添加路径过滤器，仅在特定目录发生变更时运行作业：

```yaml
test:frontend:
  script:
    - npm run test
  rules:
    - changes:
        - frontend/**/*
        - package.json

test:backend:
  script:
    - npm run test
  rules:
    - changes:
        - backend/**/*
        - package.json
```

### 矩阵构建（多 Node 版本）

跨多个 Node.js 版本测试：

```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ["16", "18", "20"]
  image: node:${NODE_VERSION}-alpine
  script:
    - npm ci
    - npm test
```

### 定时流水线

运行夜间构建或清理作业：

**设置 → CI/CD → 定时任务**

然后添加规则：

```yaml
cleanup:
  script:
    - cleanup-old-artifacts.sh
  rules:
    - if: '$CI_PIPELINE_SOURCE == "schedule"'
```

---

## 故障排除

### 流水线验证失败

```bash
# Check syntax errors
glab ci lint

# Common issues:
# - Indentation (YAML is whitespace-sensitive)
# - Missing required fields (script, stage)
# - Invalid stage names
```

### 缓存不生效

```bash
# Verify cache key matches your lockfile
cache:
  key:
    files:
      - package-lock.json  # Must match actual file

# Check cache paths exist
cache:
  paths:
    - node_modules/  # Verify this directory is created
```

### 作业报错 "npm: command not found"

```bash
# Ensure correct base image
image: node:20-alpine  # Must be a Node.js image
```

### 后续作业无法获取产物

```yaml
build:
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour  # Extend if jobs run longer

deploy:
  needs:
    - job: build
      artifacts: true  # Explicitly download artifacts
```

---

## 相关技能

- **[glab-ci](../SKILL.md)** - 流水线管理的 CLI 命令
- **[pipeline-best-practices.md](../references/pipeline-best-practices.md)** - 详细的配置最佳实践
- **[glab-variable](../../glab-variable/SKILL.md)** - 管理 CI/CD 变量
- **[glab-schedule](../../glab-schedule/SKILL.md)** - 定时流水线

---

## 更多资源

- [GitLab CI/CD YAML 参考](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab CI/CD 示例](https://docs.gitlab.com/ee/ci/examples/)
- [GitLab 流水线效率优化](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)

---

**需要帮助？** 运行 `glab ci lint` 验证配置，或查看 [pipeline-best-practices.md](../references/pipeline-best-practices.md) 获取详细说明。
