---
name: glab-runner-controller
description: 管理 GitLab Runner 控制器和认证令牌。创建、更新、删除控制器；生成、轮换和撤销令牌。仅管理员可用的实验性功能，用于管理 Runner 控制器的生命周期。触发词：runner controller、控制器令牌、实验性 runner、管理员 runner。
---

# glab-runner-controller

管理 GitLab Runner 控制器及其认证令牌。

## ⚠️ 实验性功能

**状态：** 实验性（仅管理员可用）
- 此功能可能在没有事先通知的情况下被破坏或移除
- 使用风险自担
- 需要 GitLab 管理员权限
- 参阅：https://docs.gitlab.com/policy/development_stages_support/

## 功能说明

Runner 控制器用于管理基础设施中 GitLab Runner 的编排。此技能提供以下命令：
- 创建和配置 Runner 控制器
- 管理控制器生命周期（列出、更新、删除）
- 生成和轮换认证令牌
- 撤销已泄露的令牌

## 常见工作流

### 创建 Runner 控制器

```bash
# 使用默认设置创建
glab runner-controller create

# 创建时添加描述
glab runner-controller create --description "Production runners"

# 创建已启用的控制器
glab runner-controller create --description "Prod" --state enabled
```

**状态说明：**
- `disabled` - 控制器已创建但未激活
- `enabled` - 控制器已激活（默认）
- `dry_run` - 测试模式（不实际执行 Runner）

### 列出和查看控制器

```bash
# 列出所有控制器
glab runner-controller list

# 分页列出
glab runner-controller list --page 2 --per-page 50

# 以 JSON 格式输出
glab runner-controller list --output json
```

### 更新控制器

```bash
# 更新描述
glab runner-controller update 42 --description "Updated name"

# 更改状态
glab runner-controller update 42 --state disabled

# 同时更新描述和状态
glab runner-controller update 42 --description "Prod" --state enabled
```

### 删除控制器

```bash
# 删除（会有确认提示）
glab runner-controller delete 42

# 跳过确认直接删除
glab runner-controller delete 42 --force
```

## 令牌管理工作流

### 令牌生命周期

**创建 → 轮换 → 撤销** 是安全最佳实践中的典型令牌生命周期。

#### 1. 创建令牌

```bash
# 为控制器 42 创建令牌
glab runner-controller token create 42

# 创建时添加描述
glab runner-controller token create 42 --description "production"

# 以 JSON 格式输出（便于自动化）
glab runner-controller token create 42 --output json
```

**重要：** 令牌值创建后只显示一次，请立即保存。

#### 2. 列出令牌

```bash
# 列出控制器 42 的所有令牌
glab runner-controller token list 42

# 以 JSON 格式列出
glab runner-controller token list 42 --output json

# 分页查看
glab runner-controller token list 42 --page 1 --per-page 20
```

#### 3. 轮换令牌

轮换操作会生成新令牌并使旧令牌失效。

```bash
# 轮换令牌 1（带确认提示）
glab runner-controller token rotate 42 1

# 跳过确认直接轮换
glab runner-controller token rotate 42 1 --force

# 轮换并以 JSON 格式输出
glab runner-controller token rotate 42 1 --force --output json
```

**适用场景：**
- 定期轮换（满足安全策略要求）
- 令牌泄露后的响应
- 员工离职前的密钥轮换

#### 4. 撤销令牌

```bash
# 撤销令牌 1（带确认提示）
glab runner-controller token revoke 42 1

# 跳过确认直接撤销
glab runner-controller token revoke 42 1 --force
```

**适合撤销的场景：**
- 令牌被泄露或泄漏
- 控制器已退役
- 不再需要访问权限

### 令牌安全最佳实践

1. **定期轮换** - 设置定时轮换计划（如每 90 天）
2. **使用描述信息** - 记录令牌用途和负责人
3. **泄露后立即撤销**
4. **切勿将令牌提交**到版本控制系统
5. **使用 `--output json`** 进行自动化操作（安全地解析令牌值）

## 决策树：控制器状态选择

```
是否需要激活控制器？
├─ 是 → --state enabled
├─ 正在测试配置？ → --state dry_run
└─ 否（维护/设置阶段） → --state disabled
```

## 故障排查

**"Permission denied" 或 "403 Forbidden"：**
- Runner 控制器命令需要 GitLab 管理员权限
- 确认你以管理员用户身份登录
- 使用 `glab auth status` 检查当前用户

**"Runner controller not found"：**
- 使用 `glab runner-controller list` 确认控制器 ID
- 控制器可能已被删除
- 检查你是否连接到正确的 GitLab 实例

**令牌创建失败：**
- 确保控制器存在且已启用
- 确认管理员权限
- 检查 GitLab 实例版本（实验性功能可能需要较新版本）

**轮换后旧令牌仍然有效：**
- 令牌失效可能需要几秒钟才能生效
- 等待 10-30 秒后再次测试
- 检查控制器状态（已禁用的控制器不会强制执行令牌验证）

**无法删除控制器：**
- 检查控制器是否有活跃的 Runner
- 可能需要先退役 Runner
- 使用 `--force` 强制覆盖（⚠️ 破坏性操作）

**实验性功能不可用：**
- 检查 glab 版本：`glab version`（需要 v1.83.0+）
- 检查 GitLab 实例上是否启用了该功能标志
- 确认 GitLab 实例版本支持 Runner 控制器

**分页不起作用：**
- 默认每页 30 条
- 使用 `--per-page` 调整（最大值因实例而异）
- 使用 `--page` 翻页浏览结果

## v1.87.0 变更：Runner 范围子命令

从 v1.87.0 起，Runner 控制器支持 `runner` 范围，用于管理与控制器关联的 Runner。

### 列出范围内的 Runner

```bash
# 列出控制器 42 管理的所有 Runner
glab runner-controller runner list 42

# 以 JSON 格式输出
glab runner-controller runner list 42 --output json

# 分页查看
glab runner-controller runner list 42 --page 2 --per-page 50
```

### 将 Runner 添加到范围

```bash
# 将 Runner 添加到控制器 42 的范围
glab runner-controller runner create 42 --runner-id <runner-id>
```

### 从范围中移除 Runner

```bash
# 从控制器 42 的范围中移除 Runner（带确认提示）
glab runner-controller runner delete 42 <runner-id>

# 跳过确认直接移除
glab runner-controller runner delete 42 <runner-id> --force
```

**使用场景：** Runner 范围管理允许你明确定义哪些 Runner 由特定控制器编排，在多控制器环境中提供细粒度的 Runner 分配控制。

## 相关技能

**CI/CD 与 Runner：**
- `glab-ci` - 查看和管理 CI/CD 流水线与作业
- `glab-job` - 重试、取消、查看单个作业的日志
- `glab-runner` - 管理单个 Runner（列出、暂停、删除）——v1.87.0 新增

**仓库管理：**
- `glab-repo` - 管理仓库（Runner 控制器为实例级别）

**认证：**
- `glab-auth` - 登录和认证管理

## 命令参考

完整的命令语法和所有可用参数，请参阅：
- [references/commands.md](references/commands.md)
