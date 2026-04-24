---
name: glab-attestation
description: 管理 GitLab 软件attestation（证明），用于软件供应链安全，包括制品验证和来源追溯。适用于验证软件制品、管理 attestation 或进行供应链安全工作。触发词：attestation、验证制品、来源追溯、供应链安全。
---

# glab attestation

## 概览

```

  Manage software attestations. (EXPERIMENTAL)                                                                          
         
  USAGE  
         
    glab attestation <command> [command] [--flags]                                    
            
  EXAMPLES  
            
    # Verify attestation for the filename.txt file in the gitlab-org/gitlab project.  
    $ glab attestation verify gitlab-org/gitlab filename.txt                          
                                                                                      
    # Verify attestation for the filename.txt file in the project with ID 123.        
    $ glab attestation verify 123 filename.txt                                        
            
  COMMANDS  
            
    verify <project_id> <artifact_path>  Verify the provenance of a specific artifact or file. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help                            Show help for this command.
```

## 快速开始

```bash
glab attestation --help
```

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
