---
name: glab-token
description: 管理 GitLab 个人访问令牌和项目访问令牌。适用于创建令牌、撤销访问权限或管理 API 认证。触发关键词：token、访问令牌、PAT、个人访问令牌、API 令牌。
---

# glab token

## 概述

```

  Manage personal, project, or group tokens                                                                             
         
  USAGE  
         
    glab token [command] [--flags]  
            
  COMMANDS  
            
    create <name> [--flags]                 Creates user, group, or project access tokens.
    list [--flags]                          List user, group, or project access tokens.
    revoke <token-name|token-id> [--flags]  Revoke user, group or project access tokens
    rotate <token-name|token-id> [--flags]  Rotate user, group, or project access tokens
         
  FLAGS  
         
    -h --help                               Show help for this command.
    -R --repo                               Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab token --help
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
