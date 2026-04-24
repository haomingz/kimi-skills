---
name: glab-milestone
description: 管理项目里程碑（milestone），包括创建、列出、更新、查看和关闭操作。适用于规划发布版本、跟踪里程碑进度或按里程碑组织 issue/MR。触发关键词：milestone、里程碑、发布规划、里程碑进度、版本里程碑。
---

# glab milestone

## 概述

```

  Manage group or project milestones.                                                                                   
         
  USAGE  
         
    glab milestone <command> [command] [--flags]  
            
  COMMANDS  
            
    create [--flags]  Create a group or project milestone.
    delete [--flags]  Delete a group or project milestone.
    edit [--flags]    Edit a group or project milestone.
    get [--flags]     Get a milestones via an ID for a project or group.
    list [--flags]    Get a list of milestones for a project or group.
         
  FLAGS  
         
    -h --help         Show help for this command.
    -R --repo         Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab milestone --help
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
