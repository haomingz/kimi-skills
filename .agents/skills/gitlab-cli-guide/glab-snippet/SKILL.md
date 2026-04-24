---
name: glab-snippet
description: 创建、查看、更新和管理 GitLab 代码片段（类似 Gist）。适用于分享代码片段、创建快速示例或管理可复用代码块。触发词：snippet、gist、代码片段、分享代码、创建代码片段。
---

# glab snippet

## 概述

```

  Create, view and manage snippets.                                                                                     
         
  USAGE  
         
    glab snippet <command> [command] [--flags]                                 
            
  EXAMPLES  
            
    $ glab snippet create --title "Title of the snippet" --filename "main.go"  
            
  COMMANDS  
            
    create  -t <title> <file1>                                        [<file2>...] [--flags]  Create a new snippet.
    glab snippet create  -t <title> -f <filename>  # reads from stdin                                              
         
  FLAGS  
         
    -h --help                                                                                 Show help for this command.
    -R --repo                                                                                 Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab snippet --help
```

## 子命令

完整的 `--help` 输出请参阅 [references/commands.md](references/commands.md)。
