---
name: glab-securefile
description: 管理 CI/CD 安全文件，包括上传、下载、列出和删除操作。适用于存储流水线敏感文件、管理证书或处理安全配置文件。触发词：secure file、CI 密钥、证书、安全配置。
---

# glab securefile

## 概述

```

  Store up to 100 files for secure use in CI/CD pipelines. Secure files are                                             
  stored outside of your project's repository, not in version control.                                                  
  It is safe to store sensitive information in these files. Both plain text                                             
  and binary files are supported, but they must be smaller than 5 MB.                                                   
                                                                                                                        
         
  USAGE  
         
    glab securefile <command> [command] [--flags]  
            
  COMMANDS  
            
    create <fileName> <inputFilePath>  Create a new project secure file.
    download <fileID> [--flags]        Download a secure file for a project.
    get <fileID>                       Get details of a project secure file. (GitLab 18.0 and later)
    list [--flags]                     List secure files for a project.
    remove <fileID> [--flags]          Remove a secure file.
         
  FLAGS  
         
    -h --help                          Show help for this command.
    -R --repo                          Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速入门

```bash
glab securefile --help
```

## 子命令

完整的 `--help` 输出请参阅 [references/commands.md](references/commands.md)。
