---
name: glab-issue
description: 创建、查看、更新和管理 GitLab 议题。适用于议题跟踪、缺陷报告、功能请求或任务管理等场景。操作包括创建议题、带过滤器列表、查看详情、添加评论/备注、更新标签/指派人/里程碑、关闭/重新打开以及看板管理。触发关键词：议题、缺陷、任务、工单、功能请求、列出议题、创建议题。
---

# glab issue

创建、查看、更新和管理 GitLab 议题（issue）。

## 快速入门

```bash
# Create an issue
glab issue create --title "Fix login bug" --label bug

# List open issues
glab issue list --state opened

# View issue details
glab issue view 123

# Add comment
glab issue note 123 -m "Working on this now"

# Close issue
glab issue close 123
```

## 常用工作流

### 缺陷报告工作流

1. **创建缺陷议题：**
   ```bash
   glab issue create \
     --title "Login fails with 500 error" \
     --label bug \
     --label priority::high \
     --assignee @dev-lead
   ```

2. **添加复现步骤：**
   ```bash
   glab issue note 456 -m "Steps to reproduce:
   1. Navigate to /login
   2. Enter valid credentials
   3. Click submit
   Expected: Dashboard loads
   Actual: 500 error"
   ```

### 议题分类

1. **列出未分类的议题：**
   ```bash
   glab issue list --label needs-triage --state opened
   ```

2. **更新标签和指派人：**
   ```bash
   glab issue update 789 \
     --label backend,priority::medium \
     --assignee @backend-team \
     --milestone "Sprint 23"
   ```

3. **移除分类标签：**
   ```bash
   glab issue update 789 --unlabel needs-triage
   ```

**批量打标签：**

对多个议题批量添加标签：
```bash
scripts/batch-label-issues.sh "priority::high" 100 101 102
scripts/batch-label-issues.sh bug 200 201 202 203
```

### Sprint 规划

**查看当前 Sprint 的议题：**
```bash
glab issue list --milestone "Sprint 23" --assignee @me
```

**添加到 Sprint：**
```bash
glab issue update 456 --milestone "Sprint 23"
```

**看板视图：**
```bash
glab issue board view
```

### 将议题关联到工作

**为议题创建 MR：**
```bash
glab mr for 456  # Creates MR that closes issue #456
```

**自动化工作流（创建分支 + 草稿 MR）：**
```bash
scripts/create-mr-from-issue.sh 456 --create-mr
```

该脚本自动完成：从议题标题创建分支 → 空提交 → 推送 → 创建草稿 MR。

**通过提交/MR 关闭议题：**
```bash
git commit -m "Fix login bug

Closes #456"
```

## 相关技能

**从议题创建 MR：**
- 参见 `glab-mr` 了解合并请求操作
- 使用 `glab mr for <issue-id>` 创建可关闭议题的 MR
- 脚本：`scripts/create-mr-from-issue.sh` 自动化分支创建 + 草稿 MR

**标签管理：**
- 参见 `glab-label` 了解标签的创建和管理
- 脚本：`scripts/batch-label-issues.sh` 用于批量打标签操作

**项目规划：**
- 参见 `glab-milestone` 了解版本规划
- 参见 `glab-iteration` 了解 Sprint/迭代管理

## 命令参考

完整的命令文档和所有参数请参见 [references/commands.md](references/commands.md)。

**可用命令：**
- `create` - 创建新议题
- `list` - 带过滤器列出议题
- `view` - 显示议题详情
- `note` - 为议题添加评论
- `update` - 更新标题、标签、指派人、里程碑
- `close` - 关闭议题
- `reopen` - 重新打开已关闭的议题
- `delete` - 删除议题
- `subscribe` / `unsubscribe` - 管理通知
- `board` - 使用议题看板
