---
name: glab-mr
description: 创建、查看、管理、批准和合并 GitLab merge request（合并请求）。适用于从分支/议题创建 MR、审查、批准、添加评论、解决讨论线程、本地检出、查看差异、变基、合并或管理状态等场景。触发关键词：merge request、MR、pull request、PR、审查、批准、合并、解决线程。
---

# glab mr

创建、查看和管理 GitLab merge request（合并请求）。

## 快速入门

```bash
# 从当前分支创建 MR
glab mr create --fill

# 列出我的 MR
glab mr list --assignee=@me

# 审查一个 MR
glab mr checkout 123
glab mr diff
glab mr approve

# 合并一个 MR
glab mr merge 123 --when-pipeline-succeeds --remove-source-branch
```

## 常用工作流

### 创建 MR

**从当前分支创建：**
```bash
glab mr create --fill --label bugfix --assignee @reviewer
```

**从议题创建：**
```bash
glab mr for 456  # 创建与议题 #456 关联的 MR
```

**创建草稿 MR：**
```bash
glab mr create --draft --title "WIP: Feature X"
```

### 审查工作流

1. **列出待审查的 MR：**
   ```bash
   glab mr list --reviewer=@me --state=opened
   ```

2. **检出并测试：**
   ```bash
   glab mr checkout 123
   npm test
   ```

3. **提交反馈：**
   ```bash
   glab mr note 123 -m "Looks good, one question about the cache logic"

   # 在添加备注的同时解决讨论线程（v1.88.0+）
   glab mr note 123 --resolve <discussion-id> -m "Fixed, addressed in latest commit."

   # 重新打开已解决的线程
   glab mr note 123 --unresolve <discussion-id>
   ```

4. **批准：**
   ```bash
   glab mr approve 123
   ```

**自动化审查工作流：**

对于重复性的审查任务，可以使用自动化脚本：
```bash
scripts/mr-review-workflow.sh 123
scripts/mr-review-workflow.sh 123 "pnpm test"
```

该脚本自动完成：检出 → 运行测试 → 发布结果 → 测试通过则批准。

### 合并策略

**流水线通过后自动合并：**
```bash
glab mr merge 123 --when-pipeline-succeeds --remove-source-branch
```

**压缩提交：**
```bash
glab mr merge 123 --squash
```

**合并前变基：**
```bash
glab mr rebase 123
glab mr merge 123
```

## 故障排除

**合并冲突：**
- 检出 MR：`glab mr checkout 123`
- 在编辑器中手动解决冲突
- 提交解决结果：`git add . && git commit`
- 推送：`git push`

**无法批准 MR：**
- 检查你是否是作者（大多数配置下不能自我批准）
- 验证权限：`glab mr approvers 123`
- 确保 MR 不处于草稿状态

**流水线未运行但又是必需的：**
- 检查分支中是否存在 `.gitlab-ci.yml`
- 验证项目是否启用了 CI/CD
- 手动触发：`glab ci run`

**"MR already exists" 错误：**
- 列出该分支的现有 MR：`glab mr list --source-branch <branch>`
- 如果已过时则关闭旧 MR：`glab mr close <id>`
- 或更新现有的：`glab mr update <id> --title "New title"`

## 相关技能

**处理议题：**
- 参见 `glab-issue` 了解议题的创建和管理
- 使用 `glab mr for <issue-id>` 创建与议题关联的 MR
- 脚本：`scripts/create-mr-from-issue.sh` 自动化分支创建 + MR 创建

**CI/CD 集成：**
- 参见 `glab-ci` 了解合并前的流水线状态
- 使用 `glab mr merge --when-pipeline-succeeds` 实现自动合并

**自动化：**
- 脚本：`scripts/mr-review-workflow.sh` 用于自动化审查 + 测试工作流

## 在 MR 差异上发布行内评论

### `glab api --field` 的问题

当 GitLab 拒绝位置数据时，`glab api --field position[new_line]=N` 会静默回退为**普通**（非行内）评论。以下情况会触发此问题：
- 全新文件（diff 中 `new_file: true`）
- 路径复杂或经过编码的文件
- 任何无法通过表单编码传递的嵌套 position 字段

不会报错 —— GitLab 只是丢弃 position 并创建一个普通讨论。除非你检查返回的 note 的 `position` 字段，否则无法知道是否失败。

### 解决方案：始终使用 JSON 请求体

通过 REST API 使用 `Content-Type: application/json` 请求体发布行内评论：

