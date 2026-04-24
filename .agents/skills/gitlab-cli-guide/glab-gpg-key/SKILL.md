---
name: glab-gpg-key
description: 管理用于提交签名的 GPG 密钥，包括添加、列出和删除操作。适用于设置提交签名、管理 GPG 密钥或验证已签名的提交。触发关键词：GPG 密钥、提交签名、已签名提交、验证提交。
---

# glab gpg-key

## 概述

```

  Manage GPG keys registered with your GitLab account.                                                                  
         
  USAGE  
         
    glab gpg-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file]   Add a GPG key to your GitLab account.
    delete <key-id>  Deletes a single GPG key specified by the ID.
    get <key-id>     Returns a single GPG key specified by the ID.
    list [--flags]   Get a list of GPG keys for the currently authenticated user.
         
  FLAGS  
         
    -h --help        Show help for this command.
    -R --repo        Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab gpg-key --help
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
