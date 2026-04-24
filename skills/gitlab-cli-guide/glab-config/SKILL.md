---
name: glab-config
description: 管理 glab CLI 配置设置，包括默认值、偏好设置和按主机的配置。适用于配置 glab 行为、设置默认值或查看当前配置。触发关键词：config、configuration、设置、glab 设置、设置默认值。
---

# glab config

## 概述

```

  Manage key/value strings.                                                                                             
                                                                                                                        
  Current respected settings:                                                                                           
                                                                                                                        
  - browser: If unset, uses the default browser. Override with environment variable $BROWSER.                           
  - check_update: If true, notifies of new versions of glab. Defaults to true. Override with environment variable       
  $GLAB_CHECK_UPDATE.                                                                                                   
  - display_hyperlinks: If true, and using a TTY, outputs hyperlinks for issues and merge request lists. Defaults to    
  false.                                                                                                                
  - editor: If unset, uses the default editor. Override with environment variable $EDITOR.                              
  - glab_pager: Your desired pager command to use, such as 'less -R'.                                                   
  - glamour_style: Your desired Markdown renderer style. Options are dark, light, notty. Custom styles are available    
  using [glamour](https://github.com/charmbracelet/glamour#styles).                                                     
  - host: If unset, defaults to `https://gitlab.com`.                                                                   
  - token: Your GitLab access token. Defaults to environment variables.                                                 
  - visual: Takes precedence over 'editor'. If unset, uses the default editor. Override with environment variable       
  $VISUAL.                                                                                                              
                                                                                                                        
         
  USAGE  
         
    glab config [command] [--flags]  
            
  COMMANDS  
            
    edit [--flags]               Opens the glab configuration file.
    get <key> [--flags]          Prints the value of a given configuration key.
    set <key> <value> [--flags]  Updates configuration with the value of a given key.
         
  FLAGS  
         
    -g --global                  Use global config file.
    -h --help                    Show help for this command.
```

## 快速开始

```bash
glab config --help
```

## v1.86.0 变更

### 按主机配置 HTTPS 代理
从 v1.86.0 起，你可以按主机配置 HTTPS 代理。当不同的 GitLab 实例（例如 gitlab.com 与自托管实例）需要不同的代理设置时，这个功能非常有用。

```bash
# 为特定主机设置 HTTPS 代理
glab config set https_proxy "http://proxy.example.com:8080" --host gitlab.mycompany.com

# 全局设置（适用于所有未单独配置的主机）
glab config set https_proxy "http://proxy.example.com:8080" --global

# 验证
glab config get https_proxy --host gitlab.mycompany.com
```

**优先级：** 按主机配置会覆盖全局配置。全局配置会覆盖 `HTTPS_PROXY` / `https_proxy` 环境变量。

## 常用设置

```bash
# 查看当前配置
glab config get --global

# 设置默认编辑器
glab config set editor vim --global

# 设置分页器
glab config set glab_pager "less -R" --global

# 禁用更新检查
glab config set check_update false --global

# 设置默认主机
glab config set host https://gitlab.mycompany.com --global
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
