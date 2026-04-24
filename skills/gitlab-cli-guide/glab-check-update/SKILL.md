---
name: glab-check-update
description: 检查 glab CLI 更新并查看最新版本信息。适用于检查 glab 是否为最新版本或查找可用更新。触发词：更新 glab、检查版本、glab 版本、CLI 更新。
---

# glab check-update

## 概览

```

  Checks for the latest version of glab available on GitLab.com.                                                        
                                                                                                                        
  When run explicitly, this command always checks for updates regardless of when the last check occurred.               
                                                                                                                        
  When run automatically after other glab commands, it checks for updates at most once every 24 hours.                  
                                                                                                                        
  To disable the automatic update check entirely, run 'glab config set check_update false'.                             
  To re-enable the automatic update check, run 'glab config set check_update true'.                                     
                                                                                                                        
         
  USAGE  
         
    glab check-update [--flags]  
         
  FLAGS  
         
    -h --help  Show help for this command.
```

## 快速开始

```bash
glab check-update --help
```

## 子命令

此命令没有子命令。
