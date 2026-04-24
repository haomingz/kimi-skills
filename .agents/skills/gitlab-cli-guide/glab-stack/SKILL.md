---
name: glab-stack
description: 管理堆叠式合并请求（Stacked MR），用于复杂的多部分变更。适用于创建有依赖关系的 MR、管理 MR 堆栈或处理多层变更。触发词：stack、堆叠式 MR、依赖 MR、MR 堆栈、堆叠变更。
---

# glab stack

## 概览

```

  Stacked diffs are a way of creating small changes that build upon each other to ultimately deliver a feature. This    
  kind of workflow can be used to accelerate development time by continuing to build upon your changes, while earlier   
  changes in the stack are reviewed and updated based on feedback.                                                      
                                                                                                                        
  This feature is experimental. It might be broken or removed without any prior notice.                                 
  Read more about what experimental features mean at                                                                    
  https://docs.gitlab.com/policy/development_stages_support/                                                            
                                                                                                                        
  Use experimental features at your own risk.                                                                           
                                                                                                                        
         
  USAGE  
         
    glab stack <command> [command] [--flags]  
            
  EXAMPLES  
            
    $ glab stack create cool-new-feature      
    $ glab stack sync                         
            
  COMMANDS  
            
    amend [--flags]      Save more changes to a stacked diff. (EXPERIMENTAL)
    create               Create a new stacked diff. (EXPERIMENTAL)
    first                Moves to the first diff in the stack. (EXPERIMENTAL)
    last                 Moves to the last diff in the stack. (EXPERIMENTAL)
    list                 Lists all entries in the stack. (EXPERIMENTAL)
    move                 Moves to any selected entry in the stack. (EXPERIMENTAL)
    next                 Moves to the next diff in the stack. (EXPERIMENTAL)
    prev                 Moves to the previous diff in the stack. (EXPERIMENTAL)
    reorder              Reorder a stack of merge requests. (EXPERIMENTAL)
    save [--flags]       Save your progress within a stacked diff. (EXPERIMENTAL)
    switch <stack-name>  Switch between stacks. (EXPERIMENTAL)
    sync                 Sync and submit progress on a stacked diff. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help            Show help for this command.
    -R --repo            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab stack --help
```

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
