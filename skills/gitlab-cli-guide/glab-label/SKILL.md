---
name: glab-label
description: 管理 GitLab 标签（label），包括在项目级别和群组级别进行创建、列出、更新和删除操作。适用于使用标签组织 issue/MR、创建标签分类体系或管理标签颜色/描述。触发关键词：label、标签、issue 标签、创建标签、管理标签。
---

# glab label

管理项目级别和群组级别的标签。

## 快速开始

```bash
# 创建项目标签
glab label create --name bug --color "#FF0000"

# 创建群组标签
glab label create --group my-group --name priority::high --color "#FF6B00"

# 列出标签
glab label list

# 更新标签
glab label edit bug --color "#CC0000" --description "Software defects"

# 删除标签
glab label delete bug
```

## 决策：项目标签还是群组标签？

```
这个标签应该属于哪个层级？
├─ 在群组内的多个项目中使用
│  └─ 群组级别：glab label create --group <group> --name <label>
└─ 仅特定于某一个项目
   └─ 项目级别：glab label create --name <label>
```

**适合使用群组级别标签的场景：**
- 希望在群组内所有项目中保持统一的标签体系
- 管理组织范围的工作流
- 示例：`priority::high`、`type::bug`、`status::blocked`
- 减少重复，确保一致性

**适合使用项目级别标签的场景：**
- 标签仅与特定项目的工作流相关
- 团队希望自主管理自己的标签
- 示例：`needs-ux-review`、`deploy-to-staging`、`legacy-code`

## 常见工作流

### 创建标签分类体系

**设置优先级标签（群组级别）：**
```bash
glab label create --group engineering --name "priority::critical" --color "#FF0000"
glab label create --group engineering --name "priority::high" --color "#FF6B00"
glab label create --group engineering --name "priority::medium" --color "#FFA500"
glab label create --group engineering --name "priority::low" --color "#FFFF00"
```

**设置类型标签（群组级别）：**
```bash
glab label create --group engineering --name "type::bug" --color "#FF0000"
glab label create --group engineering --name "type::feature" --color "#00FF00"
glab label create --group engineering --name "type::maintenance" --color "#0000FF"
```

### 管理项目专属标签

**创建工作流标签：**
```bash
glab label create --name "needs-review" --color "#428BCA"
glab label create --name "ready-to-merge" --color "#5CB85C"
glab label create --name "blocked" --color "#D9534F"
```

### 批量操作

**列出所有标签以便审查：**
```bash
glab label list --per-page 100 > labels.txt
```

**删除已废弃的标签：**
```bash
glab label delete old-label-1
glab label delete old-label-2
```

## 相关技能

**使用标签：**
- 参见 `glab-issue` 了解如何为 issue 添加标签
- 参见 `glab-mr` 了解如何为合并请求添加标签
- 脚本：`scripts/batch-label-issues.sh` 用于批量打标签

## 命令参考

完整的命令文档和所有参数说明，请参见 [references/commands.md](references/commands.md)。

**可用命令：**
- `create` - 创建标签（项目或群组级别）
- `list` - 列出标签
- `edit` - 更新标签属性
- `delete` - 删除标签
- `get` - 查看单个标签详情
