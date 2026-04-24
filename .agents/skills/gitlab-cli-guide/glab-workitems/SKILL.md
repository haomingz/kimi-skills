---
name: glab-workitems
description: 列出和管理 GitLab 工作项（任务、OKR、关键结果、史诗）。适用于使用标准 Issue 之外的 GitLab 工作项类型。触发词：work items、任务、OKR、关键结果、史诗列表、工作项列表。
---

# glab workitems

列出和管理 GitLab 工作项——GitLab 中新一代的工作跟踪格式，支持任务（Task）、OKR、关键结果（Key Result）、史诗（Epic）等类型。

> **glab v1.87.0 新增**

## 什么是工作项？

工作项是 GitLab 的统一工作跟踪模型。它们在传统 Issue 的基础上扩展，支持：
- **任务（Task）** — Issue 内的子任务
- **OKR** — 目标与关键结果
- **关键结果（Key Result）** — 与 OKR 关联的可衡量成果
- **史诗（Epic，新一代）** — 跨里程碑的大型工作单元
- **事件（Incident）** — 关联到事件管理

## 快速入门

```bash
# 列出当前项目的工作项
glab workitems list

# 列出指定项目的工作项
glab workitems list --repo owner/project

# 以 JSON 格式输出
glab workitems list --output json
```

## 常见工作流

### 列出工作项

```bash
# 所有工作项（默认：打开状态）
glab workitems list

# 按类型筛选
glab workitems list --type Task
glab workitems list --type OKR
glab workitems list --type KeyResult
glab workitems list --type Epic

# 按状态筛选
glab workitems list --state opened
glab workitems list --state closed

# 以 JSON 格式输出（便于脚本处理）
glab workitems list --output json | python3 -c "
import sys, json
items = json.load(sys.stdin)
for item in items:
    print(f\"{item['iid']}: {item['title']} [{item['type']}]\")
"
```

### 指定仓库或群组

```bash
# 指定仓库
glab workitems list --repo mygroup/myproject

# 群组级别的工作项
glab workitems list --group mygroup
```

## 工作项 vs Issue

| 功能 | Issue | 工作项 |
|---|---|---|
| 标准缺陷/功能跟踪 | ✅ | ✅ |
| 任务（子任务） | ❌ | ✅ |
| OKR / 关键结果 | ❌ | ✅ |
| 新一代史诗 | ❌ | ✅ |
| CLI 支持 | 完整 | `list`（v1.87.0） |

标准 Issue 工作流请使用 `glab issue`。处理任务、OKR 或新一代史诗时请使用 `glab workitems`。

## 故障排查

**"workitems: command not found"：**
- 需要 glab v1.87.0 或更高版本。使用 `glab version` 检查。

**预期有结果但返回为空：**
- 工作项与 Issue 是不同的类型。以 Issue 方式创建的条目不会出现在这里，除非已被转换。
- 在 GitLab 界面中查看项目的"计划 > 工作项"侧边栏。

**类型筛选无结果：**
- 并非所有 GitLab 实例都启用了全部工作项类型。GitLab SaaS 比私有部署实例支持更多类型。

## 相关技能

- `glab-issue` — 标准 Issue 管理
- `glab-milestone` — 里程碑（常与 OKR 配合使用）
- `glab-iteration` — 迭代/冲刺管理
- `glab-incident` — 事件管理（一种工作项类型）

## 命令参考

```
glab workitems list [--flags]

Flags:
  --group        Select a group/subgroup
  --output       Format output as: text, json
  --page         Page number
  --per-page     Number of items per page
  --repo         Select a repository
  --state        Filter by state: opened, closed, all
  --type         Filter by work item type
  -h, --help     Show help
```
