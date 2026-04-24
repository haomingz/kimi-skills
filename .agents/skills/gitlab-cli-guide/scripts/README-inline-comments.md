# GitLab 行内评论自动化

## 概述

`add-inline-comment.sh` 脚本可以在 GitLab 合并请求的特定文件行处发布行内代码审查评论。这比普通的 MR 评论更有效，因为开发者可以直接在上下文中看到反馈，无需在代码中来回查找。

## 为什么使用行内评论？

**问题：** GitLab 原生的 `glab mr note` 命令只能创建通用 MR 评论。在审查代码时，你通常想对特定行进行评论，但 glab 没有内置的相关命令。

**解决方案：** 本脚本使用 GitLab Discussions API 来发布带有精确位置数据（文件路径、行号和提交 SHA）的行内评论。

**优势：**
- 📍 **上下文化反馈** - 评论出现在精确的代码行位置
- ⏱️ **节省时间** - 无需在 GitLab 界面中手动点击
- 🤖 **支持自动化** - 可集成到审查工作流中
- ✅ **更好的体验** - 开发者在上下文中即可看到反馈

## 安装

```bash
# 脚本已包含在 gitlab-cli-skills 仓库中
cd /path/to/gitlab-cli-skills/scripts
chmod +x add-inline-comment.sh

# 可选：添加到 PATH 以便全局使用
ln -s $(pwd)/add-inline-comment.sh ~/.local/bin/add-inline-comment
```

## 前置条件

- **glab CLI** - 已配置并认证（`glab auth login`）
- **jq** - 用于 JSON 解析（`apt install jq` 或 `brew install jq`）
- **curl** - 用于 API 调用（通常已预装）

## 用法

```bash
add-inline-comment.sh <repo> <mr_iid> <file_path> <line_number> <comment_text>
```

### 参数说明

| 参数 | 描述 | 示例 |
|-----------|-------------|---------|
| `repo` | 仓库路径 | `owner/repo` |
| `mr_iid` | 合并请求 IID（数字） | `42` |
| `file_path` | 相对于仓库根目录的文件路径 | `src/main.js` |
| `line_number` | 新版本中的行号 | `100` |
| `comment_text` | 评论内容（支持 markdown） | `Bug: Add null check` |

### 示例

**简单评论：**
```bash
add-inline-comment.sh \
  "owner/repo" \
  "42" \
  "src/components/Button.tsx" \
  "25" \
  "Consider using a more descriptive variable name here"
```

**带 markdown 的 Bug 报告：**
```bash
add-inline-comment.sh \
  "owner/repo" \
  "42" \
  "src/utils/validator.js" \
  "10" \
  "**Bug**: This regex doesn't handle edge case when input is \`null\`. Add: \`if (!input) return false;\`"
```

**多条评论（批量审查）：**
```bash
#!/bin/bash
REPO="owner/repo"
MR_IID="42"

add-inline-comment.sh "$REPO" "$MR_IID" "src/api.js" 15 "Add error handling"
add-inline-comment.sh "$REPO" "$MR_IID" "src/api.js" 22 "Use async/await instead of .then()"
add-inline-comment.sh "$REPO" "$MR_IID" "src/types.ts" 8 "Missing JSDoc comment"
```

## 工作原理

1. **提取 GitLab 令牌** —— 从 `~/.config/glab-cli/config.yml` 读取
2. **获取 MR 元数据** —— 通过 `glab api` 获取：
   - 项目 ID
   - Base SHA（目标分支提交）
   - Head SHA（源分支提交）
   - Start SHA（合并基准提交）
3. **构建 JSON 请求体** —— 包含位置数据：
   ```json
   {
     "body": "Comment text",
     "position": {
       "base_sha": "abc123...",
       "head_sha": "def456...",
       "start_sha": "abc123...",
       "position_type": "text",
       "new_path": "src/file.js",
       "new_line": 42
     }
   }
   ```
4. **发送到 GitLab API** —— 通过 `curl`（`glab api` 不支持嵌套 JSON）
5. **验证响应** —— 检查 note 类型是 `DiffNote`（行内）而非 `DiscussionNote`（通用）

## 输出

### 成功输出

```
✅ Success!
Discussion ID: abc123...
Note ID: 3106970438
Note Type: DiffNote
Inline: true

✅ Inline comment posted successfully at src/main.js:42
URL: https://gitlab.com/owner/repo/-/merge_requests/42#note_3106970438
```

脚本还会输出完整的 JSON 响应供程序化使用。

### 错误输出

```
❌ Error: HTTP 400
{
  "message": "400 Bad request - Position is invalid"
}
```

