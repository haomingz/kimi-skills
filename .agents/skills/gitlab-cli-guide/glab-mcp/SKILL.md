---
name: glab-mcp
description: 使用 MCP（Model Context Protocol，模型上下文协议）服务器进行 AI 助手集成。将 GitLab 功能作为工具暴露给 AI 助手（如 Claude Code），用于与项目、issue、合并请求和流水线交互。适用于将 AI 助手与 GitLab 集成或使用 MCP 服务器。触发词：MCP、模型上下文协议、AI 助手集成、glab mcp serve。
---

# glab mcp

## 概览

```

  Manage Model Context Protocol server features for GitLab integration.                                                 
                                                                                                                        
  The MCP server exposes GitLab features as tools for use by                                                            
  AI assistants (like Claude Code) to interact with GitLab projects, issues,                                            
  merge requests, pipelines, and other resources.                                                                       
                                                                                                                        
  This feature is an experiment and is not ready for production use.                                                    
  It might be unstable or removed at any time.                                                                          
  For more information, see                                                                                             
  https://docs.gitlab.com/policy/development_stages_support/.                                                           
                                                                                                                        
         
  USAGE  
         
    glab mcp <command> [command] [--flags]  
            
  EXAMPLES  
            
    $ glab mcp serve                        
            
  COMMANDS  
            
    serve      Start a MCP server with stdio transport. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help  Show help for this command.
```

## 快速开始

```bash
glab mcp --help
```

## v1.86.0 变更

### 自动启用 JSON 输出
从 v1.86.0 起，`glab mcp serve` 运行时会自动启用 JSON 输出格式——无需手动添加参数。这提高了 AI 助手解析 MCP 服务器工具响应时的可靠性。

### 排除无注解的命令
缺少 MCP 注解的命令不再注册为 MCP 工具。这意味着只有明确支持的命令才会暴露给 AI 助手，从而减少干扰并提高可靠性。如果你期望的某个 GitLab 操作未作为 MCP 工具提供，可能是因为当前版本中该命令缺少 MCP 注解。

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
