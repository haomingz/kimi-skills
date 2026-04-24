---
name: glab-release
description: 管理 GitLab 发布版本（release），包括创建、列出、查看、删除、下载和上传发布资产。适用于发布软件版本、管理发布说明、上传二进制文件/构建产物、下载发布文件或查看发布历史。触发关键词：release、版本、tag、发布版本、发布说明、下载发布。
---

# glab release

## 概述

```

  Manage GitLab releases.                                                                                               
         
  USAGE  
         
    glab release <command> [command] [--flags]  
            
  COMMANDS  
            
    create <tag> [<files>...] [--flags]  Create a new GitLab release, or update an existing one.
    delete <tag> [--flags]               Delete a GitLab release.
    download <tag> [--flags]             Download asset files from a GitLab release.
    list [--flags]                       List releases in a repository.
    upload <tag> [<files>...] [--flags]  Upload release asset files or links to a GitLab release.
    view <tag> [--flags]                 View information about a GitLab release.
         
  FLAGS  
         
    -h --help                            Show help for this command.
    -R --repo                            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab release --help
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
