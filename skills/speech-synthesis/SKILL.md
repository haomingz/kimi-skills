---
name: speech-synthesis
description: "将文本转换为高质量语音，支持多语言、多种音色，可调节语速、音调和音量，并生成字幕，输出MP3音频文件。当你需要朗读文本（比如文章、消息）、为视频或演示文稿生成配音，或直接提到“TTS”、“文字转语音”、“配音”、“朗读”时，就会使用这个技能。"
---

<!-- Localized from: edge-tts -->

# Edge-TTS 技能

## 概述

使用 node-edge-tts npm 包调用微软 Edge 神经网络语音服务，生成高质量的文字转语音音频。支持多种语言、多种音色、可调节语速/音调，以及字幕生成。

## 快速开始

当检测到触发词或用户发出 TTS 请求时：

1. **调用 tts 工具**（Clawdbot 内置），将文本转换为语音
2. 工具返回一个 MEDIA: 路径
3. Clawdbot 将音频发送到当前频道

```javascript
// 示例：使用内置 tts 工具
tts("要转换为语音的文本")
// 返回：MEDIA: /path/to/audio.mp3
```

## 触发检测

识别 "tts" 关键词作为 TTS 请求。该技能会自动过滤文本中的 TTS 相关关键词，避免将触发词本身也转换为语音。

## 高级自定义

### 使用 Node.js 脚本

如需更精细的控制，可直接使用内置脚本：

#### TTS 转换器
```bash
cd scripts
npm install
node tts-converter.js "要转换的文本" --voice en-US-AriaNeural --rate +10% --output output.mp3
```

**参数说明：**
- `--voice, -v`：音色名称（默认：en-US-AriaNeural）
- `--lang, -l`：语言代码（如 en-US、es-ES）
- `--format, -o`：输出格式（默认：audio-24khz-48kbitrate-mono-mp3）
- `--pitch`：音调调节（如 +10%、-20%、default）
- `--rate, -r`：语速调节（如 +10%、-20%、default）
- `--volume`：音量调节（如 +0%、-10%、default）
- `--save-subtitles, -s`：将字幕保存为 JSON 文件
- `--output, -f`：输出文件路径（默认：tts_output.mp3）
- `--proxy, -p`：代理地址（如 http://localhost:7890）
- `--timeout`：请求超时时间（毫秒，默认：10000）
- `--list-voices, -L`：列出可用音色

#### 配置管理器
```bash
cd scripts
npm install
node config-manager.js --set-voice en-US-AriaNeural

node config-manager.js --set-rate +10%

node config-manager.js --get

node config-manager.js --reset
```

### 音色选择

常用音色（使用 `--list-voices` 查看完整列表）：

**英语：**
- `en-US-MichelleNeural`（女声，自然风格，**默认**）
- `en-US-AriaNeural`（女声，自然风格）
- `en-US-GuyNeural`（男声，自然风格）
- `en-GB-SoniaNeural`（女声，英式英语）
- `en-GB-RyanNeural`（男声，英式英语）

**其他语言：**
- `es-ES-ElviraNeural`（西班牙语，西班牙）
- `fr-FR-DeniseNeural`（法语）
- `de-DE-KatjaNeural`（德语）
- `ja-JP-NanamiNeural`（日语）
- `zh-CN-XiaoxiaoNeural`（中文）
- `ar-SA-ZariyahNeural`（阿拉伯语）

### 语速指南

语速值使用百分比格式：
- `"default"`：正常语速
- `"-20%"` 至 `"-10%"`：较慢、清晰（适合教程、故事、无障碍场景）
- `"+10%"` 至 `"+20%"`：略快（适合摘要）
- `"+30%"` 至 `"+50%"`：较快（适合新闻、追求效率的场景）

### 输出格式

根据使用场景选择音频质量：
- `audio-24khz-48kbitrate-mono-mp3`：标准质量（语音消息、即时通讯）
- `audio-24khz-96kbitrate-mono-mp3`：高质量（演示文稿、内容创作）
- `audio-48khz-96kbitrate-stereo-mp3`：最高质量（专业音频、音乐）

