---
name: glab-variable
description: 管理项目和群组级别的 CI/CD 变量，包括创建、更新、列出和删除操作。适用于设置流水线环境变量、管理密钥或配置 CI/CD 变量。触发词：variable、CI 变量、环境变量、密钥、CI/CD 配置。
---

# glab variable

## 概述

```

  Manage variables for a GitLab project or group.                                                                       
         
  USAGE  
         
    glab variable [command] [--flags]  
            
  COMMANDS  
            
    delete <key> [--flags]          Delete a variable for a project or group.
    export [--flags]                Export variables from a project or group.
    get <key> [--flags]             Get a variable for a project or group.
    list [--flags]                  List variables for a project or group.
    set <key> <value> [--flags]     Create a new variable for a project or group.
    update <key> <value> [--flags]  Update an existing variable for a project or group.
         
  FLAGS  
         
    -h --help                       Show help for this command.
    -R --repo                       Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab variable --help
```

## 子命令

完整的 `--help` 输出请参阅 [references/commands.md](references/commands.md)。
