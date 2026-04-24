# node-edge-tts 参考文档

node-edge-tts 是一个 Node.js 模块，利用微软 Edge 在线 TTS（文字转语音）服务。支持多种音色、语言和音频格式。

## 安装

```bash
npm install node-edge-tts
# 或
npx node-edge-tts -t "Hello world"
```

## 核心概念

### 音色

node-edge-tts 提供微软 Edge 的神经网络音色。音色名称遵循以下格式：
- `en-US-AriaNeural` - 英语（美国），女声
- `en-US-GuyNeural` - 英语（美国），男声
- `es-ES-ElviraNeural` - 西班牙语（西班牙），女声

格式：`{语言代码}-{地区代码}-{名称}{音色类型}`

### 输出格式

node-edge-tts 支持多种音频输出格式：
- `audio-24khz-48kbitrate-mono-mp3` - 24kHz，48kbps，单声道 MP3（默认）
- `audio-24khz-96kbitrate-mono-mp3` - 24kHz，96kbps，单声道 MP3（更高质量）
- `audio-48khz-96kbitrate-stereo-mp3` - 48kHz，96kbps，立体声 MP3（最高质量）

## 常用音色列表

### 英语
- `en-US-AriaNeural`（女声，自然风格，推荐）
- `en-US-GuyNeural`（男声，自然风格）
- `en-GB-SoniaNeural`（女声，英式英语）
- `en-GB-RyanNeural`（男声，英式英语）

### 西班牙语
- `es-ES-ElviraNeural`（女声，西班牙）
- `es-MX-DaliaNeural`（女声，墨西哥）

### 法语
- `fr-FR-DeniseNeural`（女声）
- `fr-FR-HenriNeural`（男声）

### 德语
- `de-DE-KatjaNeural`（女声）
- `de-DE-ConradNeural`（男声）

### 亚洲语言
- `ja-JP-NanamiNeural`（日语，女声）
- `zh-CN-XiaoxiaoNeural`（中文，女声）
- `ko-KR-SunHiNeural`（韩语，女声）

### 阿拉伯语
- `ar-SA-ZariyahNeural`（女声）
- `ar-SA-HamedNeural`（男声）

## 使用方式

### 命令行用法

```bash
# 基本用法
npx node-edge-tts -t "Hello world" -f output.mp3

# 指定音色和语言
npx node-edge-tts -t "Hello world" -v en-US-AriaNeural -l en-US -f output.mp3

# 调整音调和语速
npx node-edge-tts -t "Hello world" --rate "+10%" --pitch "-10%" -f output.mp3

# 生成字幕
npx node-edge-tts -t "Hello world" -f output.mp3 -s
```

### 模块用法

```javascript
const { EdgeTTS } = require('node-edge-tts');

async function generateSpeech(text, outputFile) {
  const tts = new EdgeTTS({
    voice: 'en-US-AriaNeural',
    lang: 'en-US',
    outputFormat: 'audio-24khz-48kbitrate-mono-mp3',
    pitch: 'default',
    rate: 'default',
    volume: 'default',
  });

  await tts.ttsPromise(text, outputFile);
}

generateSpeech('Hello world!', 'output.mp3');
```

### 带选项使用

```javascript
const { EdgeTTS } = require('node-edge-tts');

async function generateSpeech(text, outputFile) {
  const tts = new EdgeTTS({
    voice: 'en-US-AriaNeural',
    lang: 'en-US',
    outputFormat: 'audio-24khz-96kbitrate-mono-mp3',
    saveSubtitles: true,
    proxy: 'http://localhost:7890',
    timeout: 10000,
    pitch: '+10%',
    rate: '+20%',
    volume: '-10%',
  });

  await tts.ttsPromise(text, outputFile);
  // 字幕保存到 output.json
}
```

## 韵律参数

### 语速（Rate）
通过百分比调整语速：
- `"default"` - 正常语速（默认）
- `"+10%"` - 加速 10%
- `"-20%"` - 减速 20%
- `"+50%"` - 加速 50%

### 音调（Pitch）
通过百分比调整音调：
- `"default"` - 正常音调（默认）
- `"+10%"` - 升高音调
- `"-10%"` - 降低音调

### 音量（Volume）
通过百分比调整音量：
- `"default"` - 正常音量（默认）
- `"+10%"` - 增大 10%
- `"-20%"` - 减小 20%

## 字幕

node-edge-tts 支持生成 JSON 格式的字幕，包含词级别的时间戳：

```bash
npx node-edge-tts -t "Hello world" -f output.mp3 -s
```

生成文件：
- `output.mp3` - 音频文件
- `output.json` - 字幕文件（含时间数据）

**字幕格式：**
```json
[
  {
    "part": "Hello ",
    "start": 100,
    "end": 500
  },
  {
    "part": "world",
    "start": 500,
    "end": 900
  }
]
```

- `part`：单词或短语
- `start`：开始时间（毫秒）
- `end`：结束时间（毫秒）

## 最佳实践

1. **选择合适的音色**：以 `Neural` 结尾的神经网络音色质量更高
2. **根据内容调整语速**：新闻适合较快，故事适合较慢
3. **使用自然的措辞**：标点符号会影响语音节奏
4. **试听音色**：不同音色适合不同类型的内容
5. **考虑受众**：选择与目标受众匹配的音色
6. **使用字幕增强可访问性**：为视频和演示文稿生成字幕
7. **优化输出格式**：专业用途选高码率，语音消息选低码率

## 命令行参数速查

| 参数 | 缩写 | 说明 | 默认值 |
|--------|---------|-------------|----------|
| --help | -h | 显示帮助信息 | - |
| --version | | 显示版本号 | - |
| --text | -t | 要转换的文本（必填） | - |
| --filepath | -f | 输出文件路径 | "./output.mp3" |
| --voice | -v | 音色名称 | "zh-CN-XiaoyiNeural" |
| --lang | -l | 语言代码 | "zh-CN" |
| --outputFormat | -o | 输出格式 | "audio-24khz-48kbitrate-mono-mp3" |
| --pitch | | 音调 | "default" |
| --rate | -r | 语速 | "default" |
| --volume | | 音量 | "default" |
| --saveSubtitles | -s | 保存字幕 | false |
| --proxy | -p | 代理地址 | - |
| --timeout | | 请求超时（毫秒） | 10000 |

## 使用限制

- 需要网络连接（使用微软 Edge 在线服务）
- 文本最大长度取决于服务限制
- 过度使用可能触发速率限制
- 音色可用性取决于微软 Edge 服务
- 并非所有韵律参数对所有音色都有效

## 与 Clawdbot 集成

配合 `tts` 工具使用时：
1. 使用 node-edge-tts 生成音频
2. 将音频文件保存到工作区
3. 返回 MEDIA: 路径给 Clawdbot
4. Clawdbot 将音频路由到相应频道

示例流程：
```javascript
// 生成音频
const outputPath = await textToSpeech("要转换的文本", {
  voice: "en-US-AriaNeural",
  lang: "en-US",
});

// 通过 tts 工具返回给 Clawdbot
// （调用 tts 工具时由 Clawdbot 内部处理）
```

## 版本信息

- 当前版本：1.2.9
- 最近发布：3 天前
- 许可协议：MIT
- 主页：github.com/SchneeHertz/node-edge-tts
