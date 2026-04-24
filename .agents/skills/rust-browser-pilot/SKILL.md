---
name: rust-browser-pilot
displayName: 极速浏览器自动化
emoji: "⚡"
summary: 基于 Rust 的浏览器自动化工具，DOM 处理速度是 Puppeteer 的 10 倍。
homepage: https://github.com/rknoche6/fast-browser-use
primaryEnv: bash
os:
  - darwin
  - linux
requires:
  bins:
    - chrome
install:
  - kind: brew
    formula: rknoche6/tap/fast-browser-use
  - kind: cargo
    package: fast-browser-use
config:
  requiredEnv:
    - CHROME_PATH
  example: |
    # Standard headless setup
    export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    export BROWSER_HEADLESS="true"
description: "基于 Rust 的高性能浏览器自动化工具，通过 Chrome DevTools 协议直接驱动浏览器，执行 DOM 提取、页面截图、表单填写、会话管理和站点地图分析等操作。启动速度和内存效率远超 Puppeteer 与 Selenium，非常适合网页抓取、自动化测试和需要复杂交互的场景。当用户需要自动化浏览器任务、提及网页抓取、自动化测试、DOM 提取、页面截图、表单填写、会话管理、站点地图分析，或比较 Puppeteer/Selenium 性能时触发。"
---

<!-- 本地化自: fast-browser-use -->

# 极速浏览器自动化

基于 Rust 的浏览器自动化引擎，提供一个轻量级二进制程序，通过 CDP 直接驱动 Chrome。专为高效的 DOM 提取、稳健的会话管理和极致速度而优化。

![终端演示](https://placehold.co/800x400/1e1e1e/ffffff?text=Terminal+Demo+Coming+Soon)

## 🧪 Agent 使用场景

### 1. 通过模拟真人行为绕过"反爬检测"
模拟鼠标抖动和随机延迟，抓取受保护的站点。

```bash
fast-browser-use navigate --url "https://protected-site.com" \
  --human-emulation \
  --wait-for-selector "#content"
```

### 2. "深度冻结"快照
捕获完整的 DOM 状态*和*计算样式，以便后续完美还原。

```bash
fast-browser-use snapshot --include-styles --output state.json
```

### 3. 登录与 Cookie 复用
手动登录一次，然后将会话保存下来，用于后续的无头自动化。

**步骤一：打开有界面的浏览器手动登录**
```bash
fast-browser-use login --url "https://github.com/login" --save-session ./auth.json
```

**步骤二：后续复用会话**
```bash
fast-browser-use navigate --url "https://github.com/dashboard" --load-session ./auth.json
```

### 4. 🚜 无限滚动数据采集器
**从无限滚动页面提取最新数据** —— 非常适合采集最新帖子、新闻或社交动态。

```bash
# Harvest headlines from Hacker News (scrolls 3x, waits 800ms between)
fast-browser-use harvest \
  --url "https://news.ycombinator.com" \
  --selector ".titleline a" \
  --scrolls 3 \
  --delay 800 \
  --output headlines.json
```

**实际输出**（约 6 秒内获取 59 条不重复结果）：
```json
[
  "Genode OS is a tool kit for building highly secure special-purpose OS",
  "Mobile carriers can get your GPS location",
  "Students using \"humanizer\" programs to beat accusations of cheating with AI",
  "Finland to end \"uncontrolled human experiment\" with ban on youth social media",
  ...
]
```

适用于所有无限滚动页面：Reddit、Twitter、LinkedIn 动态流、搜索结果等。

### 5. 📸 快速截图
将任意页面截图保存为 PNG：

```bash
fast-browser-use screenshot \
  --url "https://example.com" \
  --output page.png \
  --full-page  # Optional: capture entire scrollable page
```

### 6. 🗺️ 站点地图与页面结构分析器
通过解析站点地图和分析页面结构，了解网站的整体组织方式。

```bash
# Basic sitemap discovery (checks robots.txt + common sitemap URLs)
fast-browser-use sitemap --url "https://example.com"
```

```bash
# Full analysis with page structure (headings, nav, sections)
fast-browser-use sitemap \
  --url "https://example.com" \
  --analyze-structure \
  --max-pages 10 \
  --max-sitemaps 5 \
  --output site-structure.json
```

**参数说明：**
- `--analyze-structure`：同时提取页面结构（标题、导航、区块、元信息）
- `--max-pages N`：限制结构分析的页面数（默认：5）
- `--max-sitemaps N`：限制解析的站点地图数（默认：10，适用于大型站点）

**示例输出：**
```json
{
  "base_url": "https://example.com",
  "robots_txt": "User-agent: *\nSitemap: https://example.com/sitemap.xml",
  "sitemaps": ["https://example.com/sitemap.xml"],
  "pages": [
    "https://example.com/about",
    "https://example.com/products",
    "https://example.com/contact"
  ],
  "page_structures": [
    {
      "url": "https://example.com",
      "title": "Example - Home",
      "headings": [
        {"level": 1, "text": "Welcome to Example"},
        {"level": 2, "text": "Our Services"}
      ],
      "nav_links": [
        {"text": "About", "href": "/about"},
        {"text": "Products", "href": "/products"}
      ],
      "sections": [
        {"tag": "main", "id": "content", "role": "main"},
        {"tag": "footer", "id": "footer", "role": null}
      ],
      "main_content": {"tag": "main", "id": "content", "word_count": 450},
      "meta": {
        "description": "Example company homepage",
        "canonical": "https://example.com/"
      }
    }
  ]
}
```

利用此功能可以在抓取前了解站点架构、梳理导航流程或审计 SEO 结构。

## ⚡ 性能对比

| 特性 | Fast Browser Use (Rust) | Puppeteer (Node) | Selenium (Java) |
| :--- | :--- | :--- | :--- |
| **启动时间** | **< 50ms** | ~800ms | ~2500ms |
| **内存占用** | **15 MB** | 100 MB+ | 200 MB+ |
| **DOM 提取** | **零拷贝** | JSON 序列化 | 慢速桥接 |

## 功能与工具

### 视觉与提取
- **vision_map**：返回带有编号边框的截图，标注所有可交互元素。
- **snapshot**：捕获原始 HTML 快照（针对 AI 优化的 YAML/Markdown 格式）。
- **screenshot**：对页面进行可视化截图。
- **extract**：从 DOM 中提取结构化数据。
- **markdown**：将当前页面内容转换为 Markdown。
- **sitemap**：通过 robots.txt、站点地图和页面语义分析来解析站点结构。

### 导航与生命周期
- **navigate**：访问指定 URL。
- **go_back** / **go_forward**：前进/后退浏览历史。
- **wait**：暂停执行或等待特定条件。
- **new_tab**：打开新标签页。
- **switch_tab**：切换到指定标签页。
- **close_tab**：关闭当前或指定标签页。
- **tab_list**：列出所有打开的标签页。
- **close**：终止浏览器会话。

### 交互操作
- **click**：通过 CSS 选择器或 DOM 索引点击元素。
- **input**：在输入框中输入文本。
- **press_key**：发送键盘事件。
- **hover**：悬停在元素上。
- **scroll**：滚动视口。
- **select**：在下拉菜单中选择选项。

### 状态与调试
- **cookies**：管理会话 Cookie（获取/设置）。
- **local_storage**：管理本地存储数据。
- **debug**：访问控制台日志和调试信息。

## 使用说明

本 skill 专为需要维护状态（如保持登录）、处理动态 JavaScript 内容或同时管理多个页面的复杂网页交互场景而设计。相比标准的 fetch 工具，它提供更高的性能和更精细的控制。
