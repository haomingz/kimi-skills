# GitLab CI 流水线最佳实践

本参考文档提供编写高效、可靠、易维护的 `.gitlab-ci.yml` 配置的最佳实践。

## 目录

- [缓存策略](#缓存策略)
- [多阶段流水线模式](#多阶段流水线模式)
- [覆盖率报告集成](#覆盖率报告集成)
- [安全扫描](#安全扫描)
- [常用流水线模式](#常用流水线模式)
- [性能优化](#性能优化)
- [特定环境配置](#特定环境配置)

---

## 缓存策略

有效的缓存能够通过在流水线运行之间复用依赖项和构建产物来大幅减少构建时间。

### Node.js 缓存（node_modules）

**最佳实践：基于 lockfile 哈希进行缓存**

```yaml
cache:
  key:
    files:
      - package-lock.json  # or yarn.lock, pnpm-lock.yaml
  paths:
    - node_modules/
    - .npm/  # npm cache directory
```

**原理：**
- 缓存 key 仅在依赖项变更时才更新
- 避免每次运行都执行耗时的 `npm install`
- 缓存 `.npm/` 即使缓存未命中也能加速 `npm ci`

### 按作业缓存

```yaml
variables:
  NPM_CONFIG_CACHE: "$CI_PROJECT_DIR/.npm"

cache:
  key: "$CI_COMMIT_REF_SLUG"
  paths:
    - node_modules/
    - .npm/
    - .next/cache/  # Next.js build cache

build:
  cache:
    key: "$CI_COMMIT_REF_SLUG"
    paths:
      - .next/  # Build output for reuse in deploy stage
    policy: push  # Only write to cache
```

### 缓存策略

- `pull` - 下载缓存，不更新（大多数作业的默认策略）
- `push` - 上传缓存，不下载（适合安装/构建作业）
- `pull-push` - 同时下载和上传（未指定时的默认策略）

**示例：**

```yaml
install:
  cache:
    policy: pull-push  # Update cache with fresh dependencies
  script:
    - npm ci

test:
  cache:
    policy: pull  # Only read cache, don't update
  script:
    - npm test
```

### 缓存失效

**强制刷新缓存：**
```yaml
cache:
  key: "$CI_COMMIT_REF_SLUG-v2"  # Increment version to bust cache
```

**按分支缓存：**
```yaml
cache:
  key: "$CI_COMMIT_REF_SLUG"  # Different cache per branch
```

**回退缓存 key：**
```yaml
cache:
  key:
    files:
      - package-lock.json
  fallback_keys:
    - "$CI_COMMIT_REF_SLUG"  # Use branch cache if lockfile cache miss
    - default                # Use default cache as last resort
```

---

## 多阶段流水线模式

通过清晰的阶段结构来实现更好的并行化和故障隔离。

### 标准阶段

```yaml
stages:
  - install      # Install dependencies once
  - lint         # Fast quality checks (fail early)
  - test         # Run test suites
  - build        # Create production artifacts
  - deploy       # Deploy to environments
```

### 作业间依赖

**顺序执行：**

```yaml
build:
  stage: build
  needs: [lint, test]  # Wait for both to complete
  script:
    - npm run build
```

**并行执行：**

```yaml
lint:
  stage: lint
  script:
    - npm run lint

test:unit:
  stage: test
  script:
    - npm run test:unit

test:integration:
  stage: test
  script:
    - npm run test:integration
```

由于两个测试作业之间没有依赖关系，它们会并行运行。

### 跨阶段产物共享

```yaml
install:
  stage: install
  script:
    - npm ci
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 hour  # Clean up after pipeline completes

build:
  stage: build
  needs:
    - job: install
      artifacts: true  # Download artifacts from install job
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
      - .next/
    expire_in: 1 week
```

### 基于分支的工作流

```yaml
deploy:staging:
  stage: deploy
  script:
    - deploy-to-staging.sh
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

deploy:production:
  stage: deploy
  script:
    - deploy-to-production.sh
  environment:
    name: production
    url: https://example.com
  only:
    - main
  when: manual  # Require manual approval
```

**基于 rules 的替代方案（更灵活）：**

```yaml
deploy:staging:
  stage: deploy
  script:
    - deploy-to-staging.sh
  environment:
    name: staging
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: manual

deploy:production:
  stage: deploy
  script:
    - deploy-to-production.sh
  environment:
    name: production
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
```

---

## 覆盖率报告集成

在 GitLab 合并请求中直接显示测试覆盖率。

### Jest 覆盖率（Node.js）

```yaml
test:
  stage: test
  script:
    - npm test -- --coverage --coverageReporters=text --coverageReporters=lcov
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'  # Extract coverage percentage
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/
    expire_in: 30 days
```

**说明：**
- `coverage: '/regex/'` - 提取覆盖率百分比用于徽章展示
- `coverage_report` - 启用 MR diff 中的覆盖率标注
- `cobertura` 格式 - GitLab 首选的覆盖率格式

### Vitest 覆盖率

```yaml
test:
  stage: test
  script:
    - npm test -- --coverage --reporter=verbose
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

### 覆盖率阈值

**覆盖率下降时使流水线失败：**

```yaml
test:
  script:
    - npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'
  allow_failure: false
```

### 覆盖率徽章

GitLab 会自动根据提取的覆盖率百分比生成覆盖率徽章：

```markdown
![coverage](https://gitlab.com/your-group/your-project/badges/main/coverage.svg)
```

---

## 安全扫描

将安全扫描集成到流水线中，尽早发现漏洞。

### 依赖扫描（npm audit）

```yaml
security:audit:
  stage: test
  script:
    - npm audit --audit-level=moderate
  allow_failure: true  # Don't block pipeline, but flag issues
```

**更严格的策略：**

```yaml
security:audit:
  script:
    - npm audit --audit-level=high --production
  allow_failure: false  # Block pipeline on high/critical vulnerabilities
```

### SAST（静态应用安全测试）

**使用 GitLab 内置的 SAST：**

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml

variables:
  SAST_EXCLUDED_PATHS: "spec,test,tests,tmp,node_modules"
```

### 许可证合规检查

```yaml
license:check:
  stage: test
  script:
    - npx license-checker --onlyAllow "MIT;Apache-2.0;BSD-3-Clause;ISC"
  allow_failure: true
```

### 密钥检测

**防止密钥被提交到代码库：**

```yaml
include:
  - template: Security/Secret-Detection.gitlab-ci.yml
```

### Docker 镜像扫描

```yaml
container:scan:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker pull $CI_REGISTRY_IMAGE:latest
    - docker run --rm aquasec/trivy image $CI_REGISTRY_IMAGE:latest
```

---

## 常用流水线模式

### 矩阵构建（多 Node 版本）

```yaml
test:
  stage: test
  parallel:
    matrix:
      - NODE_VERSION: ["16", "18", "20"]
  image: node:${NODE_VERSION}
  script:
    - npm ci
    - npm test
```

### 条件作业

**仅在合并请求时运行：**

```yaml
lint:mr-only:
  stage: lint
  script:
    - npm run lint
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

**仅在 main 分支运行：**

```yaml
deploy:
  stage: deploy
  script:
    - deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

**在标签上运行：**

```yaml
release:
  stage: deploy
  script:
    - create-release.sh
  rules:
    - if: '$CI_COMMIT_TAG'
```

### 手动作业与自动部署选项

```yaml
deploy:production:
  stage: deploy
  script:
    - deploy.sh
  when: manual
  allow_failure: false  # Pipeline waits for manual trigger
  environment:
    name: production
    on_stop: stop:production  # Enable environment cleanup

stop:production:
  stage: deploy
  script:
    - cleanup.sh
  when: manual
  environment:
    name: production
    action: stop
```

### 自动重试失败的作业

```yaml
test:flaky:
  script:
    - npm run test:integration
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```

### 超时配置

```yaml
build:
  script:
    - npm run build
  timeout: 30m  # Override default 1h timeout
```

---

## 性能优化

### 快速失败策略

在耗时任务之前先运行快速检查：

```yaml
stages:
  - lint       # ~30 seconds
  - test       # ~2 minutes
  - build      # ~5 minutes
  - deploy     # ~3 minutes

lint:
  stage: lint
  script:
    - npm run lint
  allow_failure: false  # Stop pipeline immediately if fails

test:
  stage: test
  needs: [lint]  # Only run if lint passes
  script:
    - npm test
```

### 并行化独立作业

```yaml
lint:eslint:
  stage: lint
  script:
    - npm run lint:eslint

lint:prettier:
  stage: lint
  script:
    - npm run lint:prettier

lint:types:
  stage: lint
  script:
    - npm run check-types
```

三个 lint 作业同时运行。

### 使用更小的 Docker 镜像

```yaml
# ❌ Slow - full image download every time
image: node:20

# ✅ Fast - smaller alpine image
image: node:20-alpine

# ✅ Even faster - cache locally built image
image: $CI_REGISTRY_IMAGE/node-build:latest
```

### 优化产物大小

```yaml
build:
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    exclude:
      - dist/**/*.map  # Exclude source maps
      - dist/**/*.test.js
    expire_in: 1 day  # Auto-cleanup
```

### 流水线效率指标

**查看流水线耗时：**
```bash
glab ci list --per-page 10
```

**识别慢速作业：**
```bash
glab ci view --web  # Visual timeline of jobs
```

**优化依据：**
- 耗时最长的作业 → 并行化或优化
- 失败最多的作业 → 添加重试或修复不稳定问题
- 缓存命中率 → 调整缓存 key

---

## 特定环境配置

### 环境变量

**流水线级别：**

```yaml
variables:
  NODE_ENV: "production"
  API_BASE_URL: "https://api.example.com"
```

**作业级别：**

```yaml
deploy:staging:
  variables:
    API_BASE_URL: "https://staging-api.example.com"
  script:
    - deploy.sh
```

**受保护环境：**

在 GitLab CI/CD 变量中存储密钥（设置 → CI/CD → 变量）：
- 标记为"Protected" - 仅在受保护分支上可用
- 标记为"Masked" - 在作业日志中隐藏

```yaml
deploy:production:
  script:
    - deploy.sh
  environment:
    name: production
  variables:
    DATABASE_URL: $PRODUCTION_DB_URL  # Protected variable
```

### 动态环境

**Review Apps：**

```yaml
review:
  stage: deploy
  script:
    - deploy-review-app.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop:review
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

stop:review:
  stage: deploy
  script:
    - cleanup-review-app.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  when: manual
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```

### 环境保护

```yaml
deploy:production:
  environment:
    name: production
    deployment_tier: production  # Visible in deployment boards
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual  # Require approval
```

**在 GitLab 界面中设置（设置 → CI/CD → 环境）：**
- Protected - 仅允许 Maintainer 部署
- 部署审批 - 部署前需要手动批准

---

## 验证与测试

推送流水线配置前的检查：

```bash
# Validate syntax
glab ci lint

# Validate specific file
glab ci lint --path .gitlab-ci-custom.yml

# Dry run (simulate without executing)
glab ci run --dry-run
```

---

## 延伸阅读

- [GitLab CI/CD YAML 参考](https://docs.gitlab.com/ee/ci/yaml/)
- [GitLab CI/CD 示例](https://docs.gitlab.com/ee/ci/examples/)
- [GitLab CI/CD 最佳实践](https://docs.gitlab.com/ee/ci/pipelines/pipeline_efficiency.html)

**相关 glab-cli-skills：**
- [glab-ci](../SKILL.md) - 流水线管理的 CLI 命令
- [glab-job](../../glab-job/SKILL.md) - 作业级操作
- [glab-variable](../../glab-variable/SKILL.md) - 管理 CI/CD 变量
- [glab-schedule](../../glab-schedule/SKILL.md) - 定时流水线
