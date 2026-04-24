---
name: glab-alias
description: 创建、列出和删除 GitLab CLI 命令别名和快捷方式。适用于创建自定义 glab 命令、管理 CLI 快捷方式或查看现有别名。触发词：alias、快捷方式、自定义命令、CLI 别名。
---

# glab alias

## 概览

```

  Create, list, and delete aliases.                                                                                     
         
  USAGE  
         
    glab alias [command] [--flags]  
            
  COMMANDS  
            
    delete <alias name> [--flags]           Delete an alias.
    list [--flags]                          List the available aliases.
    set <alias name> '<command>' [--flags]  Set an alias for a longer command.
         
  FLAGS  
         
    -h --help                               Show help for this command.
```

## 快速开始

```bash
glab alias --help
```

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