常见错误：
- **400 Bad Request** - 行号在 diff 中不存在
- **401 Unauthorized** - 令牌无效或已过期
- **404 Not Found** - MR 或仓库不存在

## 故障排除

### "Could not extract GitLab token"

**原因：** glab CLI 未认证或配置文件不存在。

**修复方法：**
```bash
glab auth login
glab auth status  # 验证认证状态
```

### "Position is invalid"

**原因：** 行号在文件 diff 中不存在。

**修复方法：**
- 确认行号存在于文件的**新版本**中
- 检查文件是否确实在此 MR 中被修改
- 使用 `glab mr diff <iid>` 查看 diff 中包含哪些行

### 评论显示为通用评论而非行内评论

**原因：** 如果脚本执行成功，这种情况不应出现，但如果确实发生：
- 文件路径可能不正确（必须是相对于仓库根目录的路径）
- 行号可能超出了 diff 范围

**调试：**
```bash
# 检查 diff 以查看可用的行
glab mr diff 42 --repo owner/repo | grep -A5 -B5 "src/file.js"
```

## 与代码审查工作流的集成

### 示例：自动化审查脚本

```bash
#!/bin/bash
# review-mr.sh - 自动化代码审查辅助工具

REPO="$1"
MR_IID="$2"

# 获取 MR diff
DIFF=$(glab mr diff "$MR_IID" --repo "$REPO")

# 检查常见问题
if echo "$DIFF" | grep -q "console.log"; then
    # 查找 console.log 的行号
    LINE=$(echo "$DIFF" | grep -n "console.log" | head -1 | cut -d: -f1)
    FILE=$(echo "$DIFF" | grep -B20 "console.log" | grep "^+++" | head -1 | cut -d/ -f2-)
    
    add-inline-comment.sh "$REPO" "$MR_IID" "$FILE" "$LINE" \
        "⚠️ Remove console.log before merging"
fi

# 检查 TODO 注释
if echo "$DIFF" | grep -q "TODO"; then
    # ... 类似逻辑
fi
```

### 示例：从分析工具发起审查

```bash
#!/bin/bash
# 运行 ESLint 并为每个问题发布行内评论

REPO="owner/repo"
MR_IID="42"

# 运行 linter 并解析输出
eslint src/ --format json | jq -r '.[] | "\(.filePath):\(.messages[].line) \(.messages[].message)"' | \
while IFS=: read -r file line message; do
    # 移除绝对路径前缀
    rel_path="${file#/absolute/path/to/repo/}"
    
    add-inline-comment.sh "$REPO" "$MR_IID" "$rel_path" "$line" "ESLint: $message"
done
```

## 限制

1. **行必须存在于 diff 中** - 只能对 MR 中新增或修改的行添加评论
2. **文件路径必须精确** - 必须与相对于仓库根目录的路径完全匹配
3. **仅限新文件的行** - 行号指向文件的新版本（修改后）
4. **仅限 GitLab.com** - 脚本使用 `https://gitlab.com/api/v4/`（自托管实例需修改）

## API 参考

本脚本使用 [GitLab Discussions API](https://docs.gitlab.com/ee/api/discussions.html#create-a-new-thread-in-the-merge-request-diff)。

**端点：**
```
POST /projects/:id/merge_requests/:merge_request_iid/discussions
```

**关键字段：**
- `body` - 评论文本（支持 markdown）
- `position.base_sha` - 目标分支提交
- `position.head_sha` - 源分支提交
- `position.new_path` - 文件路径
- `position.new_line` - 行号

## 开发

### 测试

在个人仓库上测试后再用于正式 MR：

```bash
# 创建测试 MR
glab mr create --title "Test MR" --repo owner/test-repo

# 发布测试评论
./add-inline-comment.sh \
  "owner/test-repo" \
  "1" \
  "README.md" \
  "1" \
  "TEST: This is a test inline comment"

# 在 GitLab 界面中验证
# 完成后删除测试评论和 MR
```

### 贡献

欢迎改进！本脚本是 [gitlab-cli-skills](https://github.com/vince-winkintel/gitlab-cli-skills) 的一部分。

**改进方向：**
- 支持自托管 GitLab 实例（可配置 API URL）
- 批量模式（从文件或标准输入读取评论）
- 支持行范围（多行评论）
- 与现有的 `glab-mr` 审查工作流集成

## 相关技能

- **glab-mr** - 主要的 MR 管理技能
- **代码审查工作流** - 在 `glab-mr/SKILL.md` 中有文档说明
- **CI 自动化** - 可从 CI 流水线中触发

## 许可证

与 gitlab-cli-skills 相同：MIT 许可证

---

**版本：** 1.0.0 (2026-02-23)  
**测试环境：** GitLab.com，glab CLI v1.48.0
