欢迎任何形式的贡献！
Skill 已发布到 clawhub https://www.clawhub.ai/rknoche6/fast-browser-use

# browser-use

一个通过 Chrome DevTools 协议（CDP）实现浏览器自动化的轻量级 Rust 库。

## ✨ 亮点

- **零 Node.js 依赖** - 纯 Rust 实现，通过 CDP 直接控制浏览器
- **轻量高速** - 无重量级运行时，开销极低
- **MCP 集成** - 内置模型上下文协议（Model Context Protocol）服务器，支持 AI 驱动的自动化
- **简洁 API** - 易用的工具集，覆盖常见浏览器操作

## 安装

```bash
cargo add browser-use
```

## 代码格式化

```bash
cargo +nightly fmt
```

## 快速开始

```rust
use browser_use::browser::BrowserSession;

// Launch browser and navigate
let session = BrowserSession::launch(Default::default())?;
session.navigate("https://example.com", None)?;

// Extract DOM with indexed interactive elements
let dom = session.extract_dom()?;
```

## MCP 服务器

运行内置的 MCP 服务器，实现 AI 驱动的浏览器自动化：

```bash
# Headless mode
cargo run --bin mcp-server

# Visible browser
cargo run --bin mcp-server -- --headed
```

## 功能特性

- 导航、点击、输入、截图、内容提取
- 带索引的可交互元素 DOM 提取
- 支持 CSS 选择器或数字索引定位元素
- 线程安全的浏览器会话管理

## 环境要求

- Rust 1.70+
- 已安装 Chrome 或 Chromium