```python
import json, urllib.request, urllib.parse, subprocess

# Get token from glab config
token = subprocess.run(
    ["glab", "config", "get", "token", "--host", "gitlab.com"],
    capture_output=True, text=True
).stdout.strip()

project = urllib.parse.quote("mygroup/myproject", safe="")
mr_iid = 42

# Always fetch fresh SHAs — never use cached values
r = urllib.request.urlopen(urllib.request.Request(
    f"https://gitlab.com/api/v4/projects/{project}/merge_requests/{mr_iid}/versions",
    headers={"PRIVATE-TOKEN": token}
))
v = json.loads(r.read())[0]

payload = {
    "body": "Your comment here",
    "position": {
        "base_sha":  v["base_commit_sha"],
        "start_sha": v["start_commit_sha"],
        "head_sha":  v["head_commit_sha"],
        "position_type": "text",
        "new_path": "src/utils/helpers.ts",
        "new_line": 16,
        "old_path": "src/utils/helpers.ts",  # same as new_path
        "old_line": None                       # None = added line
    }
}

req = urllib.request.Request(
    f"https://gitlab.com/api/v4/projects/{project}/merge_requests/{mr_iid}/discussions",
    data=json.dumps(payload).encode(),
    headers={"PRIVATE-TOKEN": token, "Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    note = result["notes"][0]
    is_inline = note.get("position") is not None  # True = inline, False = fell back to general
    print("inline:", is_inline, "| disc_id:", result["id"])
```

### 查找正确的行号

行号必须指向 diff 中的**新增行**（`+` 前缀）—— 上下文行和删除行会导致 position 被拒绝：

```python
import re

def get_new_line_number(diff_text, keyword):
    """Find the new_file line number of the first added line containing keyword."""
    new_line = 0
    for line in diff_text.split("\n"):
        hunk = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if hunk:
            new_line = int(hunk.group(1)) - 1
            continue
        if line.startswith("-") or line.startswith("\\"):
            continue
        new_line += 1
        if line.startswith("+") and keyword in line:
            return new_line
    return None

# Usage
diffs = json.loads(...)  # from /merge_requests/{iid}/diffs
for d in diffs:
    if d["new_path"] == "src/utils/helpers.ts":
        line = get_new_line_number(d["diff"], "safeParse")
        print("line:", line)
```

### 可复用脚本

对于脚本化或自动化的 MR 审查，可使用内置的辅助工具：

```bash
# Single comment
python3 scripts/post-inline-comment.py \
  --project "mygroup/myproject" \
  --mr 42 \
  --file "src/utils/helpers.ts" \
  --line 16 \
  --body "This returns the wrapper object — use .data instead."

# Batch from JSON file
python3 scripts/post-inline-comment.py \
  --project "mygroup/myproject" \
  --mr 42 \
  --batch comments.json
```

批量文件格式：
```json
[
  { "file": "src/utils/helpers.ts", "line": 16, "body": "Comment 1" },
  { "file": "src/routes/+page.svelte", "line": 58, "body": "Comment 2" }
]
```

该脚本自动从 glab 配置读取 token，获取最新的 SHA，并报告每条评论是否成功作为行内评论发布。

---

### 按解决状态过滤讨论线程（v1.88.0+）

```bash
# Show only unresolved discussion threads on an MR
glab mr view 123 --unresolved

# Show only resolved threads
glab mr view 123 --resolved
```

适用于在合并前快速检查哪些审查线程仍需处理。

## v1.87.0 变更：新增 `glab mr list` 参数

以下参数在 v1.87.0 中添加到 `glab mr list`：

```bash
# Filter by author
glab mr list --author <username>

# Filter by source or target branch
glab mr list --source-branch feature/my-branch
glab mr list --target-branch main

# Filter by draft status
glab mr list --draft
glab mr list --not-draft

# Filter by label or exclude label
glab mr list --label bugfix
glab mr list --not-label wip

# Order and sort
glab mr list --order updated_at --sort desc
glab mr list --order merged_at --sort asc

# Date range filtering
glab mr list --created-after 2026-01-01
glab mr list --created-before 2026-03-01

# Search in title/description
glab mr list --search "login fix"

# Full flag reference (all available flags)
glab mr list \
  --assignee @me \
  --author vince \
  --reviewer @me \
  --label bugfix \
  --not-label wip \
  --source-branch feature/x \
  --target-branch main \
  --milestone "v2.0" \
  --draft \
  --state opened \
  --order updated_at \
  --sort desc \
  --search "auth" \
  --created-after 2026-01-01
```

## v1.88.0 变更

- `glab mr note`：新增 `--resolve <discussion-id>` 和 `--unresolve <discussion-id>` 参数，可在添加备注的同时解决/重新打开讨论线程
- `glab mr view`：新增 `--resolved` 和 `--unresolved` 参数，按解决状态过滤显示的讨论线程

## 命令参考

完整的命令文档和所有参数请参见 [references/commands.md](references/commands.md)。

**可用命令：**
- `approve` - 批准合并请求
- `checkout` - 本地检出 MR
- `close` - 关闭合并请求
- `create` - 创建新 MR
- `delete` - 删除合并请求
- `diff` - 查看 MR 中的变更
- `for` - 为议题创建 MR
- `list` - 列出合并请求
- `merge` - 合并/接受 MR
- `note` - 为 MR 添加评论
- `rebase` - 变基源分支
- `reopen` - 重新打开合并请求
- `revoke` - 撤销批准
- `subscribe` / `unsubscribe` - 管理通知
- `todo` - 添加待办事项
- `update` - 更新 MR 元数据
- `view` - 显示 MR 详情
