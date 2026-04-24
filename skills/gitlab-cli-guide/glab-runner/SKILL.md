---
name: glab-runner
description: 管理 GitLab CI/CD Runner（运行器）——列出、分配、取消分配、暂停和删除项目、群组或实例级别的 Runner。适用于查看 Runner 状态、将 Runner 分配给项目、临时暂停 Runner 或移除已退役的 Runner。触发词：runner、glab runner、列出 runner、分配 runner、取消分配 runner、暂停 runner、删除 runner、CI runner。
---

# glab runner

通过命令行管理 GitLab CI/CD Runner（运行器）。

> **glab v1.87.0 新增**

## 快速入门

```bash
# 列出当前项目的 Runner
glab runner list

# 暂停一个 Runner
glab runner pause <runner-id>

# 删除一个 Runner
glab runner delete <runner-id>
```

## 常见工作流

### 列出 Runner

```bash
# 列出当前项目的所有 Runner
glab runner list

# 列出指定项目的 Runner
glab runner list --repo owner/project

# 列出所有 Runner（实例级别，仅管理员可用）
glab runner list --all

# 以 JSON 格式输出
glab runner list --output json

# 分页查看
glab runner list --page 2 --per-page 50
```

**JSON 输出解析示例：**
```bash
# 查找所有已暂停的 Runner
glab runner list --output json | python3 -c "
import sys, json
runners = json.load(sys.stdin)
paused = [r for r in runners if r.get('paused')]
for r in paused:
    print(f\"{r['id']}: {r.get('description','(no description)')} — {r.get('status')}\")
"
```

### 暂停 Runner

暂停 Runner 可以阻止它接收新作业，但不会将其移除。

```bash
# 暂停 Runner 123
glab runner pause 123

# 在指定项目上下文中暂停
glab runner pause 123 --repo owner/project
```

**适合暂停的场景：**
- 维护窗口期（更新、重启）
- 排查故障 Runner
- 临时减少 Runner 容量
- 退役前（先确认没有正在运行的作业）

### 删除 Runner

```bash
# 删除（会有确认提示）
glab runner delete 123

# 跳过确认直接删除
glab runner delete 123 --force

# 在指定项目上下文中删除
glab runner delete 123 --repo owner/project
```

**⚠️ 删除操作不可恢复。** 如果不确定，请先暂停。

## 决策树：暂停 vs 删除

```
是否需要永久移除该 Runner？
├─ 否 → 暂停它（可恢复）
└─ 是 → 它当前是否正在运行作业？
          ├─ 是 → 先暂停，等作业完成后再删除
          └─ 否 → 使用 --force 直接删除
```

## Runner 状态参考

| 状态 | 含义 |
|---|---|
| `online` | 已连接，准备接收作业 |
| `offline` | 未连接（检查 Runner 进程） |
| `paused` | 已连接但不接收新作业 |
| `stale` | 最近 3 个月无通信 |

## 故障排查

**"runner: command not found"：**
- 需要 glab v1.87.0 或更高版本。使用 `glab version` 检查。

**实例级别 Runner 出现 "Permission denied"：**
- 实例级别的 Runner 管理需要 GitLab 管理员权限。
- 项目 Runner 可以由项目维护者管理。

**Runner 无法暂停：**
- 使用 `glab runner list` 确认 Runner ID。
- 检查权限（至少需要项目的 Maintainer 角色）。

**暂停后 Runner 仍显示 "online"：**
- Runner 进程仍在主机上运行——只是不再接收新作业。
- 这是正常现象。如需完全停止，请通过 SSH 登录 Runner 主机并停止进程。

**无法删除 Runner：**
- Runner 可能是共享/群组级别的（需要更高权限）。
- 检查 Runner 是否被分配给多个项目；从一个项目移除可能需要项目级别删除而非实例级别删除。

### 为项目分配/取消分配 Runner（v1.88.0+）

将已有的 Runner 分配给项目，使其可以接收作业：

```bash
# 将 Runner 分配给当前项目
glab runner assign <runner-id>

# 分配给指定项目
glab runner assign <runner-id> --repo owner/project
```

从项目中移除 Runner（不会删除该 Runner）：

```bash
# 从当前项目取消分配
glab runner unassign <runner-id>

# 从指定项目取消分配
glab runner unassign <runner-id> --repo owner/project
```

**注意：** 分配/取消分配 Runner 至少需要项目的 Maintainer 角色。这与 `glab runner delete`（永久删除 Runner）不同。

## 相关技能

- `glab-runner-controller` — 管理 Runner 控制器和编排（仅管理员，实验性功能）
- `glab-ci` — 查看和管理 CI/CD 流水线与作业
- `glab-job` — 重试、取消、追踪单个作业的日志

## v1.88.0 变更

- 新增 `glab runner assign <runner-id>` — 将 Runner 分配给项目
- 新增 `glab runner unassign <runner-id>` — 从项目取消分配 Runner

## 命令参考

```
glab runner <command> [--flags]

Commands:
  list      Get a list of runners available to the user
  assign    Assign a runner to a project (v1.88.0+)
  unassign  Unassign a runner from a project (v1.88.0+)
  pause     Pause a runner
  delete    Delete a runner

Flags (list):
  --all          List all runners (instance-level, admin only)
  --output       Format output as: text, json
  --page         Page number
  --per-page     Number of items per page
  --repo         Select a repository
  -h, --help     Show help

Flags (pause / delete):
  --force        Skip confirmation prompt (delete only)
  --repo         Select a repository
  -h, --help     Show help
```
