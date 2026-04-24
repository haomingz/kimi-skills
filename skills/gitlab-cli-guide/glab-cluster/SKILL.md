---
name: glab-cluster
description: 管理 GitLab Kubernetes 集群和 Agent 集成。适用于连接集群、管理集群 Agent 或使用 Kubernetes 集成。触发词：cluster、Kubernetes、k8s、集群 Agent、连接集群。
---

# glab cluster

## 概览

```

  Manage GitLab Agents for Kubernetes and their clusters.                                                               
         
  USAGE  
         
    glab cluster <command> [command] [--flags]  
            
  COMMANDS  
            
    agent <command> [command] [--flags]  Manage GitLab Agents for Kubernetes.
    graph [--flags]                      Queries the Kubernetes object graph, using the GitLab Agent for Kubernetes. (EXPERIMENTAL)
         
  FLAGS  
         
    -h --help                            Show help for this command.
    -R --repo                            Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 快速开始

```bash
glab cluster --help
```

## 子命令

完整的 `--help` 输出详见 [references/commands.md](references/commands.md)。
