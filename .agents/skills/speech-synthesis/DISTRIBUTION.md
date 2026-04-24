# Edge-TTS 技能分发说明

## 概述

本文档提供 Edge-TTS 技能包的分发信息。

## 包内容

分发包包含以下内容：

- `SKILL.md` - 完整的技能文档
- `scripts/` - 用于 TTS 转换和配置的 Node.js 脚本
- `references/` - 补充文档和指南
- `dist/` - 分发产物和安装脚本

## 安装要求

### 系统要求
- Node.js（v14.0.0 或更高版本）
- npm（v6.0.0 或更高版本）
- TTS 服务需要网络连接
- 约 50MB 磁盘空间

### 依赖项
包已包含所有必需的依赖：
- `node-edge-tts` - 微软 Edge TTS 服务封装库
- `commander` - 命令行参数解析

## 安装说明

### 方法一：直接安装（推荐）
```bash
# 克隆或下载安装包
git clone https://github.com/clawdbot/edge-tts-skill.git
cd edge-tts-skill

# 安装依赖
npm install

# 测试安装
npm test
```

### 方法二：手动安装
```bash
# 创建安装目录
mkdir -p /home/user/clawd/skills/public/edge-tts
cd /home/user/clawd/skills/public/edge-tts

# 复制包内容
cp -r /path/to/edge-tts-package/* .

# 安装依赖
npm install

# 运行测试
npm test
```

## 使用方法

### 基本 TTS
```javascript
// 简单的 TTS 转换
tts("Hello, world!")
```

### 高级用法
```bash
# 使用自定义音色转换文本
node scripts/tts-converter.js "Hello, world!" --voice en-US-GuyNeural

# 列出可用音色
node scripts/tts-converter.js --list-voices

# 配置默认设置
node scripts/config-manager.js --set-voice en-US-AriaNeural
```

## 测试

### 包验证
```bash
# 运行包测试
npm test

# 验证音色列表
node scripts/tts-converter.js --list-voices

# 测试 TTS 转换
node scripts/tts-converter.js "This is a test." --output test.mp3
```

## 音色试听

可在此网站试听不同音色并预览音频质量：https://tts.travisvn.com/

## 支持

如遇问题需要帮助，请联系技能维护者或查阅官方文档。

## 许可协议

MIT 许可协议 - 详见 LICENSE 文件。
