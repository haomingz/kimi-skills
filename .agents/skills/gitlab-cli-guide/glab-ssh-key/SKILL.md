---
name: glab-ssh-key
description: 管理 GitLab 账户的 SSH 密钥，包括添加、列出和删除操作。适用于设置 SSH 认证、管理 SSH 密钥或配置 Git 通过 SSH 连接。触发关键词：SSH 密钥、添加 SSH 密钥、SSH 认证、Git SSH。
---

# glab ssh-key

## 概述

```

  Manage SSH keys registered with your GitLab account.                                                                  
         
  USAGE  
         
    glab ssh-key <command> [command] [--flags]  
            
  COMMANDS  
            
    add [key-file] [--flags]   Add an SSH key to your GitLab account.
    delete <key-id> [--flags]  Deletes a single SSH key specified by the ID.
    get <key-id> [--flags]     Returns a single SSH key specified by the ID.
    list [--flags]             Get a list of SSH keys for the currently authenticated user.
         
  FLAGS  
         
    -h --help                  Show help for this command.
    -R --repo                  Select another repository. Can use either `OWNER/REPO` or `GROUP/NAMESPACE/REPO` format. Also accepts full URL or Git URL.
```

## 安全警告：仅上传公钥

**务必确认你上传的是公钥（public key），而不是私钥（private key）。**

- 公钥：`~/.ssh/id_rsa.pub`、`~/.ssh/id_ed25519.pub`（`.pub` 扩展名）
- 私钥：`~/.ssh/id_rsa`、`~/.ssh/id_ed25519`（没有扩展名 -- 绝对不要上传这些文件）

将私钥上传到 GitLab 会暴露你的凭证。在运行 `glab ssh-key add` 前请仔细检查文件名。

```bash
# 正确 -- 公钥
glab ssh-key add ~/.ssh/id_ed25519.pub --title "My Laptop"

# 错误 -- 绝对不要这样做 -- 这是私钥
# glab ssh-key add ~/.ssh/id_ed25519 --title "My Laptop"
```

**上传前，请验证你的密钥是否为公钥：**
```bash
# 输出应以 'ssh-rsa'、'ssh-ed25519'、'ecdsa-sha2-*' 等开头
head -c 20 ~/.ssh/id_ed25519.pub
```

## 快速开始

```bash
glab ssh-key --help
```

## 子命令

完整的 `--help` 输出请参见 [references/commands.md](references/commands.md)。