## 资源说明

### scripts/tts-converter.js
主要的 TTS 转换脚本，基于 node-edge-tts。可生成自定义音色、语速、音量、音调和格式的音频文件，支持字幕生成和音色列表查询。

### scripts/config-manager.js
管理用户的 TTS 偏好设置（音色、语言、格式、音调、语速、音量），配置保存在 `~/.tts-config.json`。

### scripts/package.json
NPM 包配置文件，包含 node-edge-tts 依赖。

### references/node_edge_tts_guide.md
node-edge-tts npm 包的完整文档，包含：
- 按语言分类的完整音色列表
- 韵律参数（语速、音调、音量）
- 使用示例（命令行和模块两种方式）
- 字幕生成
- 输出格式
- 最佳实践和使用限制

### 音色试听
可在此网站试听不同音色并预览音频质量：https://tts.travisvn.com/

需要了解特定音色详情或高级功能时，请参阅上述资源。

## 安装

使用内置脚本前，请先安装依赖：

```bash
cd /home/user/clawd/skills/public/tts-skill/scripts
npm install
```

将安装以下依赖：
- `node-edge-tts` - TTS 库
- `commander` - 命令行参数解析

## 工作流程

1. **识别意图**：检查用户消息中是否包含 "tts" 触发词或关键词
2. **选择方式**：简单请求使用内置 `tts` 工具，需要自定义时使用 `scripts/tts-converter.js`
3. **生成音频**：将目标文本（消息、搜索结果、摘要等）转换为语音
4. **返回用户**：tts 工具返回 MEDIA: 路径，由 Clawdbot 完成音频分发

## 测试

### 基本测试
运行测试脚本验证 TTS 功能：
```bash
cd /home/user/clawd/skills/public/edge-tts/scripts
npm test
```
将生成一个测试音频文件，并验证 TTS 服务是否正常运行。

### 音色试听
在此网站试听不同音色并预览音频质量：https://tts.travisvn.com/

### 集成测试
使用内置 `tts` 工具进行快速测试：
```javascript
// 示例：使用默认设置测试 TTS
tts("This is a test of the TTS functionality.")
```

### 配置测试
验证配置持久化功能：
```bash
cd /home/user/clawd/skills/public/edge-tts/scripts
node config-manager.js --get
node config-manager.js --set-voice en-US-GuyNeural
node config-manager.js --get
```

## 故障排查

- **测试连通性**：运行 `npm test` 检查 TTS 服务是否可访问
- **检查音色可用性**：使用 `node tts-converter.js --list-voices` 查看可用音色
- **验证代理设置**：如使用代理，用 `node tts-converter.js "test" --proxy http://localhost:7890` 测试
- **检查音频输出**：测试应在 scripts 目录下生成 `test-output.mp3` 文件

## 注意事项

- node-edge-tts 使用微软 Edge 在线 TTS 服务（已更新，认证有效）
- 无需 API 密钥（免费服务）
- 默认输出 MP3 格式
- 需要网络连接
- 支持字幕生成（JSON 格式，包含词级别的时间戳）
- **临时文件处理**：默认情况下，音频文件保存在系统临时目录（Unix 系统为 `/tmp/edge-tts-temp/`，Windows 系统为 `C:\Users\<user>\AppData\Local\Temp\edge-tts-temp\`），文件名唯一（如 `tts_1234567890_abc123.mp3`）。文件不会自动删除——调用方（Clawdbot）应在使用后负责清理。如需永久保存，可使用 `--output` 参数指定自定义输出路径。
- **TTS 关键词过滤**：该技能会自动过滤文本中的 TTS 相关关键词（tts、TTS、text-to-speech），避免将触发词本身转换为语音
- 如有常用偏好设置，可使用 `config-manager.js` 设置默认值
- **默认音色**：`en-US-MichelleNeural`（女声，自然风格）
- 以 `Neural` 结尾的神经网络音色比标准音色质量更高
