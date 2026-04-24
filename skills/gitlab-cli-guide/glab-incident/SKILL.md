---
name: glab-incident
description: 管理 GitLab 事件（Incident），用于问题跟踪和事件管理。适用于创建事件、管理事件响应或将事件关联到 Issue。触发词：incident、事件管理、创建事件、事件响应。
---

# glab incident

## 概述

```

  Work with GitLab incidents.                                                                                           
         
  USAGE  
         
    glab incident [command] [--flags]  
            
  EXAMPLES  
            
    $ glab incident list               
            
  COMMANDS  
            
    close [<id> | <url>] [--flags]   Close an incident.
    list [--flags]                   List project incidents.
    note <incident-id> [--flags]     Comment on an incident in GitLab.
    reopen [<id> | <url>] [--flags]  Reopen a resolved incident.
    subscribe <id>                   Subscribe to an incident.
    unsubscribe <id>                 Unsubscribe from an incident.
    view <id> [--flags]              Display the title, body, and other information about an incident.
         
  FLAGS  
         
    -h --help                        Show help for this command.
    -R --repo                        Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab incident --help
```

## 子命令

完整的 `--help` 输出请参阅 [references/commands.md](references/commands.md)。
