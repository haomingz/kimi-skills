# CODEBUDDY.md 本文件为 CodeBuddy Code 在此仓库中开发提供指导。

## 项目概述

`browser-use` 是一个通过 Chrome DevTools 协议（CDP）实现浏览器自动化的 Rust 库。它提供：

- 基于 `headless_chrome` 封装的浏览器会话管理器
- 覆盖常见浏览器操作的工具系统（导航、点击、输入、提取等）
- 带索引的可交互元素 DOM 提取
- 用于 AI 驱动浏览器自动化的 MCP（模型上下文协议）服务器

## 常用命令

### 构建

```bash
cargo build                    # Build library
cargo build --bin mcp-server  # Build MCP server binary
cargo build --release         # Production build
```

### 测试

```bash
cargo test                     # Run unit tests only
cargo test -- --ignored        # Run integration tests (requires Chrome installed)
cargo test dom_integration     # Run specific test file
```

### 运行

```bash
cargo run --bin mcp-server              # Run MCP server (headless)
cargo run --bin mcp-server -- --headed  # Run with visible browser
```

### 开发

```bash
cargo check        # Fast compile check
cargo clippy       # Linting
cargo fmt          # Format code
```

## 架构

### 模块结构

代码库分为五个主要模块：

**1. `browser/` - 浏览器管理**

- `session.rs`：`BrowserSession` 封装 `headless_chrome::Browser` 并管理标签页
- `config.rs`：`LaunchOptions` 和 `ConnectionOptions`，用于浏览器初始化配置
- 核心 API：`launch()`、`connect()`、`navigate()`、`extract_dom()`

**2. `dom/` - DOM 提取与索引**

- `tree.rs`：`DomTree` 表示带有索引可交互元素的页面结构
- `element.rs`：`ElementNode` 是可序列化的 DOM 节点，包含可见性/交互性元数据
- `extract_dom.js`：注入页面的 JavaScript，用于提取 DOM 并输出为 JSON
- 流程：JS 提取 → JSON → `ElementNode` 树 → 索引可交互元素 → `DomTree.selectors`

**3. `tools/` - 浏览器自动化工具**

- 每个工具独立一个文件：`navigate.rs`、`click.rs`、`input.rs`、`extract.rs`、`screenshot.rs`、`evaluate.rs`、`wait.rs`
- 所有工具实现 `Tool` trait，使用类型安全的参数结构体（如 `ClickParams`、`NavigateParams`）
- `ToolRegistry` 管理工具并通过 `ToolContext`（包含 `BrowserSession` + 可选的缓存 `DomTree`）执行
- 元素选择：工具接受 CSS 选择器或数字索引（来自 `DomTree`）
- **⚠️ 重要：添加新工具时，务必在 `src/mcp/mod.rs` 中使用 `register_mcp_tools!` 宏进行注册**

**4. `mcp/` - 模型上下文协议服务器**

- `handler.rs`：`BrowserServer` 将 `BrowserSession` 包装在 `Arc<Mutex<>>` 中，实现线程安全的 MCP 访问
- `mod.rs`：使用 `register_mcp_tools!` 宏从内部工具自动生成 MCP 工具包装
- 通过 `rmcp` crate 以 stdio 方式运行 MCP 服务器

**5. `error.rs` - 错误处理**

- `BrowserError` 枚举，包含启动/连接/导航/DOM/工具故障等变体
- 转换来自 `headless_chrome` 的 `anyhow::Error` 和 `serde_json::Error`

### 关键设计模式

**工具系统**：`Tool` trait 使用关联类型实现编译期参数校验：

```rust
trait Tool {
    type Params: Serialize + Deserialize + JsonSchema;
    fn execute_typed(&self, params: Self::Params, context: &mut ToolContext) -> Result<ToolResult>;
}
```

**DOM 索引**：为可交互元素分配数字索引，便于大语言模型定位：

- 提取 DOM → 遍历树 → 检测可交互元素（按钮、链接、输入框）
- 仅为可见且可交互的元素分配索引
- 工具可使用 `{"index": 5}` 替代复杂的 CSS 选择器

**双重元素选择**：工具同时接受两种方式：

- CSS 选择器：`{"selector": "#submit-btn"}`
- 数字索引：`{"index": 5}`（需先执行 DOM 提取）

**MCP 集成**：`register_mcp_tools!` 宏自动包装内部工具：

- 接收工具类型 + MCP 名称 + 描述
- 生成异步函数：锁定会话、调用工具、转换结果
- 所有工具在 `tool_router` 中注册，供 `rmcp` 调度器使用

### 测试策略

- 各模块内有针对结构体/枚举行为的单元测试
- `tests/` 目录中的集成测试需要 Chrome（标记 `#[ignore]` 属性）
- 运行需忽略的测试：`cargo test -- --ignored`
- 测试使用 `data:` URL 以避免网络依赖

## 重要实现说明

- MCP 服务器运行在单线程 Tokio 运行时中（`#[tokio::main(flavor = "current_thread")]`）
- `BrowserSession` 持有一个 `headless_chrome::Browser` 实例，每次管理一个活跃标签页
- DOM 提取通过在浏览器中执行 JavaScript 并解析返回的 JSON 实现
- 所有工具操作活跃标签页；使用 `switch_tab()` 切换上下文
- 元素索引仅对其对应的 DOM 提取结果有效
- 重新提取 DOM 会重建 `DomTree` 上的选择器列表并重新分配所有索引
- **在编写需要在浏览器中执行的 JavaScript 时，始终使用 `JSON.stringify()` 确保结果正确返回** —— 这可以避免复杂对象的问题，确保一致的序列化

## Crate 依赖

- `headless_chrome`：Chrome/Chromium 自动化的 CDP 客户端
- `rmcp`：模型上下文协议（MCP）服务器框架
- `serde`/`serde_json`：参数和 DOM 的 JSON 序列化
- `schemars`：工具参数的 JSON Schema 生成
- `thiserror`：简洁的错误定义
- `tokio`（可选）：MCP 服务器的异步运行时
- `clap`（可选）：MCP 服务器二进制的 CLI 参数解析

## 文件位置

- MCP 服务器二进制：`src/bin/mcp_server.rs`
- DOM 提取脚本：`src/dom/extract_dom.js`（通过 `include_str!` 嵌入）
- 集成测试：`tests/dom_integration.rs`
