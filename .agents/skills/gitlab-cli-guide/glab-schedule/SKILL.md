---
name: glab-schedule
description: 管理 CI/CD 流水线定时计划，包括创建、列出、更新、删除和运行定时流水线。适用于自动化流水线、设置定时任务或管理定时构建。触发词：schedule、定时流水线、cron、流水线计划、自动化构建。
---

# glab schedule

## 概述

```

  Work with GitLab CI/CD schedules.                                                                                     
         
  USAGE  
         
    glab schedule <command> [command] [--flags]  
            
  COMMANDS  
            
    create [--flags]       Schedule a new pipeline.
    delete <id> [--flags]  Delete the schedule with the specified ID.
    list [--flags]         Get the list of schedules.
    run <id>               Run the specified scheduled pipeline.
    update <id> [--flags]  Update a pipeline schedule.
         
  FLAGS  
         
    -h --help              Show help for this command.
    -R --repo              Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab schedule --help
```

## 子命令

完整的 `--help` 输出请参阅 [references/commands.md](references/commands.md)。
