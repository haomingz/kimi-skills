---
name: glab-opentofu
description: 在 GitLab 中管理 OpenTofu 状态。适用于管理 Terraform/OpenTofu 状态、配置状态后端或进行基础设施即代码（IaC）工作。触发词：OpenTofu、Terraform、状态管理、基础设施即代码、IaC。
---

# glab opentofu

## 概览

```

  Work with the OpenTofu or Terraform integration.                                                                      
         
  USAGE  
         
    glab opentofu <command> [command] [--flags]  
            
  COMMANDS  
            
    init <state> [--flags]               Initialize OpenTofu or Terraform.
    state <command> [command] [--flags]  Work with the OpenTofu or Terraform states.
         
  FLAGS  
         
    -h --help                            Show help for this command.
    -R --repo                            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab opentofu --help
```

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
