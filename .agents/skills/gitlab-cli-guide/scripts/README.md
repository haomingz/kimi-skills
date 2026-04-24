# GitLab CLI 脚本

常用 GitLab CLI 工作流的自动化脚本。

## 可用脚本

### `mr-review-workflow.sh`

自动化 MR 审查：检出 → 运行测试 → 通过则批准。

```bash
./scripts/mr-review-workflow.sh <MR_ID> [test_command]

# 示例
./scripts/mr-review-workflow.sh 123
./scripts/mr-review-workflow.sh 123 "pnpm test"
./scripts/mr-review-workflow.sh 123 "cargo test"
```

**功能说明：**
1. 本地检出 MR
2. 运行测试命令（默认：`npm test`）
3. 测试通过：添加批准评论 + 批准 MR
4. 测试失败：添加包含详细信息的失败评论

### `create-mr-from-issue.sh`

从 Issue 创建分支并正确命名。

```bash
./scripts/create-mr-from-issue.sh <ISSUE_ID> [--create-mr]

# 示例
./scripts/create-mr-from-issue.sh 456
./scripts/create-mr-from-issue.sh 456 --create-mr  # 同时创建草稿 MR
```

**功能说明：**
1. 获取 Issue 标题
2. 创建名为 `<issue-id>-<slugified-title>` 的分支
3. 可选地创建关联 Issue 的草稿 MR

### `ci-debug.sh`

通过显示失败任务日志来调试 CI 失败。

```bash
./scripts/ci-debug.sh <PIPELINE_ID>

# 示例
./scripts/ci-debug.sh 987654
```

**功能说明：**
1. 列出流水线中所有失败的任务
2. 显示每个失败任务日志的最后 50 行
3. 提供调试的后续步骤建议

### `add-inline-comment.sh`

在 MR diff 的特定行号处发布行内代码审查评论。

```bash
./scripts/add-inline-comment.sh <repo> <mr_iid> <file_path> <line_number> <comment_text>

# 示例
./scripts/add-inline-comment.sh owner/repo 42 "src/main.js" 100 "Bug: Add null check"
./scripts/add-inline-comment.sh owner/repo 42 "lib/util.py" 25 "**Performance**: Use dict comprehension"
```

**功能说明：**
1. 获取 MR 元数据（项目 ID、提交 SHA）
2. 在精确的 文件:行号 位置发布行内评论
3. 评论直接显示在 GitLab 界面的 diff 中
4. 返回评论的 URL

**文档：** 详细用法和集成示例请参见 `scripts/README-inline-comments.md`。

### `batch-label-issues.sh`

批量为多个 Issue 添加标签。

```bash
./scripts/batch-label-issues.sh <label> <issue_id1> [issue_id2] ...

# 示例
./scripts/batch-label-issues.sh bug 100 101 102
./scripts/batch-label-issues.sh "priority::high" 200 201
```

**功能说明：**
1. 将指定标签应用到所有列出的 Issue
2. 显示每个 Issue 的处理进度
3. 报告成功/失败汇总

### `sync-fork.sh`

将 Fork 与上游仓库同步。

```bash
./scripts/sync-fork.sh [branch] [upstream_remote]

# 示例
./scripts/sync-fork.sh                    # 将 main 与上游同步
./scripts/sync-fork.sh develop            # 将 develop 与上游同步
./scripts/sync-fork.sh main my-upstream   # 自定义上游远程名称
```

**功能说明：**
1. 从上游远程仓库拉取
2. 将上游更改合并到本地分支
3. 推送到 Fork 的 origin

## 使用技巧

**全局可用脚本：**
```bash
# 添加到 PATH
export PATH="$PATH:/path/to/gitlab-cli-skills/scripts"

# 或创建别名
alias mr-review="/path/to/gitlab-cli-skills/scripts/mr-review-workflow.sh"
alias ci-debug="/path/to/gitlab-cli-skills/scripts/ci-debug.sh"
```

**配合 OpenClaw 使用：**

代理可以直接执行这些脚本：
```
"运行 MR 123 的审查工作流"
"调试失败的 CI 流水线 456789"
"为 Issue 789 创建分支和草稿 MR"
```

## 前置条件

- 已安装并认证 `glab` CLI
- `git`（用于分支/Fork 操作）
- 测试框架（用于 `mr-review-workflow.sh`，如 npm、pnpm、cargo 等）

## Token 效率

这些脚本专为 OpenClaw 的渐进式披露模式设计：
- 脚本执行时无需加载到上下文中
- 仅脚本输出消耗 Token
- 确定性行为优于 AI 生成的代码
- 可跨多个任务复用
