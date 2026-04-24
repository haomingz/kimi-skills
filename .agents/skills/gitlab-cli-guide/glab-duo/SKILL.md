---
name: glab-duo
description: 与 GitLab Duo AI 助手交互，获取代码建议和对话。适用于使用 AI 驱动的代码辅助、获取代码建议或与 GitLab Duo 对话。触发词：Duo、AI 助手、代码建议、AI 对话。
---

# glab duo

## 概览

```

  Work with GitLab Duo, our AI-native assistant for the command line.                                                   
                                                                                                                        
  GitLab Duo for the CLI integrates AI capabilities directly into your terminal                                         
  workflow. It helps you retrieve forgotten Git commands and offers guidance on                                         
  Git operations. You can accomplish specific tasks without switching contexts.                                         
                                                                                                                        
         
  USAGE  
         
    glab duo <command> prompt [command] [--flags]  
            
  COMMANDS  
            
    ask <prompt> [--flags]  Generate Git commands from natural language.
    help [command]          Show help information for duo commands and subcommands.
         
  FLAGS  
         
    -h --help               Show help for this command.
```

## 快速开始

```bash
glab duo --help
```

## v1.87.0 变更

### 二进制文件下载管理
从 v1.87.0 起，`glab duo` 包含了一个 CLI 二进制文件下载管理命令，用于安装和更新 GitLab Duo AI 二进制文件。

```bash
# 下载/更新 Duo CLI 二进制文件
glab duo update

# 检查当前 Duo 二进制文件版本
glab duo --version
```

**使用场景：** 升级 glab 后运行 `glab duo update`，确保 Duo AI 二进制文件与你的 CLI 版本匹配。如果升级 glab 后 `glab duo ask` 无法正常工作，通常运行此命令即可修复。

## v1.88.0 变更

### `glab duo help` 子命令

```bash
# 显示所有 duo 命令的帮助
glab duo help

# 显示特定子命令的帮助
glab duo help ask
```

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
