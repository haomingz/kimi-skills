---
name: glab-deploy-key
description: 管理 GitLab 项目的 SSH 部署密钥（deploy key），包括添加、列出和删除操作。适用于为 CI/CD 设置部署密钥、管理只读访问权限或配置部署认证。触发关键词：deploy key、SSH 密钥、部署密钥、只读访问。
---

# glab deploy-key

## 概述

```

  Manage deploy keys.                                                                                                   
         
  USAGE  
         
    glab deploy-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file] [--flags]  Add a deploy key to a GitLab project.
    delete <key-id>           Deletes a single deploy key specified by the ID.
    get <key-id>              Returns a single deploy key specified by the ID.
    list [--flags]            Get a list of deploy keys for the current project.
         
  FLAGS  
         
    -h --help                 Show help for this command.
    -R --repo                 Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab deploy-key --help
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
